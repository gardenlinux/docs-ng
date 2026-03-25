---
title: Garden Linux Repository Migration Guide
date: 2026-03-19
---

# Garden Linux Repository - Diátaxis Migration Guide

This document outlines the content migration plan for the **gardenlinux** repository.

## Overview

The gardenlinux repository documentation needs to be reorganized according to the Diátaxis framework on a `docs-ng` branch.

## Current Structure

```
docs/
├── 00_introduction/
│   ├── kernel.md
│   ├── motivation.md
│   ├── package-pipeline.md
│   ├── release.md
│   └── README.md
├── 01_developers/
│   ├── bare_container.md
│   ├── build_image.md
│   ├── build_image_openstack.md
│   ├── build_packages.md
│   ├── contributing.md
│   ├── github_pipelines.md
│   ├── test_image.md
│   ├── vmware-ova.md
│   ├── troubleshooting/
│   │   ├── package-linux/
│   │   │   ├── build-fails-in-binary-phase-c-header-not-found.md
│   │   │   ├── build-fails-in-source-phase-patch-is-rejected.md
│   │   │   └── index.md
│   │   └── index.md
│   └── README.md
├── 02_operators/
│   ├── apt_repo.md
│   ├── gardener-kernel-restart.md
│   ├── lima-vm.md
│   ├── local-k8s-lima.md
│   ├── ssh-hardening.md
│   ├── time-configuration.md
│   ├── deployment/
│   │   ├── aws-secureboot.md
│   │   ├── gcp-secureboot.md
│   │   ├── install-non-default.md
│   │   └── ipxe-install.md
│   └── README.md
├── architecture/
│   └── decisions/ (32 ADR files)
├── boot_modes.md
└── README.md
```

## Target Structure (on docs-ng branch)

```
docs/
├── tutorials/
│   ├── first-boot-aws.md          # NEW - create from scratch
│   ├── first-boot-azure.md        # NEW - create from scratch
│   ├── first-boot-gcp.md          # NEW - create from scratch
│   ├── first-boot-openstack.md    # NEW - create from scratch
│   ├── first-boot-kvm.md          # NEW - create from scratch
│   ├── first-boot-oci.md          # Adapt from 01_developers/bare_container.md
│   ├── first-boot-lima.md         # Adapt from 02_operators/lima-vm.md (tutorial parts)
│   ├── first-boot-bare-metal.md   # Adapt from 02_operators/deployment/ipxe-install.md
│   └── index.md                    # NEW - overview
├── how-to/
│   ├── getting-images.md          # NEW - create from scratch
│   ├── choosing-flavors.md        # NEW - create from scratch
│   ├── initial-configuration.md   # Adapt from 02_operators/deployment/install-non-default.md
│   ├── system-management.md       # Adapt from 02_operators/apt_repo.md
│   ├── platform-specific/
│   │   ├── aws.md                 # Adapt from 02_operators/deployment/aws-secureboot.md
│   │   ├── azure.md               # NEW - create from scratch
│   │   ├── gcp.md                 # Adapt from 02_operators/deployment/gcp-secureboot.md
│   │   ├── openstack.md           # Adapt from 01_developers/build_image_openstack.md
│   │   ├── kvm.md                 # NEW - create from scratch
│   │   ├── oci.md                 # Adapt from 01_developers/bare_container.md
│   │   ├── vmware.md              # Adapt from 01_developers/vmware-ova.md
│   │   ├── bare-metal.md          # Adapt from 02_operators/deployment/ipxe-install.md
│   │   ├── lima.md                # Merge 02_operators/lima-vm.md + local-k8s-lima.md
│   │   ├── gardener.md            # Adapt from 02_operators/gardener-kernel-restart.md
│   │   └── index.md               # NEW - overview
│   ├── security/
│   │   ├── ssh-hardening.md       # Adapt from 02_operators/ssh-hardening.md
│   │   ├── secure-boot.md         # NEW - create from scratch
│   │   ├── time-configuration.md  # Adapt from 02_operators/time-configuration.md
│   │   └── index.md               # NEW - overview
│   ├── customization/
│   │   ├── building-flavors.md    # Adapt from 01_developers/build_image.md
│   │   ├── testing-builds.md      # Adapt from 01_developers/test_image.md
│   │   └── index.md               # NEW - overview
│   ├── troubleshooting/
│   │   ├── package-linux/         # Copy from 01_developers/troubleshooting/package-linux/
│   │   └── index.md               # Adapt from 01_developers/troubleshooting/index.md
│   └── index.md                    # NEW - overview
├── explanation/
│   ├── use-cases.md               # Adapt from 00_introduction/motivation.md
│   ├── flavors-and-features.md    # NEW - create from scratch
│   ├── image-types.md             # Adapt from boot_modes.md (conceptual part)
│   ├── security-posture.md        # NEW - create from scratch
│   ├── release-cadence.md         # Adapt from 00_introduction/release.md (conceptual part)
│   ├── architecture.md            # Merge 00_introduction/kernel.md + package-pipeline.md (conceptual parts)
│   ├── design-decisions.md        # Summarize from architecture/decisions/ (32 ADRs)
│   └── index.md                    # NEW - overview
├── reference/
│   ├── flavor-matrix.md           # NEW - create from scratch
│   ├── platform-compatibility.md  # NEW - create from scratch
│   ├── image-formats.md           # Adapt from boot_modes.md (factual part)
│   ├── kernels-and-modules.md     # Adapt from 00_introduction/kernel.md (factual part)
│   ├── releases/
│   │   ├── maintained-releases.md # Adapt from 00_introduction/release.md (factual part)
│   │   ├── release-notes.md       # NEW - aggregate from GitHub releases
│   │   └── index.md               # NEW - overview
│   └── index.md                    # NEW - overview
└── contributing/
    ├── building-image.md          # Adapt from 01_developers/build_packages.md
    ├── workflow.md                # Merge with 01_developers/github_pipelines.md
    └── index.md                   # Merge with 01_developers/contributing.md
```

