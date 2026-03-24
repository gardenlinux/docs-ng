---
title: "Documentation Overview"
description: "How Garden Linux documentation is organized"
---

# How Our Documentation Is Organized

Garden Linux documentation is organized to help you find what you need quickly, whether you're learning the basics, solving a specific problem, understanding concepts, or looking up technical details.

## Documentation Structure

Our documentation follows a proven framework that organizes content by **what you need**, not by your role. Here's how to navigate:

### 🎓 Tutorials — "I want to learn"

**Purpose**: Learn by doing with step-by-step guides  
**Best for**: Newcomers, those trying Garden Linux for the first time

Tutorials are hands-on, learning-oriented guides that walk you through complete workflows from start to finish. Each tutorial:
- Starts from zero knowledge
- Provides complete, copy-pasteable commands
- Guarantees success if followed exactly
- Takes 15-30 minutes to complete

**Start here**: [First Boot Tutorials](/tutorials/)

**Examples**:
- First Boot on AWS, Azure, GCP, KVM, Lima, etc.
- Complete walkthroughs for each platform

---

### 🛠️ How-to Guides — "I want to accomplish a task"

**Purpose**: Step-by-step solutions for specific problems  
**Best for**: Users who know what they want to do

How-to guides are goal-oriented instructions that help you accomplish specific tasks. They assume some familiarity with Garden Linux and focus on practical solutions.

**Start here**: [How-to Guides](/how-to/)

**Categories**:
- **Getting Started**: Choosing flavors, getting images, initial configuration
- **Platform-Specific**: AWS, Azure, GCP, KVM, OpenStack, Lima, OCI, VMware, Bare Metal
- **Security**: SSH hardening, Secure Boot, time configuration
- **Customization**: Building features and flavors, testing builds
- **System Management**: Updates, users, disks, APT repositories

---

### 💡 Explanation — "I want to understand"

**Purpose**: Background, concepts, and design philosophy  
**Best for**: Users who want to understand *why* and *how* things work

Explanations provide context and background to help you think about Garden Linux. They're discursive and conceptual rather than task-focused.

**Start here**: [Explanation](/explanation/)

**Topics**:
- **Use Cases**: Why use Garden Linux? What problems does it solve?
- **Flavors and Features**: How the build system works
- **Image Types**: Different formats and boot modes
- **Architecture**: System design and components
- **Security Posture**: Security philosophy and approach
- **Release Cadence**: Release lifecycle and versioning
- **Design Decisions**: Key architectural choices and rationale

---

### 📚 Reference — "I want to look something up"

**Purpose**: Technical specifications and lookup tables  
**Best for**: Users who need accurate, detailed information

Reference documentation provides concise, accurate technical details organized for quick lookup.

**Start here**: [Reference](/reference/)

**Includes**:
- **Flavor Matrix**: Complete table of all available flavors
- **Feature Glossary**: All features documented
- **Platform Compatibility**: Which platforms support which features
- **Image Formats**: Naming conventions and specifications
- **Kernels and Modules**: Kernel versions and module support
- **Releases**: Maintained releases and release notes
- **API Documentation**: CLI and Python library reference

---

### 🤝 Contributing

**Purpose**: Guidelines for contributing to Garden Linux  
**Best for**: Contributors to code or documentation

Contributing guides explain how to participate in Garden Linux development.

**Start here**: [Contributing](/contributing/)

**Topics**:
- Documentation guide
- Building and testing images
- Contribution workflow
- Code style and conventions
- Dependency policy

---

## Where Should I Start?

Choose your path based on your situation:

| Your Situation | Where to Go |
|----------------|-------------|
| **New to Garden Linux?** | Start with [Tutorials](/tutorials/) to learn the basics |
| **Need to deploy on a specific platform?** | Go to [How-to Guides → Platform-Specific](/how-to/platform-specific/) |
| **Want to customize Garden Linux?** | Check [How-to Guides → Customization](/how-to/customization/) |
| **Need to understand concepts?** | Read [Explanation](/explanation/) for background |
| **Looking for specific details?** | Search [Reference](/reference/) documentation |
| **Want to contribute?** | See [Contributing](/contributing/) guidelines |

## Documentation Principles

### Content Types

Each section has a specific purpose:

- **Tutorials** teach through practice
- **How-to guides** solve specific problems
- **Explanations** provide understanding
- **Reference** offers precise specifications

### Finding Related Content

Documentation types are interconnected:

- **Tutorials** link to relevant **how-to guides** for variations
- **How-to guides** link to **explanations** for background
- **Explanations** link to **reference** for detailed specs
- **Reference** links to **tutorials** and **how-to guides** for examples

### Getting Help

If you can't find what you need:

1. Use the **search** feature (top navigation)
2. Check the [FAQ or troubleshooting guides](/how-to/) (if applicable)
3. Visit the [Garden Linux GitHub repository](https://github.com/gardenlinux/gardenlinux)
4. Open an issue or discussion on GitHub

## About This Organization

This documentation structure is based on the [Diátaxis framework](https://diataxis.fr/), a systematic approach to technical documentation that organizes content by user needs rather than by topics or roles. This makes it easier to find the right information at the right time.