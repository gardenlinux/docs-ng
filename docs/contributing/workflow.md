---
title: "Contribution Workflow"
description: "Git workflow, GitHub workflows, and contribution process for Garden Linux"
category: "contributing"
tags: ["workflow", "git", "github", "ci-cd", "contribution"]
---

# Contribution Workflow

Learn about the Git workflow, GitHub Actions pipelines, and contribution process for Garden Linux.

## Git Workflow

### Fork and Clone

1. **Fork the repository**:
   - Go to [github.com/gardenlinux/gardenlinux](https://github.com/gardenlinux/gardenlinux)
   - Click "Fork" button
   - Select your GitHub account

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/gardenlinux.git
   cd gardenlinux
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/gardenlinux/gardenlinux.git
   git fetch upstream
   ```

### Create Feature Branch

Create a branch for your changes:

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-improvement

# Or for bug fixes
git checkout -b fix/issue-123
```

**Branch naming conventions**:
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### Make Changes

1. **Make your changes**:
   - Edit files
   - Follow [Code Style](/contributing/code-style) guidelines
   - Add tests if applicable

2. **Test locally**:
   ```bash
   # Build image
   ./build kvm-gardener_dev-amd64
   
   # Run tests
   make test
   ```

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: Add new feature XYZ"
   ```

**Commit message format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or auxiliary tool changes

### Push and Create Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/my-improvement
   ```

2. **Create pull request**:
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Select base: `gardenlinux:main`
   - Select compare: `your-fork:feature/my-improvement`
   - Fill in PR description
   - Click "Create Pull Request"

### PR Review Process

1. **Automated checks run**:
   - CI/CD pipelines execute
   - Tests run
   - Build validation

2. **Review by maintainers**:
   - Code review
   - Feedback provided
   - Changes requested if needed

3. **Address feedback**:
   ```bash
   # Make requested changes
   git add .
   git commit -m "fix: Address review feedback"
   git push origin feature/my-improvement
   ```

4. **Merge**:
   - Once approved, maintainers merge
   - Branch can be deleted after merge

## GitHub Actions Workflows

Garden Linux uses GitHub Actions for CI/CD automation.

### Manually Triggered Workflows

| Workflow | Purpose | Side Effects |
|----------|---------|--------------|
| **manual_release** | Manually trigger a release build | Uploads to S3 bucket `gardenlinux-github-releases` |
| **manual_tests** | Run platform tests, build specific version, or download from S3 | Builds image and uploads to S3 if specified |
| **manual_gh_release_page** | Create GitHub release page for published Garden Linux release | Creates new release page on GitHub |
| **manual_tag_latest_container** | Tag container image as `latest` | Updates `latest` tag for specified container |
| **publish** | Publish containers after successful nightly or manual_release | Publishes to ghcr.io |
| **publish_s3** | Publish artifacts to S3 after successful nightly or manual_release | Uploads to S3 `gardenlinux-github-releases` |
| **cloud_test_cleanup** | Clean up cloud resources from platform tests | Removes cloud test resources |

### Trigger Manual Workflows

Access workflows at: [github.com/gardenlinux/gardenlinux/actions](https://github.com/gardenlinux/gardenlinux/actions)

**Example: Manually trigger nightly run**:
1. Go to [manual_release workflow](https://github.com/gardenlinux/gardenlinux/actions)
2. Click "Run workflow"
3. Select "nightly" as release target
4. Enter version (e.g., `2134.0.0`) or use `now`
   - ⚠️ Note: `today` doesn't work during S3 upload

**Example: Run platform tests**:
1. Go to [manual_tests workflow](https://github.com/gardenlinux/gardenlinux/actions)
2. Click "Run workflow"
3. Select platforms to test
4. Specify version if needed

### Scheduled Workflows

| Workflow | Schedule | Description | Side Effects |
|----------|----------|-------------|--------------|
| **nightly** | Daily | Builds current version from main, runs platform tests, uploads .0 release candidate | Uploads to S3 `gardenlinux-github-releases` |
| **cloud_test_cleanup** | Daily | Cleans up accumulated cloud resources from platform tests | Removes test resources |

### CI/CD Pipeline

**On Pull Request**:
1. Linting and code quality checks
2. Build validation
3. Unit tests
4. Integration tests (if applicable)
5. Documentation build check

**On Merge to Main**:
1. Full build process
2. Comprehensive test suite
3. Container image creation
4. Artifact generation

**On Release**:
1. Version tagging
2. Release build
3. Platform tests
4. Publish to registries
5. S3 artifact upload
6. GitHub release creation

## Best Practices

### Before Creating PR

- [ ] Code follows [Code Style](/contributing/code-style)
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main
- [ ] No merge conflicts

### PR Description

Include in your PR description:
- **What**: Brief description of changes
- **Why**: Motivation and context
- **How**: Technical approach
- **Testing**: How changes were tested
- **Related**: Link to related issues

**Example**:
```markdown
## What
Adds support for ARM64 architecture in KVM builds

## Why
Users requested ARM64 support for development environments

## How
- Modified build scripts to detect architecture
- Added ARM64-specific configuration
- Updated documentation

## Testing
- Built KVM image for ARM64
- Tested boot process in QEMU
- Verified all features work

## Related
Closes #123
```

### During Review

- Respond to feedback promptly
- Ask questions if feedback is unclear
- Make requested changes in new commits
- Don't force-push after review starts
- Mark conversations as resolved when addressed

### After Merge

- Delete your feature branch
- Update local main branch
- Close related issues if not auto-closed

## Troubleshooting

### Merge Conflicts

```bash
# Update your branch with upstream changes
git fetch upstream
git rebase upstream/main

# Resolve conflicts in your editor
# After resolving:
git add .
git rebase --continue

# Force push (only if no one else is using your branch)
git push origin feature/my-improvement --force
```

### Failed CI Checks

1. **Review failure logs** in GitHub Actions
2. **Reproduce locally**:
   ```bash
   # Run same checks
   make test
   ./build kvm-gardener_dev-amd64
   ```
3. **Fix issues** and push again
4. **Checks re-run automatically**

### PR Not Merging

**Common reasons**:
- Failed CI checks
- Unresolved review comments
- Merge conflicts
- Missing required reviews

**Resolution**:
- Address all CI failures
- Respond to all review comments
- Resolve merge conflicts
- Request reviews from maintainers

## Related Documentation

- **Contributing**: [Building Images](/contributing/building-image) - Build and package development
- **Contributing**: [Testing Images](/contributing/testing-image) - Testing procedures
- **Contributing**: [Code Style](/contributing/code-style) - Coding standards
- **How-to**: [Building Custom Flavors](/how-to/customization/building-flavors) - Build instructions
