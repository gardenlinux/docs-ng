---
title: "Building Images"
description: "Build Garden Linux images and packages for development and contribution"
category: "contributing"
tags: ["build", "development", "packages", "contribution"]
---

# Building Images

Learn how to build Garden Linux images and packages for development and contribution purposes.

## Building Images for Development

For detailed instructions on building Garden Linux images, see the [Building Custom Flavors](/how-to/customization/building-flavors) guide, which covers:

- Build requirements and prerequisites
- Basic and advanced build commands
- Cross-architecture builds
- Parallel build options
- Secure boot image generation

## Building Packages

Garden Linux packages are built using [the package-build scripts](https://github.com/gardenlinux/package-build). Understanding the package build system is essential for contributing package changes.

### Package Repository Structure

Each package has its own GitHub repository following the naming convention `package-{package_name}`. These packages are automatically picked up by [the workflows in the 'repo'](https://github.com/gardenlinux/repo).

**Examples**:
- **Trivial example**: [`gardenlinux/package-containerd`](https://github.com/gardenlinux/package-containerd)
- **Non-trivial example**: [`gardenlinux/package-openssh`](https://github.com/gardenlinux/package-openssh)

### Package Build Strategy

Garden Linux follows a pragmatic approach to package management:

**Default approach**: Use binary packages as provided by Debian
- Leverages Debian's extensive testing and security processes
- Reduces maintenance burden
- Ensures compatibility with Debian ecosystem

**Rebuild only when necessary**: Create a `package-{package_name}` repository when:
- Garden Linux-specific patches are required
- Custom build environment is needed
- Package is temporarily unavailable in Debian testing

### Types of Package Rebuilds

#### 1. Source from Debian

Rebuild Debian packages with Garden Linux modifications.

**Use cases**:
- **Apply patches**: Add Garden Linux-specific patches on top of Debian source
- **Custom build environment**: Rebuild with specific compiler/runtime versions (e.g., newer golang, glibc, gcc)
- **Debian testing gaps**: Package temporarily removed from Debian testing (happens periodically)

**Example workflow**:
```bash
# Clone package repository
git clone https://github.com/gardenlinux/package-openssh
cd package-openssh

# Review Garden Linux patches
ls debian/patches/

# Build package
./build.sh
```

#### 2. Source from Upstream Project

Package software directly from upstream when Debian doesn't provide suitable packages.

**Use cases**:
- **Not in Debian**: Software not maintained by Debian
- **Version mismatch**: Debian maintains old version, newer upstream version required
- **Specialized needs**: Garden Linux requires features not in Debian package

**Example**:
```bash
# Clone package repository
git clone https://github.com/gardenlinux/package-{upstream-software}
cd package-{upstream-software}

# Check upstream source
cat debian/watch  # Upstream version tracking

# Build from upstream
./build.sh
```

#### 3. Native Source

Package software developed and maintained by Garden Linux team.

**Use cases**:
- **Garden Linux-specific tools**: Software developed by Garden Linux team
- **Integration components**: Tools for Garden Linux system integration
- **Custom utilities**: Garden Linux-specific system utilities

**Example**:
```bash
# Clone native package
git clone https://github.com/gardenlinux/package-{native-tool}
cd package-{native-tool}

# Source is maintained in repository
ls src/

# Build native package
./build.sh
```

## Package Development Workflow

### Set Up Package Development Environment

1. **Install build dependencies**:
   ```bash
   sudo apt install build-essential devscripts debhelper
   ```

2. **Clone package repository**:
   ```bash
   git clone https://github.com/gardenlinux/package-{package_name}
   cd package-{package_name}
   ```

3. **Review package structure**:
   ```bash
   # Debian packaging files
   ls debian/

   # Build scripts
   ls *.sh

   # Package-specific patches
   ls debian/patches/
   ```

### Make Package Changes

1. **Create feature branch**:
   ```bash
   git checkout -b feature/my-package-change
   ```

2. **Modify source or patches**:
   ```bash
   # Add new patch
   vim debian/patches/my-fix.patch
   
   # Update patch series
   echo "my-fix.patch" >> debian/patches/series
   ```

3. **Update changelog**:
   ```bash
   dch -i "Description of changes"
   ```

4. **Test build locally**:
   ```bash
   ./build.sh
   ```

### Submit Package Contributions

1. **Commit changes**:
   ```bash
   git add debian/
   git commit -m "package: Add fix for issue XYZ"
   ```

2. **Push and create PR**:
   ```bash
   git push origin feature/my-package-change
   # Create pull request on GitHub
   ```

3. **CI/CD validation**:
   - Automated builds run on PR
   - Package builds must succeed
   - Tests must pass

## Testing Package Changes

### Local Testing

Test your package changes before submitting:

```bash
# Build package
./build.sh

# Install locally in test environment
sudo dpkg -i ../package-name_version_arch.deb

# Verify functionality
# ... test your changes ...

# Remove test package
sudo apt remove package-name
```

### Integration Testing

Test packages within Garden Linux image:

```bash
# Build image with modified package
# (assuming package in local repo)
./build kvm-gardener_dev-amd64

# Test in QEMU
# ... verify package changes in running system ...
```

## Package Repository Automation

The [`gardenlinux/repo`](https://github.com/gardenlinux/repo) repository contains workflows that:

- Monitor package repositories for changes
- Trigger automated builds
- Publish packages to Garden Linux repository
- Maintain package metadata and dependencies

**Package updates are automated**:
1. Changes merged to package repository
2. Workflow detects change
3. Package builds automatically
4. Published to Garden Linux APT repository
5. Available in next image builds

## Best Practices

### Package Maintenance

- **Minimal changes**: Only rebuild when necessary
- **Document patches**: Clear commit messages and patch descriptions
- **Test thoroughly**: Build and test before submitting
- **Follow Debian policy**: Adhere to [Debian Policy](https://www.debian.org/doc/debian-policy/)
- **Version carefully**: Use appropriate version suffixes (e.g., `+gardenlinux1`)

### Security Considerations

- **Security patches**: Apply security fixes promptly
- **Upstream tracking**: Monitor upstream security advisories
- **Testing**: Verify security fixes don't introduce regressions
- **Documentation**: Document security-related changes clearly

## Troubleshooting

### Build Fails

**Missing dependencies**:
```bash
# Install build dependencies
sudo apt build-dep package-name

# Or install from debian/control
mk-build-deps -i debian/control
```

**Patch doesn't apply**:
```bash
# Refresh patches for new upstream version
quilt push -a
quilt refresh
```

### Package Won't Install

**Dependency issues**:
```bash
# Check dependencies
dpkg-deb -I package-name.deb

# Install with dependencies
sudo apt install -f ./package-name.deb
```

## Next Steps

- **Test images**: [Testing an Image](/contributing/testing-image)
- **Contribution workflow**: [Contribution Workflow](/contributing/workflow)
- **Code style**: [Code Style Guide](/contributing/code-style)
- **Build flavors**: [Building Custom Flavors](/how-to/customization/building-flavors)

## Related Documentation

- **Explanation**: [Architecture](/explanation/architecture) - Build system design
- **Reference**: [Feature Glossary](/reference/feature-glossary) - Available features
- **How-to**: [Testing Custom Builds](/how-to/customization/testing-builds) - Testing procedures
