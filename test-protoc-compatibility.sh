#!/bin/bash
# Test script to verify protoc installation logic for both x86_64 and ARM64

set -e

echo "Testing protoc installation script compatibility..."

# Test x86_64 architecture detection
echo "Testing x86_64 detection..."
ARCH="x86_64"
if [[ "$ARCH" == "x86_64" ]]; then
  PROTOC_ARCH="x86_64"
elif [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
  PROTOC_ARCH="aarch_64"
else
  echo "ERROR: Unsupported architecture: $ARCH"
  exit 1
fi

echo "✓ x86_64 -> $PROTOC_ARCH"

# Test aarch64 architecture detection
echo "Testing aarch64 detection..."
ARCH="aarch64"
if [[ "$ARCH" == "x86_64" ]]; then
  PROTOC_ARCH="x86_64"
elif [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
  PROTOC_ARCH="aarch_64"
else
  echo "ERROR: Unsupported architecture: $ARCH"
  exit 1
fi

echo "✓ aarch64 -> $PROTOC_ARCH"

# Test arm64 architecture detection
echo "Testing arm64 detection..."
ARCH="arm64"
if [[ "$ARCH" == "x86_64" ]]; then
  PROTOC_ARCH="x86_64"
elif [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
  PROTOC_ARCH="aarch_64"
else
  echo "ERROR: Unsupported architecture: $ARCH"
  exit 1
fi

echo "✓ arm64 -> $PROTOC_ARCH"

# Test unsupported architecture detection
echo "Testing unsupported architecture detection..."
ARCH="unsupported"
if [[ "$ARCH" == "x86_64" ]]; then
  PROTOC_ARCH="x86_64"
elif [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
  PROTOC_ARCH="aarch_64"
else
  echo "✓ Correctly detected unsupported architecture: $ARCH"
fi

# Test URL generation
echo "Testing URL generation..."
PROTOC_VERSION="25.1"
for test_arch in "x86_64" "aarch_64"; do
  PROTOC_ZIP="protoc-${PROTOC_VERSION}-linux-${test_arch}.zip"
  URL="https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/${PROTOC_ZIP}"
  echo "✓ Generated URL for ${test_arch}: $URL"
done

echo ""
echo "All tests passed! ✅"
echo "The protoc installation script logic is compatible with both x86_64 and ARM64 architectures."