## Migration Steps

### 1. Create docs-ng Branch

```bash
cd /path/to/gardenlinux
git checkout -b docs-ng
```

### 2. Content Migration Tasks

#### Migration Tracking System

Each documentation file in the gardenlinux repository's `docs-ng` branch should include migration tracking metadata in its YAML frontmatter. This enables automated progress tracking and stakeholder coordination.

**Frontmatter Fields:**

```yaml
---
title: "Document Title"
# ... other frontmatter fields ...

# Migration tracking fields:
migration_status: "new"                                    # new | adapt | merge | done
migration_source: ""                                       # source file(s) from old structure
migration_issue: ""                                        # GitHub issue reference
migration_stakeholder: "@tmang0ld, @yeoldegrove, @ByteOtter"
migration_approved: false                                  # true when approved
---
```

**Field Definitions:**

| Field | Values | Description |
|-------|--------|-------------|
| `migration_status` | `new` | Content must be written from scratch |
| | `adapt` | Existing content needs rewriting for Diátaxis |
| | `merge` | Multiple source files to be combined |
| | `done` | Migration/writing complete |
| `migration_source` | path(s) | Old file path(s) relative to `docs/`, comma-separated for merges |
| `migration_issue` | string | GitHub issue reference (e.g., `gardenlinux/gardenlinux#42`) |
| `migration_stakeholder` | string | Comma-separated GitHub handles (default: `@tmang0ld, @yeoldegrove, @ByteOtter`) |
| `migration_approved` | boolean | Set to `true` when stakeholder has reviewed and approved |

**Helper Script:** Use `scripts/migration_tracker.py` in the docs-ng repo to generate progress reports from these frontmatter fields.

#### Tutorials (9 files total: 8 new + 1 index)

- [ ] `tutorials/first-boot-aws.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-azure.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-gcp.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-openstack.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-kvm.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-oci.md` — `status:adapt` `source:01_developers/bare_container.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-lima.md` — `status:adapt` `source:02_operators/lima-vm.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/first-boot-bare-metal.md` — `status:adapt` `source:02_operators/deployment/ipxe-install.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `tutorials/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

#### How-To Guides (28 files total: 5 overview + 23 guides)

