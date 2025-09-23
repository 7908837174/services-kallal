# 📋 Commit Message Template

## Primary Title (50 chars max):
```
Fix CI ARM64 compatibility: replace arduino/setup-protoc@v1
```

## Detailed Commit Message:
```
Fix CI ARM64 compatibility by replacing arduino/setup-protoc@v1

The arduino/setup-protoc@v1 action contained x86_64-specific binaries
that failed on ARM64 systems (Apple M1/M2, ARM64 Linux) when using
the 'act' tool for local CI testing.

Changes:
- Replace arduino/setup-protoc@v1 with cross-platform shell script
- Auto-detect architecture (x86_64, aarch64, arm64) 
- Download appropriate protoc binary from official GitHub releases
- Install to /usr/local/bin/protoc with proper includes
- Upgrade to protoc v25.1 (latest stable)
- Add comprehensive error handling and validation

Files updated:
- .github/workflows/ci-go-cover.yml
- .github/workflows/ci.yml  
- .github/workflows/linters.yml
- .github/workflows/time-package.yml

Benefits:
- Enables local CI testing on ARM64 systems
- Maintains full backward compatibility
- No dependency on third-party actions with arch limitations
- Future-proof solution using official protoc releases

Fixes #60

Signed-off-by: Kallal Mukherjee <ritamukherje62@gmail.com>
```

### ✅ **DCO Fix Applied**
All commits have been rebased and properly signed off to comply with the Developer Certificate of Origin requirements.

## 🏷️ Pull Request Title Options:

### Option 1 (Concise):
```
Fix CI ARM64 compatibility by replacing arduino/setup-protoc@v1
```

### Option 2 (Descriptive):  
```
Fix ARM64 CI compatibility: replace arduino/setup-protoc@v1 with cross-platform installation
```

### Option 3 (Impact-focused):
```
Enable ARM64 CI support: fix protoc installation for Apple Silicon and ARM64 Linux
```

## 📝 PR Description Template:

```markdown
## 🐛 Bug Fix: ARM64 CI Compatibility 

**Fixes**: #60 

### Problem
The `arduino/setup-protoc@v1` action fails on ARM64 systems due to x86_64-specific binaries, blocking local CI testing with the `act` tool on Apple Silicon and ARM64 Linux.

### Solution  
✅ Cross-platform protoc installation script  
✅ Architecture auto-detection (x86_64, aarch64, arm64)  
✅ Official protoc v25.1 from GitHub releases  
✅ Comprehensive error handling  

### Impact
🍎 **ARM64 Support**: Apple M1/M2 Macs  
🐧 **Linux ARM64**: ARM64 Linux systems  
🔧 **Local CI**: Enables `act` tool usage  
⚡ **Zero Breaking Changes**: Fully backward compatible  

### Files Changed
- `.github/workflows/ci-go-cover.yml`
- `.github/workflows/ci.yml` 
- `.github/workflows/linters.yml`
- `.github/workflows/time-package.yml`

### Testing
✅ Architecture detection validated  
✅ protoc v25.1 installation verified  
✅ Cross-platform compatibility confirmed  
```