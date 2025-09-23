# 🔧 Fix CI ARM64 Compatibility: Replace arduino/setup-protoc@v1 with Cross-Platform Solution

## 📋 **Pull Request Summary**

**Fixes Issue**: #60 - BUG: the .github/workflows/ci-go-cover.yml action relies on an action that is x86_64-specific

### 🎯 **Title**
```
Fix CI ARM64 compatibility by replacing arduino/setup-protoc@v1 with cross-platform protoc installation
```

### 📝 **Detailed Description**

This PR resolves the ARM64 compatibility issue in GitHub Actions workflows that prevented local CI testing on Apple M1/M2 Macs and ARM64 systems using the `act` tool.

#### **Problem**
- The `arduino/setup-protoc@v1` action contained x86_64-specific binaries in its `node_modules/@actions/tool-cache/scripts/externals/` directory
- When running CI locally on ARM64 systems, users encountered: `qemu-x86_64: Could not open '/lib64/ld-linux-x86-64.so.2': No such file or directory`
- This blocked local development and testing workflows for ARM64 users

#### **Solution**
Replaced the problematic action with a robust shell script that:

1. **🔍 Auto-detects system architecture**:
   - `x86_64` → Downloads `protoc-25.1-linux-x86_64.zip`
   - `aarch64`/`arm64` → Downloads `protoc-25.1-linux-aarch_64.zip`
   - Graceful error handling for unsupported architectures

2. **📦 Direct installation from official releases**:
   - Downloads from `https://github.com/protocolbuffers/protobuf/releases/`
   - Installs to `/usr/local/bin/protoc` with proper includes
   - Verifies installation with `protoc --version`

3. **🚀 Upgraded to latest stable protoc v25.1**

### 🛠 **Files Changed**

| File | Change Description |
|------|-------------------|
| `.github/workflows/ci-go-cover.yml` | ✅ Replaced arduino action with cross-platform script |
| `.github/workflows/ci.yml` | ✅ Replaced arduino action with cross-platform script |
| `.github/workflows/linters.yml` | ✅ Replaced arduino action with cross-platform script |
| `.github/workflows/time-package.yml` | ✅ Replaced arduino action with cross-platform script |
| `.github/workflows/PROTOC_FIX.md` | ✅ Added comprehensive documentation |

### 🧪 **Testing**

- ✅ **Architecture Detection**: Validated logic for x86_64, aarch64, and arm64
- ✅ **URL Validation**: Confirmed official release URLs exist for both architectures
- ✅ **Installation Test**: Successfully installed protoc v25.1 on current system
- ✅ **Compatibility**: Maintains backward compatibility with existing workflows

### 🎯 **Benefits**

1. **🍎 ARM64 Support**: Full compatibility with Apple M1/M2 Macs
2. **🐧 Linux ARM64**: Works on ARM64 Linux systems
3. **🔧 Local CI**: Enables `act` tool usage on ARM64 systems
4. **📈 Future-Proof**: No dependency on third-party actions with architecture limitations
5. **🛡️ Robust**: Proper error handling and validation
6. **📚 Documented**: Comprehensive documentation for maintainers

### 🔄 **Migration Path**

The change is **fully backward compatible**:
- Existing x86_64 CI runners continue working without changes
- New ARM64 support is automatically enabled
- No breaking changes to the build process
- Same protoc functionality with improved compatibility

### 🤝 **Community Impact**

This fix addresses feedback from the community:
- Resolves @dreemkiller's reported issue with M1 MacBook Pro
- Enables broader developer participation regardless of hardware architecture
- Improves developer experience for local CI testing

### 📖 **Documentation**

Added `.github/workflows/PROTOC_FIX.md` with:
- Problem description and root cause analysis
- Technical solution details
- Architecture support matrix
- Future maintenance guidelines

---

## 🚀 **Ready for Review**

This PR is ready for merge and will immediately resolve ARM64 compatibility issues for all Veraison Services contributors using Apple Silicon or ARM64 Linux systems.

**Branch**: `fix-ci-arm64-compatibility`  
**Base**: `main`  
**Commits**: 4 focused commits with clear history and proper DCO signoffs  
**Impact**: Zero breaking changes, pure enhancement  

### ✅ **DCO Compliance**
All commits are properly signed off with `Signed-off-by: Kallal Mukherjee <ritamukherje62@gmail.com>` as required by the project's Developer Certificate of Origin policy.

### 🏷️ **Labels**
- `bug` - Fixes existing issue
- `ci` - Continuous Integration improvement  
- `enhancement` - Adds ARM64 support
- `documentation` - Includes comprehensive docs