**Core guides:**
- [ ] `how-to/getting-images.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/choosing-flavors.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/initial-configuration.md` — `status:adapt` `source:02_operators/deployment/install-non-default.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/system-management.md` — `status:adapt` `source:02_operators/apt_repo.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

**Platform-specific guides:**
- [ ] `how-to/platform-specific/aws.md` — `status:adapt` `source:02_operators/deployment/aws-secureboot.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/azure.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/gcp.md` — `status:adapt` `source:02_operators/deployment/gcp-secureboot.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/openstack.md` — `status:adapt` `source:01_developers/build_image_openstack.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/kvm.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/oci.md` — `status:adapt` `source:01_developers/bare_container.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/vmware.md` — `status:adapt` `source:01_developers/vmware-ova.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/bare-metal.md` — `status:adapt` `source:02_operators/deployment/ipxe-install.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/lima.md` — `status:merge` `source:02_operators/lima-vm.md,02_operators/local-k8s-lima.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/gardener.md` — `status:adapt` `source:02_operators/gardener-kernel-restart.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/platform-specific/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

**Security guides:**
- [ ] `how-to/security/ssh-hardening.md` — `status:adapt` `source:02_operators/ssh-hardening.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/security/secure-boot.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/security/time-configuration.md` — `status:adapt` `source:02_operators/time-configuration.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/security/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

**Customization guides:**
- [ ] `how-to/customization/building-flavors.md` — `status:adapt` `source:01_developers/build_image.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/customization/testing-builds.md` — `status:adapt` `source:01_developers/test_image.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `how-to/customization/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

**Troubleshooting:**
- [ ] `how-to/troubleshooting/index.md` — `status:adapt` `source:01_developers/troubleshooting/index.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

#### Explanation (8 files total: 7 guides + 1 index)

- [ ] `explanation/use-cases.md` — `status:adapt` `source:00_introduction/motivation.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/flavors-and-features.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/image-types.md` — `status:adapt` `source:boot_modes.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/security-posture.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/release-cadence.md` — `status:adapt` `source:00_introduction/release.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/architecture.md` — `status:merge` `source:00_introduction/kernel.md,00_introduction/package-pipeline.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/design-decisions.md` — `status:adapt` `source:architecture/decisions/` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `explanation/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

#### Reference (10 files total: 4 main + 3 releases + 3 indexes)

- [ ] `reference/flavor-matrix.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/platform-compatibility.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/image-formats.md` — `status:adapt` `source:boot_modes.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/kernels-and-modules.md` — `status:adapt` `source:00_introduction/kernel.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/releases/maintained-releases.md` — `status:adapt` `source:00_introduction/release.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/releases/release-notes.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/releases/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `reference/index.md` — `status:new` `source:` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

#### Contributing (3 files total)

