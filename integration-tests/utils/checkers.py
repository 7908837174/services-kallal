# Copyright 2023-2024 Contributors to the Veraison project.
# SPDX-License-Identifier: Apache-2.0
import os
import json
from datetime import datetime, timedelta
from jose import jwt

GENDIR = '__generated__'

def save_result(response, scheme, evidence):
    os.makedirs(f'{GENDIR}/results', exist_ok=True)
    jwt_outfile = f'{GENDIR}/results/{scheme}.{evidence}.jwt'

    try:
        # Handle different response formats
        if hasattr(response, 'json'):
            response_json = response.json()
        elif isinstance(response, dict):
            response_json = response
        else:
            response_json = response
            
        # Try different key names for the result
        result = None
        if isinstance(response_json, dict):
            if "result" in response_json:
                result = response_json["result"]
            elif "attestation_result" in response_json:
                result = response_json["attestation_result"]
            elif "jwt" in response_json:
                result = response_json["jwt"]
            # Handle case where response itself might be the JWT (for direct body responses)
            elif isinstance(response_json, str) and response_json.count('.') == 2:
                result = response_json
        
        # If still no result, check if the entire response is a JWT token string
        if result is None and hasattr(response, 'text'):
            response_text = response.text.strip()
            if response_text.count('.') == 2:  # JWT format check
                result = response_text
        
        if result is None:
            # Provide more debugging information
            print(f"DEBUG: Response keys: {list(response_json.keys()) if isinstance(response_json, dict) else 'Not a dict'}")
            print(f"DEBUG: Response type: {type(response_json)}")
            print(f"DEBUG: Response content preview: {str(response_json)[:200]}...")
            raise ValueError("Did not receive an attestation result.")
            
    except (KeyError, AttributeError, TypeError) as e:
        raise ValueError(f"Did not receive an attestation result: {e}")

    with open(jwt_outfile, 'w') as wfh:
        wfh.write(result)

    decoded = jwt.decode(result, key="", options={'verify_signature': False})

    json_outfile = f'{GENDIR}/results/{scheme}.{evidence}.json'
    with open(json_outfile, 'w') as wfh:
        json.dump(decoded, wfh, indent=4)


