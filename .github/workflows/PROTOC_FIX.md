# Protoc Installation Fix for ARM64 Compatibility

## Issue
The CI workflows were using `arduino/setup-protoc@v1` which contained x86_64-specific binaries that failed on ARM64 systems like Apple M1 Macs.

## Solution
Replaced the `arduino/setup-protoc@v1` action with a manual installation script that:

1. Detects the system architecture (`x86_64` or `aarch64`/`arm64`)
2. Downloads the appropriate protoc binary from the official Protocol Buffers releases
3. Installs it to `/usr/local/bin/protoc` with proper includes
4. Verifies the installation

## Files Changed
- `.github/workflows/ci-go-cover.yml`
- `.github/workflows/ci.yml`
- `.github/workflows/linters.yml`
- `.github/workflows/time-package.yml`

## Testing
The fix supports both architectures:
- `x86_64`: Downloads `protoc-25.1-linux-x86_64.zip`
- `aarch64`/`arm64`: Downloads `protoc-25.1-linux-aarch_64.zip`

## Local Testing
To test the CI locally on ARM64 systems using the `act` tool, this fix ensures protoc installs correctly on both x86_64 and ARM64 runners.

Fixes #60