- [ ] `contributing/building-image.md` — `status:adapt` `source:01_developers/build_packages.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `contributing/workflow.md` — `status:merge` `source:01_developers/github_pipelines.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`
- [ ] `contributing/index.md` — `status:merge` `source:01_developers/contributing.md,01_developers/README.md` `issue:` `stakeholder:@tmang0ld,@yeoldegrove,@ByteOtter` `approved:false`

### 3. Step-by-Step Migration Instructions

#### Phase 1: Setup (Day 1)

1. **Create the docs-ng branch in gardenlinux repo:**
   ```bash
   cd /home/yeoldegrove/kunden/SAP/gardenlinux/gardenlinux
   git checkout main
   git pull
   git checkout -b docs-ng
   ```

2. **Create directory structure:**
   ```bash
   cd docs
   mkdir -p tutorials
   mkdir -p how-to/{platform-specific,security,customization,troubleshooting}
   mkdir -p explanation
   mkdir -p reference/releases
   mkdir -p contributing
   ```

3. **Copy troubleshooting content as-is:**
   ```bash
   cp -r 01_developers/troubleshooting/package-linux how-to/troubleshooting/
   ```

4. **Preserve .media directory:**
   ```bash
   # .media directory should remain at docs/.media for proper image linking
   ```

#### Phase 2: Migrate Contributing Section (Day 1-2)

Priority: High - Developers need this first

1. **contributing/index.md** - Merge:
   - `01_developers/contributing.md` (main content)
   - `01_developers/README.md` (overview parts)

2. **contributing/building-image.md** - Adapt:
   - `01_developers/build_packages.md` (main content)
   - Add cross-references to how-to guides

3. **contributing/workflow.md** - Merge:
   - `01_developers/github_pipelines.md`
   - Add information about development workflow

#### Phase 3: Migrate Reference Section (Day 2-3)

Priority: High - Users need factual information

1. **reference/image-formats.md** - Extract from `boot_modes.md`:
   - Focus on factual specifications (file formats, structure)
   - Remove conceptual explanations (move to explanation/)

2. **reference/kernels-and-modules.md** - Extract from `00_introduction/kernel.md`:
   - List of supported kernels
   - Module information
   - Remove architecture explanations (move to explanation/)

3. **reference/releases/maintained-releases.md** - Extract from `00_introduction/release.md`:
   - Current maintained versions
   - Support timelines
   - Remove process explanations (move to explanation/)

4. **Create new reference files:**
   - `reference/flavor-matrix.md` - Comprehensive table of all flavors
   - `reference/platform-compatibility.md` - Platform support matrix
   - `reference/releases/release-notes.md` - Aggregate from GitHub

5. **Create index files:**
   - `reference/index.md`
   - `reference/releases/index.md`

#### Phase 4: Migrate Explanation Section (Day 3-4)

Priority: Medium - Conceptual understanding

1. **explanation/use-cases.md** - Adapt from `00_introduction/motivation.md`:
   - Explain WHY Garden Linux exists
   - Use cases and scenarios

2. **explanation/image-types.md** - Extract from `boot_modes.md`:
   - Conceptual explanation of different boot modes
   - When to use each type

3. **explanation/architecture.md** - Merge:
   - `00_introduction/kernel.md` (conceptual parts)
   - `00_introduction/package-pipeline.md` (conceptual parts)
   - High-level architecture overview

4. **explanation/release-cadence.md** - Extract from `00_introduction/release.md`:
   - Explain release philosophy
   - Update cadence reasoning

5. **explanation/design-decisions.md** - Summarize ADRs:
   - Create index of `architecture/decisions/` (32 ADRs)
   - Link to original ADRs (keep them in place)
   - Provide high-level summary

6. **Create new explanation files:**
   - `explanation/flavors-and-features.md` - Explain flavor system
   - `explanation/security-posture.md` - Security philosophy
   - `explanation/index.md` - Overview

#### Phase 5: Migrate How-To Guides (Day 4-6)

Priority: High - Users need practical guidance

1. **Core how-to guides:**
   - `how-to/getting-images.md` - NEW (download locations, verification)
   - `how-to/choosing-flavors.md` - NEW (selection criteria)
   - `how-to/initial-configuration.md` - From `02_operators/deployment/install-non-default.md`
   - `how-to/system-management.md` - From `02_operators/apt_repo.md`

2. **Platform-specific guides:**
   - `how-to/platform-specific/aws.md` - From `02_operators/deployment/aws-secureboot.md`
   - `how-to/platform-specific/gcp.md` - From `02_operators/deployment/gcp-secureboot.md`
   - `how-to/platform-specific/openstack.md` - From `01_developers/build_image_openstack.md`
   - `how-to/platform-specific/vmware.md` - From `01_developers/vmware-ova.md`
   - `how-to/platform-specific/oci.md` - From `01_developers/bare_container.md` (how-to parts)
   - `how-to/platform-specific/bare-metal.md` - From `02_operators/deployment/ipxe-install.md` (how-to parts)
   - `how-to/platform-specific/lima.md` - Merge `02_operators/lima-vm.md` + `local-k8s-lima.md`
   - `how-to/platform-specific/gardener.md` - From `02_operators/gardener-kernel-restart.md`

3. **New platform guides:**
   - `how-to/platform-specific/azure.md` - Create from scratch
   - `how-to/platform-specific/kvm.md` - Create from scratch

4. **Security guides:**
   - `how-to/security/ssh-hardening.md` - From `02_operators/ssh-hardening.md`
   - `how-to/security/time-configuration.md` - From `02_operators/time-configuration.md`
   - `how-to/security/secure-boot.md` - NEW (consolidate secure boot info)

5. **Customization guides:**
   - `how-to/customization/building-flavors.md` - From `01_developers/build_image.md`
   - `how-to/customization/testing-builds.md` - From `01_developers/test_image.md`

6. **Troubleshooting:**
   - `how-to/troubleshooting/index.md` - From `01_developers/troubleshooting/index.md`
   - Already copied: `how-to/troubleshooting/package-linux/`

7. **Create index files:**
   - `how-to/index.md`
   - `how-to/platform-specific/index.md`
   - `how-to/security/index.md`
   - `how-to/customization/index.md`

#### Phase 6: Create Tutorials (Day 6-8)

Priority: Medium-High - Important for new users

1. **Platform-specific tutorials:**
   - `tutorials/first-boot-aws.md` - NEW
   - `tutorials/first-boot-azure.md` - NEW
   - `tutorials/first-boot-gcp.md` - NEW
   - `tutorials/first-boot-openstack.md` - NEW
   - `tutorials/first-boot-kvm.md` - NEW

2. **Adapt existing content:**
   - `tutorials/first-boot-oci.md` - From `01_developers/bare_container.md` (tutorial parts)
   - `tutorials/first-boot-lima.md` - From `02_operators/lima-vm.md` (tutorial parts)
   - `tutorials/first-boot-bare-metal.md` - From `02_operators/deployment/ipxe-install.md` (tutorial parts)

3. **Create index:**
   - `tutorials/index.md` - Overview of all tutorials

#### Phase 7: Clean Up Old Structure (Day 8)

**DO NOT delete old files immediately - keep them for reference during aggregator updates**

1. Mark old directories as deprecated by adding README files:
   ```bash
   echo "# Deprecated - See docs/tutorials/, docs/how-to/, etc." > 00_introduction/DEPRECATED.md
   echo "# Deprecated - See docs/how-to/customization/" > 01_developers/DEPRECATED.md
   echo "# Deprecated - See docs/how-to/platform-specific/" > 02_operators/DEPRECATED.md
   ```

2. Keep original files until aggregator is updated and tested

### 4. Writing Style Guide by Category

#### Tutorials

**Purpose:** Learning-oriented, step-by-step lessons for beginners

**Style guidelines:**
- Use second person ("you will", "your system")
- Start with clear learning objectives
- Provide complete, concrete steps
- Include expected output/results
- No branching paths - one clear path to success
- Test all steps before publishing
- Include prerequisites section
- End with "What's next?" suggestions

**Template structure:**
```markdown
# Tutorial Title (e.g., "First Boot on AWS")

