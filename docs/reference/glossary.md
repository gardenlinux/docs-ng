---
title: "Glossary"
order: 1
---

# Glossary

This glossary provides definitions for Garden Linux-specific terminology. If you would like to contribute additional terms or improve existing definitions, please visit our [contributing guide](../contributing/index.md).

**Jump to:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [I](#i) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v)

---

## A

### ADR (Architecture Decision Record)

A document that captures an important architectural decision made about the Garden Linux system. ADRs provide context, rationale, and consequences of decisions. Garden Linux stores ADRs in the [reference/adr](./adr/index.md) section. See [ADR-0001](./adr/0001-record-architecture-decisions.md) for more background on why Garden Linux uses ADRs, and [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) by Michael Nygard for the original concept.

### Architecture

The processor architecture for which a Garden Linux image is built. Supported architectures include `amd64` (x86-64) and `arm64` (ARM 64-bit). The architecture can be specified as the last component of a build flavor string, e.g., `kvm-python-amd64`. See [Architecture documentation](../explanation/architecture.md) for details on Garden Linux system design.

### AWS

Amazon Web Services. One of the major cloud platforms supported by Garden Linux. Garden Linux provides AWS-specific images through the [`aws`](https://github.com/gardenlinux/gardenlinux/blob/main/features/aws/README.md) platform feature with cloud-init integration and AWS-specific kernel modules. See [AWS platform guide](../how-to/platform-specific/aws.md) and [AWS first boot tutorial](../tutorials/cloud/first-boot-aws.md) for usage details.

### Azure

Microsoft Azure. A major cloud platform supported by Garden Linux through the [`azure`](https://github.com/gardenlinux/gardenlinux/blob/main/features/azure/README.md) platform feature with platform-specific image configurations and optimizations. See [Azure platform guide](../how-to/platform-specific/azure.md) and [Azure first boot tutorial](../tutorials/cloud/first-boot-azure.md) for usage details.

---

## B

### Bare Metal

A platform target for Garden Linux images designed to run directly on physical hardware without a hypervisor through the [`baremetal`](https://github.com/gardenlinux/gardenlinux/blob/main/features/baremetal/README.md) platform feature. Also referred to as [`metal`](https://github.com/gardenlinux/gardenlinux/blob/main/features/metal/README.md) in build configurations. See [Bare Metal platform guide](../how-to/platform-specific/bare-metal.md) and [Bare Metal first boot tutorial](../tutorials/on-premises/first-boot-bare-metal.md) for usage details.

### Builder

The [gardenlinux/builder](https://github.com/gardenlinux/builder) component that creates customized Linux distributions. The builder is a separate project maintained by the Garden Linux team and is used to build Garden Linux images with specific flavors and features. See [Building Images documentation](../how-to/building-images.md) for practical guidance, [ADR-0020](./adr/0020-enforce-single-platform-by-default-in-builder.md) for details on platform enforcement in the builder, and [ADR-0031](./adr/0031-builder-glci-interface.md) for the builder-GLCI interface design.

### Build Flavor String

The hyphenated string used with the `./build` command that specifies the platform, features, and optionally the architecture for a Garden Linux image. Format: `${platform}-${feature1}-${feature2}-${arch}`. Examples: `kvm-python_dev`, `aws-gardener_prod-amd64`. See [Building Flavors guide](../how-to/customization/building-flavors.md) for detailed instructions.

---

## C

### CIS (Center for Internet Security)

A framework providing security configuration benchmarks. Garden Linux offers optional CIS compliance through the [`cis`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cis/README.md) feature and related sub-features ([`cisAudit`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisAudit/README.md), [`cisModprobe`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisModprobe/README.md), [`cisOS`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisOS/README.md), [`cisPackages`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisPackages/README.md), [`cisPartition`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisPartition/README.md), [`cisSshd`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisSshd/README.md), [`cisSysctl`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cisSysctl/README.md)). See [ADR-0017](./adr/0017-feature-cis-to-retain-shell-scripts.md) for details on the CIS feature implementation and [ADR-0029](./adr/0029-cis-selinux-permissive.md) regarding SELinux in permissive mode for CIS compliance.

### Cloud Image

A Garden Linux image optimized for cloud platforms (AWS, Azure, GCP, etc.) with cloud-init support and platform-specific configurations. See [Image Types documentation](../explanation/image-types.md) and [Image Formats reference](./image-formats.md) for more details.

### Container Image

A Garden Linux image packaged for use with container runtimes. Available through GitHub Packages at `ghcr.io/gardenlinux/gardenlinux`. See [Image Types documentation](../explanation/image-types.md) for more details.

---

## D

### Debian

The upstream Linux distribution on which Garden Linux is based. Garden Linux is a Debian GNU/Linux derivative that provides customized, auditable images with a focus on cloud and security features.

### Dependabot

GitHub's automated dependency update tool. See [ADR-0003](./adr/0003-builder-updates-dependabot.md) (later reverted by [ADR-0018](./adr/0018-revert-0003-builder-updates-dependabot.md)) for the history of Dependabot usage in the builder project.

### Distribution

Refers to a Garden Linux release or version. See [ADR-0002](./adr/0002-dists-can-never-change-retroactively.md) which establishes that distributions can never change retroactively, ensuring stability and reproducibility.

### dracut

The initramfs infrastructure used by Garden Linux to generate the initial RAM filesystem. Garden Linux uses dracut-generated initramfs instead of initramfs-tools used by standard Debian.

---

## E

### Ephemeral

Refers to the [`_ephemeral`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_ephemeral/README.md) feature that configures Garden Linux for stateless operation where no persistent state is maintained between reboots.

---

## F

### Feature

A modular component that adds specific functionality to a Garden Linux image. Features are defined in the `features/` directory. Features prefixed with an underscore (`_`) are internal/private (e.g., [`_secureboot`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_secureboot/README.md), [`_dev`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_dev/README.md)), while features without a prefix are public (e.g., [`cis`](https://github.com/gardenlinux/gardenlinux/blob/main/features/cis/README.md), [`gardener`](https://github.com/gardenlinux/gardenlinux/blob/main/features/gardener/README.md), [`python`](https://github.com/gardenlinux/gardenlinux/blob/main/features/python/README.md)). See [Flavors and Features documentation](../explanation/flavors-and-features.md) for an overview, and [ADR-0032](./adr/0032-static-feature-test-coverage-analysis.md) for details on feature test coverage analysis.

### FedRAMP

Federal Risk and Authorization Management Program. Garden Linux provides an optional [`fedramp`](https://github.com/gardenlinux/gardenlinux/blob/main/features/fedramp/README.md) feature for US federal compliance requirements.

### FIPS

Federal Information Processing Standards. The [`_fips`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_fips/README.md) feature enables FIPS 140-2/140-3 cryptographic module compliance in Garden Linux.

### Firecracker

A lightweight virtual machine monitor (VMM) for running microVMs. Garden Linux historically supported Firecracker as a platform. See [ADR-0012](./adr/0012-remove-firecracker-feature.md) for details on why Firecracker support was discontinued.

### Flavor

A specific combination of a platform and one or more features that defines a complete Garden Linux image configuration. Flavors are expressed as hyphen-separated strings, e.g., `kvm-python_dev` or `aws-gardener_prod-amd64`. The platform must come first, and the architecture (if specified) must come last. See [Flavors and Features documentation](../explanation/flavors-and-features.md), [Choosing Flavors guide](../how-to/choosing-flavors.md), and [Flavor Matrix reference](./flavor-matrix.md) for more details.

---

## G

### Garden Linux

A Debian GNU/Linux derivative designed to provide small, auditable Linux images for cloud providers and bare-metal machines. Garden Linux is optimized for Gardener nodes and provides extensive customization through features. See [Design Decisions](../explanation/design-decisions.md), [Use Cases](../explanation/use-cases.md), and [Security Posture](../explanation/security-posture.md) for more information.

### Gardener

[Gardener](https://gardener.cloud/) is a Kubernetes-based platform for managing clusters across multiple cloud providers. Garden Linux is the recommended operating system for Gardener worker nodes through the [`gardener`](https://github.com/gardenlinux/gardenlinux/blob/main/features/gardener/README.md) feature. See [Gardener platform guide](../how-to/platform-specific/gardener.md) for integration details.

### GCP

Google Cloud Platform. A major cloud platform supported by Garden Linux through the [`gcp`](https://github.com/gardenlinux/gardenlinux/blob/main/features/gcp/README.md) platform feature with platform-specific configurations. See [GCP platform guide](../how-to/platform-specific/gcp.md) and [GCP first boot tutorial](../tutorials/cloud/first-boot-gcp.md) for usage details.

### GitHub Actions

GitHub's continuous integration and deployment platform. Garden Linux uses GitHub Actions for automated testing and building. See [ADR-0028](./adr/0028-pin-actions-to-sha.md) for the decision to pin GitHub Actions to specific SHA hashes for security and reproducibility.

### GLCI

Garden Linux Continuous Integration. See [ADR-0031](./adr/0031-builder-glci-interface.md) for details on the builder-GLCI interface design.

### GLVD

Garden Linux Vulnerability Database. A system for tracking and managing security vulnerabilities in Garden Linux packages and images.

### Go Dependencies

Garden Linux uses Go for various tools and components. See [ADR-0004](./adr/0004-vendoring-go-dependencies.md) for the decision to vendor Go dependencies.

---

## I

### Image Type

The format and target deployment method for a Garden Linux image, such as cloud images, container images, virtual machine images, or bare-metal images. See [Image Types documentation](../explanation/image-types.md) and [Image Formats reference](./image-formats.md) for detailed information.

### Immutable

Refers to the optional immutable image feature where the root filesystem is read-only to prevent modifications and ensure system integrity.

### initramfs

Initial RAM filesystem. Garden Linux uses dracut to generate the initramfs, which is loaded by the kernel during the boot process before mounting the root filesystem.

---

## K

### Kernel

Garden Linux runs the latest Long Term Support (LTS) kernel from the Linux kernel project, providing up-to-date hardware support and security patches.

### KVM

Kernel-based Virtual Machine. A Linux kernel module that provides hardware virtualization capabilities. The [`kvm`](https://github.com/gardenlinux/gardenlinux/blob/main/features/kvm/README.md) platform feature is a common target for Garden Linux images used in virtualized environments.

---

## L

### Lima (Linux Machines)

A tool for running Linux virtual machines on macOS and Linux hosts. Garden Linux provides official Lima images that can be launched with `limactl`. See [ADR-0023](./adr/0023-lima-image-download.md) for details on Lima image download mechanisms and [ADR-0024](./adr/0024-promote-lima-image-to-official.md) for the decision to promote Lima images to official status. Also see [Lima documentation](https://lima-vm.io) for more details.

### LTS Kernel

Long Term Support kernel. Garden Linux uses LTS kernel versions that receive extended security updates and bug fixes from the Linux kernel maintainers.

---

## M

### Major Version

The first number in Garden Linux's semantic versioning scheme (e.g., the "2017" in "2017.0.0"). Major versions may include breaking changes or significant architectural shifts. See [ADR-0011](./adr/0011-garden-linux-versioning.md) for the complete versioning strategy.

### Metal

See **Bare Metal**.

### Minor Version

The second number in Garden Linux's semantic versioning scheme (e.g., the "0" in "2017.0.0"). Minor versions typically add features or improvements in a backwards-compatible manner. See [ADR-0011](./adr/0011-garden-linux-versioning.md) for details.

---

## N

### Nightly Release

Automated builds of Garden Linux that occur on a regular schedule from the latest development code. Nightly releases are tagged as `nightly` and do not include maintenance commitments or updates. They are intended for testing and feedback, not production use.

---

## O

### OCI

Oracle Cloud Infrastructure. A supported cloud platform for Garden Linux.

### OpenSSL

The cryptographic library used by Garden Linux. Garden Linux uses OpenSSL 3.5 by default.

### OpenStack

An open-source cloud computing platform. Garden Linux provides OpenStack-specific images through the [`openstack`](https://github.com/gardenlinux/gardenlinux/blob/main/features/openstack/README.md) platform feature.

---

## P

### Patch Version

The third number in Garden Linux's semantic versioning scheme (e.g., the "0" in "2017.0.0"). Patch versions contain backwards-compatible bug fixes and security updates. See [ADR-0011](./adr/0011-garden-linux-versioning.md) for details.

### Platform

The target deployment environment for a Garden Linux image. Platforms include cloud providers (AWS, Azure, GCP), virtualization technologies (KVM, VMware), and physical hardware (bare metal). The platform is always the first component in a build flavor string. See [ADR-0020](./adr/0020-enforce-single-platform-by-default-in-builder.md) for details on platform enforcement.

### Podman

A daemonless container engine for developing, managing, and running OCI containers. Garden Linux uses rootless Podman by default for building images, though other container engines can be used with the `--container-engine` flag.

### PR References

Pull Request references in commit messages. See [ADR-0014](./adr/0014-enforce-pr-references-in-commits.md) for the requirement to enforce PR references in commits.

### python-gardenlinux-lib

The [python-gardenlinux-lib](https://github.com/gardenlinux/python-gardenlinux-lib) repository containing Python libraries and utilities for working with Garden Linux. See [ADR-0030](./adr/0030-python-gardenlinux-lib.md) for the architectural decision to create this library.

---

## R

### Release

A stable, versioned distribution of Garden Linux following semantic versioning. Releases are published on [GitHub Releases](https://github.com/gardenlinux/gardenlinux/releases) and GitHub Packages. See [ADR-0011](./adr/0011-garden-linux-versioning.md) for the versioning strategy and [ADR-0015](./adr/0015-no-backports-from-stable.md) for the policy on backports from stable branches.

### Rootless Podman

Running Podman without requiring root privileges. Garden Linux builds use rootless Podman by default, enhancing security by avoiding privileged operations during the build process.

---

## S

### Secure Boot

A security feature that ensures only trusted software can boot on a system by verifying digital signatures. Garden Linux supports Secure Boot through the [`_secureboot`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_secureboot/README.md) feature. See [ADR-0005](./adr/0005-secure-boot-keys-glci.md) for details on Secure Boot keys in GLCI, and the [Secure Boot documentation](../how-to/security/secure-boot.md) for usage details.

### SELinux

Security-Enhanced Linux. An optional security feature available through the [`_selinux`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_selinux/README.md) feature that provides mandatory access control (MAC) security mechanisms. See [ADR-0029](./adr/0029-cis-selinux-permissive.md) for the decision regarding SELinux in permissive mode for CIS compliance.

### Semver

Semantic Versioning. Garden Linux follows the semver specification (MAJOR.MINOR.PATCH) starting with version 2017.0.0. See [ADR-0011](./adr/0011-garden-linux-versioning.md) for the complete versioning strategy and [semver.org](https://semver.org/) for the specification.

### STIG

Security Technical Implementation Guide. Garden Linux provides optional STIG compliance through the [`stig`](https://github.com/gardenlinux/gardenlinux/blob/main/features/stig/README.md) and [`stigDev`](https://github.com/gardenlinux/gardenlinux/blob/main/features/stigDev/README.md) features, based on DISA (Defense Information Systems Agency) security standards.

### systemd

The system and service manager used by Garden Linux. Garden Linux is purely systemd-based, using systemd-networkd for networking, systemd for service management, and other systemd components. See [ADR-0019](./adr/0019-standardize-on-systemd-timers.md) for the decision to standardize on systemd timers, and [ADR-0027](./adr/0027-no-systemd-rc.md) regarding the removal of systemd-rc.

---

## T

### test-ng

The testing framework used by Garden Linux for comprehensive system testing. See [ADR-0006](./adr/0006-new-test-framework-in-place-self-contained-test-execution.md) (new test framework), [ADR-0007](./adr/0007-non-invasive-read-only-testing.md) (non-invasive testing), [ADR-0008](./adr/0008-unified-and-declarative-test-logic.md) (unified test logic), [ADR-0010](./adr/0010-incremental-migration-and-coexistence-of-tests.md) (incremental migration), [ADR-0016](./adr/0016-minimal-host-dependencies-for-test-ng.md) (minimal host dependencies), [ADR-0021](./adr/0021-use-of-tiger-tool-in-tests-ng.md) (tiger tool usage), [ADR-0022](./adr/0022-test-ng-system-state-diffing.md) (system state diffing), and [ADR-0026](./adr/0026-test-ng-when-to-parsers.md) (when-to parsers) for comprehensive details on the test-ng architecture and design decisions.

### TPM2

Trusted Platform Module 2.0. A hardware-based security feature that can be enabled with the [`_tpm2`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_tpm2/README.md) feature for secure key storage and system integrity verification.

### Trusted Boot

An extension to Secure Boot that provides additional system integrity verification throughout the boot process. Garden Linux supports Trusted Boot through the [`_trustedboot`](https://github.com/gardenlinux/gardenlinux/blob/main/features/_trustedboot/README.md) feature.

---

## U

### Unit Tests

Automated tests that validate the correct functionality of a Garden Linux image after it's created. Unit tests verify that the image contains expected packages, configurations, and behaviors. See [ADR-0013](./adr/0013-discontinue-packages-musthave-tests.md) for the decision to discontinue certain package must-have tests, and [ADR-0025](./adr/0025-disable-debsums-tests.md) for the decision to disable debsums tests.

---

## V

### Virtual Machine Image

A Garden Linux image formatted for use with hypervisors like KVM, VMware, or cloud platform virtualization systems.

### VMware

A virtualization platform supported by Garden Linux. Garden Linux provides VMware-specific images through the [`vmware`](https://github.com/gardenlinux/gardenlinux/blob/main/features/vmware/README.md) platform feature, including support for OVA (Open Virtual Appliance) format.