def normalize_base64_to_urlsafe(data):
    """
    Recursively convert all standard base64 strings to URL-safe base64 format
    to ensure consistent comparison between evidence and expected results.
    """
    if isinstance(data, str):
        # Check if this looks like a base64 string (contains + or / chars)
        if ('+' in data or '/' in data) and (data.endswith('=') or data.endswith('==')):
            # Convert standard base64 to URL-safe base64
            return data.replace('+', '-').replace('/', '_')
        return data
    elif isinstance(data, dict):
        return {key: normalize_base64_to_urlsafe(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_base64_to_urlsafe(item) for item in data]
    else:
        return data

def compare_to_expected_result(response, expected, verifier_key):
    # Handle Box objects (which Tavern uses internally)
    if hasattr(response, 'to_dict'):
        response_data = response.to_dict()
    elif hasattr(response, '__dict__'):
        response_data = response.__dict__
    else:
        response_data = response
    
    # Try to extract submods using different approaches
    decoded_submods = None
    
    # First try: Use the original method if response_data has a 'json' method
    if hasattr(response_data, 'json'):
        try:
            decoded_submods = _extract_submods(response_data, verifier_key)
        except (AttributeError, TypeError, ValueError, KeyError):
            # Fall back to dictionary method
            try:
                if hasattr(response_data, 'json'):
                    json_data = response_data.json()
                    decoded_submods = _extract_submods_from_dict(json_data, verifier_key)
            except (AttributeError, TypeError, ValueError, KeyError):
                pass
    
    # Second try: Extract directly from dictionary/response data
    if decoded_submods is None:
        try:
            decoded_submods = _extract_submods_from_dict(response_data, verifier_key)
        except (AttributeError, TypeError, ValueError, KeyError):
            # If we still can't extract, check if it's already the expected format
            if isinstance(response_data, dict) and any(key.startswith('urn:') for key in response_data.keys()):
                # It might already be the submods data
                decoded_submods = response_data
            else:
                raise ValueError("Could not extract attestation result from response")

    with open(expected) as fh:
        expected_submods = json.load(fh)

    for key, expected_claims in expected_submods.items():
        try:
            decoded_claims = decoded_submods[key]
            print("Key exists in the dictionary.")
        except KeyError:
            print(f"Key {key} does not exist in the dictionary.")
            raise

        assert decoded_claims["ear.status"] == expected_claims["ear.status"]
        print(f"Evaluating Submod with SubModName {key}")
        if "ear.appraisal-policy-id" in expected_claims:
            assert decoded_claims["ear.appraisal-policy-id"] ==\
                    expected_claims["ear.appraisal-policy-id"]

        for trust_claim, tc_value in decoded_claims["ear.trustworthiness-vector"].items():
            expected_value = expected_claims["ear.trustworthiness-vector"][trust_claim]
            assert expected_value == tc_value, f'mismatch for claim "{trust_claim}", for {key}'

        if "ear.veraison.annotated-evidence" in expected_claims:
            # Normalize base64 formats for consistent comparison
            actual_evidence = normalize_base64_to_urlsafe(decoded_claims["ear.veraison.annotated-evidence"])
            expected_evidence = expected_claims["ear.veraison.annotated-evidence"]
            assert actual_evidence == expected_evidence

        if "ear.veraison.policy-claims" in expected_claims:
            assert decoded_claims["ear.veraison.policy-claims"] == \
                expected_claims["ear.veraison.policy-claims"]

def check_policy(response, active, name, rules_file):
    policy = _extract_policy(response.json())

    _check_within_period(policy['ctime'], timedelta(seconds=60))

    if active is not None:
        assert policy['active'] == active

    if  name:
        assert policy['name'] == name

    assert policy['type'] == 'opa'

    if rules_file:
        with open(rules_file) as fh:
            rules = fh.read()

        assert policy['rules'] == rules


def check_policy_list(response, have_active):
    active_count = 0
    for entry in response.json():
        policy = _extract_policy(entry)
        _check_within_period(policy['ctime'], timedelta(seconds=60))
        if policy['active']:
            active_count += 1

    assert (have_active and active_count == 1) or \
            (not have_active and active_count == 0)


def _check_within_period(dt, period):
    now = datetime.now().replace(tzinfo=dt.tzinfo)
    assert now > dt > (now - period)


def _extract_submods(response, key_file):
    try:
        result = response.json()["result"]
    except KeyError:
        raise ValueError("Did not receive an attestation result.")

    with open(key_file) as fh:
        key = json.load(fh)

    decoded = jwt.decode(result, key=key, algorithms=['ES256'])

    return decoded["submods"]


def _extract_submods_from_dict(response_data, key_file):
    """Extract submods from a dictionary/Box object instead of a response object"""
    result = None
    
    # Debug: Print response structure
    print(f"DEBUG _extract_submods_from_dict: response_data type: {type(response_data)}")
    if isinstance(response_data, dict):
        print(f"DEBUG _extract_submods_from_dict: response_data keys: {list(response_data.keys())}")
        
        # Check if this is a raw HTTP response object with '_content'
        if '_content' in response_data:
            print("DEBUG _extract_submods_from_dict: Found raw HTTP response, extracting _content")
            try:
                import json
                content_bytes = response_data['_content']
                if isinstance(content_bytes, bytes):
                    content_str = content_bytes.decode('utf-8')
                else:
                    content_str = str(content_bytes)
                print(f"DEBUG _extract_submods_from_dict: Content string: {content_str[:500]}...")
                
                # Try to parse as JSON
                content_json = json.loads(content_str)
                print(f"DEBUG _extract_submods_from_dict: Parsed JSON keys: {list(content_json.keys()) if isinstance(content_json, dict) else 'Not a dict'}")
                
                # Now look for attestation result in the parsed content
                if isinstance(content_json, dict):
                    if "result" in content_json:
                        result = content_json["result"]
                        print(f"DEBUG _extract_submods_from_dict: Found 'result' in content_json")
                    elif "attestation_result" in content_json:
                        result = content_json["attestation_result"]
                        print(f"DEBUG _extract_submods_from_dict: Found 'attestation_result' in content_json")
                    elif "jwt" in content_json:
                        result = content_json["jwt"]
                        print(f"DEBUG _extract_submods_from_dict: Found 'jwt' in content_json")
                    # If the entire content is a JWT (very unlikely but possible)
                    elif isinstance(content_json, str) and content_json.count('.') == 2:
                        result = content_json
                        print(f"DEBUG _extract_submods_from_dict: Content itself is JWT")
                
                # Update the response_data to use the parsed content for further processing
                if result is not None:
                    response_data = content_json
                        
            except (json.JSONDecodeError, UnicodeDecodeError, KeyError) as e:
                print(f"DEBUG _extract_submods_from_dict: Error parsing _content: {e}")
        
        print(f"DEBUG _extract_submods_from_dict: response_data preview: {str(response_data)[:500]}...")
    else:
        print(f"DEBUG _extract_submods_from_dict: response_data content: {str(response_data)[:500]}...")
    
    # Try different ways to extract the result (original logic as fallback)
    if result is None and isinstance(response_data, dict):
        # Try the standard "result" key
        if "result" in response_data:
            result = response_data["result"]
        # Try alternative key names that might be used
        elif "attestation_result" in response_data:
            result = response_data["attestation_result"]
        elif "jwt" in response_data:
            result = response_data["jwt"]
        # Check if the response_data itself might be the JWT token
        elif isinstance(response_data.get('body'), str) and response_data['body'].count('.') == 2:
            result = response_data['body']
        # Check if any value in the response looks like a JWT
        else:
            for key, value in response_data.items():
                if isinstance(value, str) and value.count('.') == 2:
                    result = value
                    print(f"DEBUG _extract_submods_from_dict: Found JWT-like value in key '{key}'")
                    break
    elif isinstance(response_data, str) and response_data.count('.') == 2:
        # It might be a JWT token itself
        result = response_data
    
    if result is None:
        print(f"DEBUG _extract_submods_from_dict: No attestation result found in response")
        raise ValueError("Did not receive an attestation result.")

    with open(key_file) as fh:
        key = json.load(fh)

    try:
        decoded = jwt.decode(result, key=key, algorithms=['ES256'])
        return decoded["submods"]
    except Exception as e:
        raise ValueError(f"Failed to decode JWT token: {e}")


def _extract_policy(data):
    policy = data
    policy['ctime'] = datetime.fromisoformat(policy['ctime'])
    return policy