## What You'll Learn

In this tutorial, you will learn how to:
- Point 1
- Point 2
- Point 3

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## Step 1: [Action]

Detailed instructions...

Expected result: ...

## Step 2: [Action]

Detailed instructions...

Expected result: ...

## Conclusion

You have successfully...

## What's Next?

- Link to related how-to guide
- Link to explanation topic
```

#### How-To Guides

**Purpose:** Problem-oriented, practical step-by-step guides

**Style guidelines:**
- Assume some basic knowledge
- Focus on solving specific problems
- Start with the goal/problem statement
- Provide clear, numbered steps
- Include alternatives and options when relevant
- Add troubleshooting tips
- Can include multiple paths/variations
- Link to reference docs and explanations

**Template structure:**
```markdown
# How to [Achieve Goal]

## Overview

Brief description of what this guide covers and when to use it.

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## Steps

### Step 1: [Action]

Instructions...

### Step 2: [Action]

Instructions...

**Note:** Optional variation or alternative approach.

## Troubleshooting

- **Problem:** Description
  **Solution:** How to fix

## Related Guides

- Link to related how-to
- Link to reference
- Link to explanation
```

#### Explanation

**Purpose:** Understanding-oriented, conceptual clarification

**Style guidelines:**
- Focus on understanding WHY, not HOW
- Provide context and background
- Explain design decisions and trade-offs
- Use diagrams where helpful
- Connect concepts to real-world scenarios
- No step-by-step instructions
- Link to tutorials and how-tos for practical application
- Be comprehensive but avoid excessive detail

**Template structure:**
```markdown
# [Concept] Explained

## Introduction

High-level overview of the concept.

## Background

Historical context, motivation, why this exists.

## Key Concepts

### Concept 1

Explanation...

### Concept 2

Explanation...

## Design Decisions

Why things work the way they do...

## Trade-offs

Advantages and disadvantages...

## Real-World Applications

How this applies in practice...

## Further Reading

- Link to related explanations
- Link to how-to guides
- Link to reference docs
```

#### Reference

**Purpose:** Information-oriented, factual descriptions

**Style guidelines:**
- Be precise and accurate
- Use tables, lists, and structured formats
- No explanations of WHY (link to explanation docs)
- No instructions on HOW (link to how-to docs)
- Keep it dry and factual
- Organize for easy lookup
- Include all technical specifications
- Use consistent formatting

**Template structure:**
```markdown
# [Topic] Reference

## Overview Table

| Item | Value | Notes |
|------|-------|-------|
| ... | ... | ... |

## Details

### Item 1

**Specification:** Value
**Supported versions:** X.Y.Z
**Format:** Description

### Item 2

**Specification:** Value
**Supported versions:** X.Y.Z
**Format:** Description

## See Also

- Link to explanation
- Link to how-to guide
```

#### Contributing

**Purpose:** Contributor-oriented, development workflow

**Style guidelines:**
- Assume developer audience
- Be specific about tools and processes
- Include code style guidelines
- Explain testing requirements
- Describe review process
- Link to external resources (Git, GitHub, etc.)
- Keep community guidelines clear and welcoming

### 5. Final Step: Adapt Aggregator Mechanism

After the content migration is complete in the gardenlinux repository's `docs-ng` branch, the aggregator in the docs-ng repo must be updated to work with the new Diátaxis structure.

#### 5.1 Update repos-config.json

**Location:** `scripts/repos-config.json` in docs-ng repo

**Changes needed:**

1. **Switch branch from `main` to `docs-ng`:**
   ```json
   {
     "repos": [
       {
         "name": "gardenlinux",
         "url": "https://github.com/gardenlinux/gardenlinux",
         "docs_path": "docs",
         "branch": "docs-ng",  // Changed from "main"
         ...
       }
     ]
   }
   ```

2. **Update structure mapping** to use Diátaxis categories:
   ```json
   {
     "repos": [
       {
         "name": "gardenlinux",
         "structure": {
           "tutorials": "tutorials",
           "how-to": "how-to",
           "explanation": "explanation",
           "reference": "reference",
           "contributing": "contributing"
         },
         "special_files": {},
         "media_directories": [".media"]
       }
     ]
   }
   ```

3. **Update section priorities** for Diátaxis categories:
   ```json
   {
     "section_priorities": {
       "gardenlinux": -1,
       "readme": -1,
       "index": -1,
       "tutorials": 0,
       "how-to": 1,
       "explanation": 2,
       "reference": 3,
       "contributing": 4
     }
   }
   ```

4. **Update target_path** to organize by category:
   ```json
   {
     "repos": [
       {
         "name": "gardenlinux",
         "target_path": "projects/gardenlinux",
         ...
       }
     ]
   }
   ```

#### 5.2 Update transform_content.py

**Location:** `scripts/transform_content.py` in docs-ng repo

**Changes needed:**

1. **Update directory transformation logic:**
   - The current logic removes numbered prefixes (`00_`, `01_`, `02_`)
   - New structure doesn't have numbered prefixes
   - Simplify to direct mapping without number removal

2. **Add support for nested Diátaxis structure:**
   ```python
   # In transform_directory_structure function
   diataxis_categories = ['tutorials', 'how-to', 'explanation', 'reference', 'contributing']
   
   for category in diataxis_categories:
       source_cat = source_path / category
       if source_cat.exists():
           target_cat = target_path / category
           shutil.copytree(source_cat, target_cat, dirs_exist_ok=True)
   ```

3. **Update link rewriting** to handle Diátaxis paths:
   - Links within the same category should resolve correctly
   - Cross-category links should work (e.g., tutorial → how-to)
   - The existing logic should mostly work, but test thoroughly

#### 5.3 Sidebar Configuration

**Note:** Sidebar is now automatically generated by `vitepress-sidebar` library

**Changes needed:**

1. **Update section priority handling** for Diátaxis:
   ```python
   def get_section_priority(section, priority_map):
       section_name = section.get("text", "").lower()
       
       # Direct category matches
       diataxis_priorities = {
           "tutorials": 0,
           "how-to": 1,
           "explanation": 2,
           "reference": 3,
           "contributing": 4
       }
       
       for category, priority in diataxis_priorities.items():
           if category in section_name:
               return priority
       
       # Fallback to configured priorities
       for key, priority in priority_map.items():
           if key in section_name:
               return priority
       
       return 999
   ```

2. **Update sidebar generation** to recognize Diátaxis categories:
   - Each category becomes a collapsible section
   - Maintain proper nesting for subcategories (e.g., how-to/platform-specific)

3. **Update nav generation** to highlight key entry points:
   - Tutorials as primary entry for new users
   - How-to guides for common tasks
   - Reference for lookups

#### 5.4 Update VitePress config.mts

**Location:** `docs/.vitepress/config.mts` in docs-ng repo

**Changes needed:**

1. **Review sidebar structure** - The `vitepress-sidebar` library handles this automatically, but verify:
   - Diátaxis categories appear in correct order
   - Subcategories (e.g., how-to/platform-specific) are properly nested
   - Index pages link correctly

2. **Update nav items** - Ensure prominent placement of:
   - Tutorials for new users
   - How-to guides dropdown
   - Quick links to key platforms

3. **Test the configuration:**
   ```bash
   cd /home/yeoldegrove/kunden/SAP/gardenlinux/docs-ng
   make dev
   # Open browser and verify navigation structure
   ```

#### 5.5 Testing the Aggregator

**Complete testing workflow:**

1. **Test with local config first:**
   ```bash
   cd /home/yeoldegrove/kunden/SAP/gardenlinux/docs-ng
   
   # Use local config pointing to local gardenlinux repo
   cp scripts/repos-config.json scripts/repos-config.backup.json
   cp scripts/repos-config.local.json scripts/repos-config.json
   
   # Update local config to point to docs-ng branch
   # Edit scripts/repos-config.json and change branch to "docs-ng"
   ```

2. **Run aggregation:**
   ```bash
   make aggregate
   ```

3. **Check for errors:**
   - Review console output for transformation warnings
   - Check that all Diátaxis categories were copied
   - Verify .media directory was preserved

4. **Verify generated structure:**
   ```bash
   tree docs/projects/gardenlinux -L 2
   ```

   Expected output:
   ```
   docs/projects/gardenlinux/
   ├── tutorials/
   ├── how-to/
   │   ├── platform-specific/
   │   ├── security/
   │   ├── customization/
   │   └── troubleshooting/
   ├── explanation/
   ├── reference/
   │   └── releases/
   ├── contributing/
   └── .media/
   ```

5. **Test the site locally:**
   ```bash
   make dev
   ```

6. **Manual verification checklist:**
   - [ ] All Diátaxis categories appear in sidebar
   - [ ] Navigation links work correctly
   - [ ] Images load properly (.media links)
   - [ ] Internal links resolve correctly
   - [ ] Cross-category links work (tutorial → how-to)
   - [ ] Index pages display correctly
   - [ ] Search functionality works

7. **Test build:**
   ```bash
   make build
   ```

#### 5.6 Rollout Plan

**Phased rollout approach:**

**Phase 1: Documentation Migration (In gardenlinux repo)**
- Complete content migration on `docs-ng` branch
- Get review from team members
- Test locally with aggregator

**Phase 2: Aggregator Update (In docs-ng repo)**
- Update aggregator scripts for Diátaxis
- Test with local gardenlinux repo
- Verify all functionality works

**Phase 3: Integration Testing**
- Push `docs-ng` branch to GitHub
- Update docs-ng repo to fetch from `docs-ng` branch
- Run full aggregation and build
- Deploy to staging environment

**Phase 4: Production Deployment**
- Merge `docs-ng` branch to `main` in gardenlinux repo
- Update docs-ng repo to use `main` branch
- Deploy to production

**Phase 5: Cleanup**
- Archive old documentation structure
- Update any external links
- Announce new structure to users

### 6. Summary

**Total file count for migration:**
- Tutorials: 9 files (6 new, 3 adapted)
- How-to: 28 files (8 new, 20 adapted)
- Explanation: 8 files (3 new, 4 adapted, 1 summary)
- Reference: 10 files (4 new, 4 adapted, 2 indexes)
- Contributing: 3 files (all adapted/merged)

**Total: 58 files**

**Key success factors:**
1. Follow Diátaxis principles strictly for each category
2. Maintain consistent formatting and structure
3. Test all internal links and media references
4. Ensure aggregator correctly handles new structure
5. Get team review before finalizing
6. Document any deviations from plan

**Post-migration tasks:**
1. Apply same approach to `builder` and `python-gardenlinux-lib` repos
2. Update docs-ng placeholder files with aggregated content
3. Remove TODO markers as content is completed
4. Continuously improve based on user feedback
