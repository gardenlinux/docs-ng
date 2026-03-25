# Phase 2: Content Migration - Detailed Implementation Plan

## Executive Summary

This document provides detailed, actionable steps for implementing Phase 2 of the Garden Linux documentation reorganization. Phase 2 focuses on migrating existing content from the aggregated `docs/projects/` directory to the new Diátaxis-based structure.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Content Audit](#content-audit)
4. [Detailed Content Mapping](#detailed-content-mapping)
5. [Content Transformation Guidelines](#content-transformation-guidelines)
6. [Script Modifications](#script-modifications)
7. [Migration Workflow](#migration-workflow)
8. [Quality Assurance](#quality-assurance)
9. [Implementation Checklist](#implementation-checklist)

## Overview

Phase 2 of the Garden Linux documentation reorganization focuses on **Content Migration** - moving existing documentation from the aggregated `docs/projects/` structure to the new Diátaxis-based organization.

### Current State

**Aggregated Content Location**: `docs/projects/`
- `gardenlinux/` - Main Garden Linux documentation (introduction, developers, operators)
- `builder/` - Builder tool documentation
- `python-gardenlinux-lib/` - Python library documentation (Sphinx/RST format)

**Target Structure**: Diátaxis framework
- `docs/tutorials/` - Learning-oriented guides
- `docs/how-to/` - Task-oriented guides
- `docs/explanation/` - Understanding-oriented content
- `docs/reference/` - Information-oriented specifications
- `docs/contributing/` - Contribution guidelines

### Goals

1. **Systematically audit** all existing aggregated content (59 files identified)
2. **Categorize each document** according to Diátaxis content types
3. **Transform and migrate** content to appropriate new locations
4. **Establish cross-references** between old and new locations during transition
5. **Update internal links** to point to new structure
6. **Maintain content quality** while adapting writing style to match content type

### Non-Goals

- Creating new content (Phase 3)
- Removing legacy content (Phase 4)
- Major content rewrites (minor adaptations only)

## Prerequisites

Before starting Phase 2 migration, ensure:

### Technical Requirements

1. **Access to repositories**:
   - `gardenlinux/gardenlinux` - main repository
   - `gardenlinux/builder` - builder documentation
   - `gardenlinux/python-gardenlinux-lib` - Python library documentation

2. **Local environment**:
   - Python 3.x installed
   - Git access configured
   - VitePress development environment (Node.js, npm/pnpm)

3. **Completed Phase 1 tasks**:
   - ✅ New folder structure created (`docs/tutorials/`, `docs/how-to/`, `docs/explanation/`, `docs/reference/`)
   - ✅ Placeholder README files in each section
   - ✅ Navigation and sidebar configuration updated
   - ✅ Legacy directory structure established (`docs/legacy/`)

### Knowledge Requirements

1. **Diátaxis Framework Understanding**:
   - Tutorials: Learning-oriented, step-by-step, beginner-friendly
   - How-to: Task-oriented, problem-solving, goal-focused
   - Explanation: Understanding-oriented, conceptual, discursive
   - Reference: Information-oriented, accurate, lookup-focused

2. **Garden Linux Domain Knowledge**:
   - Understanding of flavors, features, and build system
   - Platform deployment knowledge (AWS, Azure, GCP, etc.)
   - Security concepts and hardening practices

3. **Documentation Standards**:
   - Markdown syntax and VitePress conventions
   - Frontmatter structure and metadata
   - Link rewriting and cross-referencing

## Content Audit

Based on analysis of `docs/projects/`, we have identified the following content to migrate:

### gardenlinux/introduction/ (6 files + 32 ADRs)

| File | Type | Size | Target Category |
|------|------|------|-----------------|
| `motivation.md` | Conceptual | Medium | Explanation (use-cases.md) |
| `kernel.md` | Mixed | Medium | Explanation (architecture.md) + Reference (kernels-and-modules.md) |
| `package-pipeline.md` | Conceptual | Medium | Explanation (architecture.md) |
| `release.md` | Mixed | Large | Explanation (release-cadence.md) + Reference (releases/) |
| `boot_modes.md` | Mixed | Medium | Explanation (image-types.md) + Reference (image-formats.md) |
| `architecture/decisions/*.md` | Reference | 32 files | Explanation (design-decisions.md - summarized) |

**Priority**: High (foundational concepts)

### gardenlinux/developers/ (8 files + troubleshooting)

| File | Type | Size | Target Category |
|------|------|------|-----------------|
| `build_image.md` | Task-oriented | Large | How-to (customization/building-flavors.md) |
| `build_image_openstack.md` | Task-oriented | Medium | How-to (platform-specific/openstack.md) |
| `build_packages.md` | Developer-focused | Medium | Contributing (building-image.md) |
| `test_image.md` | Task-oriented | Medium | How-to (customization/testing-builds.md) |
| `contributing.md` | Process | Medium | Contributing (README.md) |
| `bare_container.md` | Task-oriented | Medium | How-to (platform-specific/oci.md) |
| `github_pipelines.md` | Developer-focused | Medium | Contributing (workflow.md) |
| `vmware-ova.md` | Task-oriented | Small | How-to (platform-specific/vmware.md) |
| `troubleshooting/` | Mixed | 3 files | How-to (troubleshooting/) |

**Priority**: High (practical usage)

### gardenlinux/operators/ (7 files + 5 deployment guides)

| File | Type | Size | Target Category |
|------|------|------|-----------------|
| `apt_repo.md` | Task-oriented | Medium | How-to (system-management.md) |
| `ssh-hardening.md` | Security guide | Large | How-to (security/ssh-hardening.md) |
| `time-configuration.md` | Task-oriented | Medium | How-to (security/time-configuration.md) |
| `gardener-kernel-restart.md` | Task-oriented | Small | How-to (platform-specific/gardener.md) |
| `lima-vm.md` | Tutorial-like | Medium | Tutorials (first-boot-lima.md) + How-to (platform-specific/lima.md) |
| `local-k8s-lima.md` | Tutorial-like | Medium | How-to (platform-specific/lima.md) |
| `deployment/*.md` | Mixed | 5 files | How-to (platform-specific/) |

**Priority**: High (operational tasks)

### builder/ (2 files)

| File | Type | Size | Target Category |
|------|------|------|-----------------|
| `features.md` | Reference | Medium | Reference (feature-glossary.md) |
| `getting_started.md` | Mixed | Medium | How-to (customization/) + Contributing |

**Priority**: Medium (developer-focused)

### python-gardenlinux-lib/ (Sphinx/RST)

| File | Type | Size | Target Category |
|------|------|------|-----------------|
| `index.rst` | Overview | Small | Reference (api/) |
| `api.rst` | API docs | Large | Reference (api/) |
| `cli.rst` | CLI docs | Medium | Reference (api/) |
| `release.rst` | Release info | Small | Reference (releases/) |

**Priority**: Low (specialized audience, needs RST → Markdown conversion)

### Total Content Inventory

- **59 markdown files** (excluding ADRs as individual files)
- **32 Architecture Decision Records** (to be summarized)
- **4 RST files** (require conversion)
- **Estimated migration effort**: 40-60 hours

## Detailed Content Mapping

This section provides specific migration instructions for each source file to its target location(s).

### Introduction → Explanation & Reference

#### 1. motivation.md → explanation/use-cases.md

**Action**: Copy and adapt  
**Transformation**:
- Add section on SAP Gardener as primary use case
- Expand container use cases
- Rewrite from "why we built this" to "why you should use this"
- Add cross-references to tutorials and how-to guides

**Writing Style**: Discursive, persuasive, user-focused

#### 2. kernel.md → Split into TWO files

**Target 1**: `explanation/architecture.md` (conceptual part)
- Extract: Kernel philosophy, why specific versions chosen
- Add: High-level system architecture diagrams
- Style: Conceptual understanding

**Target 2**: `reference/kernels-and-modules.md` (factual part)
- Extract: Kernel versions table, module lists
- Add: Support matrix, compatibility information
- Style: Lookup reference, tables

#### 3. package-pipeline.md → explanation/architecture.md

**Action**: Merge with kernel architecture content  
**Transformation**:
- Explain package build process conceptually
- Describe repository structure
- Link to contributing guides for developers

#### 4. release.md → Split into TWO files

**Target 1**: `explanation/release-cadence.md` (conceptual)
- Release philosophy and lifecycle
- Maintenance windows explanation
- Update strategy discussion

**Target 2**: `reference/releases/maintained-releases.md` (factual)
- Table of current releases
- Support dates and status
- EOL information

#### 5. boot_modes.md → Split into TWO files

**Target 1**: `explanation/image-types.md` (conceptual)
- What are different boot modes?
- When to use each type
- Platform considerations

**Target 2**: `reference/image-formats.md` (factual)
- Image format specifications
- File naming conventions
- Technical details table

#### 6. architecture/decisions/*.md → explanation/design-decisions.md

**Action**: Summarize 32 ADRs into single document  
**Transformation**:
- Create categorized summary (not full copy)
- Group by theme: Security, Build System, Testing, Features
- Link to full ADRs in GitHub for details
- Highlight key decisions that affect users

### Developers → How-to & Contributing

#### 7. build_image.md → how-to/customization/building-flavors.md

**Action**: Copy and adapt  
**Transformation**:
- Focus on task completion
- Add clear prerequisites
- Step-by-step instructions
- Add troubleshooting section
- Link to tutorials for beginners

#### 8. build_image_openstack.md → how-to/platform-specific/openstack.md

**Action**: Copy and adapt  
**Transformation**:
- Platform-specific deployment instructions
- Include OpenStack CLI commands
- Add common issues and solutions

#### 9. build_packages.md → contributing/building-image.md

**Action**: Move to contributing  
**Transformation**:
- Developer-focused workflow
- Package build process
- Testing locally

#### 10. test_image.md → how-to/customization/testing-builds.md

**Action**: Copy and adapt  
**Transformation**:
- Testing methodologies
- Test environments (chroot, QEMU, cloud)
- CI/CD integration

#### 11. contributing.md → contributing/README.md

**Action**: Merge with existing contributing/README.md  
**Transformation**:
- Combine both sources
- Add links to specific contribution guides
- Code of conduct, PR process

#### 12. bare_container.md → how-to/platform-specific/oci.md

**Action**: Copy and adapt  
**Transformation**:
- OCI/Container deployment guide
- Docker/Podman examples
- Registry publishing

#### 13. github_pipelines.md → contributing/workflow.md

**Action**: Merge with existing workflow.md  
**Transformation**:
- GitHub Actions workflows
- CI/CD pipeline explanation
- Automated testing

#### 14. vmware-ova.md → how-to/platform-specific/vmware.md

**Action**: Copy and create new file  
**Transformation**:
- VMware deployment guide
- OVA format specifics

#### 15. troubleshooting/* → how-to/troubleshooting/

**Action**: Copy directory structure  
**Transformation**:
- Maintain troubleshooting organization
- Add index for navigation
- Cross-reference with related how-tos

### Operators → How-to & Tutorials

#### 16. apt_repo.md → how-to/system-management.md

**Action**: Merge into system management  
**Transformation**:
- APT repository configuration
- Package updates
- System maintenance tasks

#### 17. ssh-hardening.md → how-to/security/ssh-hardening.md

**Action**: Direct copy with minimal changes  
**Transformation**:
- Already well-structured as how-to
- Add prerequisites
- Link to security explanation

#### 18. time-configuration.md → how-to/security/time-configuration.md

**Action**: Direct copy  
**Transformation**:
- Time sync configuration
- NTP setup
- Security considerations

#### 19. gardener-kernel-restart.md → how-to/platform-specific/gardener.md

**Action**: Copy and expand  
**Transformation**:
- Gardener-specific operations
- Kernel restart procedures
- Node management

#### 20. lima-vm.md → Split into TWO uses

**Target 1**: `tutorials/first-boot-lima.md` (tutorial)
- Step-by-step first boot
- Complete beginner walkthrough

**Target 2**: `how-to/platform-specific/lima.md` (how-to)
- Advanced Lima operations
- Configuration options

#### 21. local-k8s-lima.md → Merge into how-to/platform-specific/lima.md

**Action**: Combine with lima.md how-to  
**Transformation**:
- K8s deployment on Lima
- Local development environment

#### 22. deployment/*.md → how-to/platform-specific/

**Files**:
- `aws-secureboot.md` → `how-to/platform-specific/aws.md`
- `gcp-secureboot.md` → `how-to/platform-specific/gcp.md`
- `install-non-default.md` → `how-to/initial-configuration.md`
- `ipxe-install.md` → `how-to/platform-specific/bare-metal.md`
- `index.md` → Remove (navigation only)

**Transformation**: Platform-specific deployment guides

### Builder → Reference & How-to

#### 23. features.md → reference/feature-glossary.md

**Action**: Copy and restructure  
**Transformation**:
- Alphabetized feature list
- Clear descriptions
- Cross-references to how-tos

#### 24. getting_started.md → Split

**Target 1**: `how-to/customization/building-features.md`
**Target 2**: Reference in `contributing/`

### Python Library → Reference (Low Priority)

#### 25. Python library docs → reference/api/

**Action**: Convert RST to Markdown  
**Tool**: `pandoc` or manual conversion  
**Priority**: Phase 3 (not critical for Phase 2)

## Content Transformation Guidelines

When migrating content, apply these transformation rules based on the target Diátaxis category:

### Writing Style by Content Type

#### Tutorials (Learning-oriented)
**Voice**: Conversational, encouraging, supportive  
**Tense**: Present tense, second person ("you will...")  
**Structure**:
- Clear learning objective at the start
- Numbered steps (1, 2, 3...)
- Complete commands (copy-pasteable)
- Expected output shown
- Success criteria at the end

**Example Transformation**:
```
BEFORE (technical): "Garden Linux can be deployed on Lima using lima.yaml"
AFTER (tutorial): "Let's deploy your first Garden Linux instance on Lima. By the end of this tutorial, you'll have a running Garden Linux VM on your local machine."
```

#### How-to Guides (Task-oriented)
**Voice**: Direct, professional, efficient  
**Tense**: Imperative mood ("Configure...", "Set...", "Run...")  
**Structure**:
- Clear goal/problem statement
- Prerequisites section
- Step-by-step instructions
- Variations and options
- Troubleshooting tips

**Example Transformation**:
```
BEFORE (explanatory): "SSH hardening involves several configuration parameters..."
AFTER (how-to): "Configure SSH hardening: 1. Edit /etc/ssh/sshd_config, 2. Set PermitRootLogin to no..."
```

#### Explanation (Understanding-oriented)
**Voice**: Discursive, thoughtful, contextual  
**Tense**: Present tense, third person or first person plural ("we", "it")  
**Structure**:
- Introduce concept
- Provide context and background
- Explain relationships
- Discuss alternatives
- No step-by-step instructions

**Example Transformation**:
```
BEFORE (task-focused): "To build an image, run ./build.sh"
AFTER (explanation): "Garden Linux uses a modular build system based on features. Each feature represents a specific capability or configuration that can be combined to create customized images for different use cases."
```

#### Reference (Information-oriented)
**Voice**: Neutral, factual, concise  
**Tense**: Present tense, declarative  
**Structure**:
- Consistent format across entries
- Tables and lists
- Complete and accurate
- Minimal explanation
- Easy to scan

**Example Transformation**:
```
BEFORE (narrative): "Garden Linux supports several cloud platforms including AWS, Azure, and GCP, each with different features..."
AFTER (reference): 
| Platform | Supported | Secure Boot | Features |
|----------|-----------|-------------|----------|
| AWS      | Yes       | Yes         | server, cloud, _aws |
| Azure    | Yes       | Yes         | server, cloud, _azure |
| GCP      | Yes       | Yes         | server, cloud, _gcp |
```

### Frontmatter Standards

Every migrated file must have proper frontmatter:

```yaml
---
title: "Clear, Descriptive Title"
description: "One-sentence description of what this document covers"
category: "tutorials|how-to|explanation|reference|contributing"
tags: ["tag1", "tag2"]
---
```

### Link Transformation Rules

1. **Internal links**: Update to new structure
   ```
   BEFORE: [build guide](/projects/gardenlinux/developers/build_image)
   AFTER: [build guide](/how-to/customization/building-flavors)
   ```

2. **Cross-references**: Add navigation hints
   ```
   "For background on this topic, see [Flavors and Features](/explanation/flavors-and-features).
   To build your first image, follow the [Building Flavors tutorial](/tutorials/building-flavors)."
   ```

3. **External links**: Maintain but verify
   ```
   [Garden Linux GitHub](https://github.com/gardenlinux/gardenlinux)
   ```

4. **Legacy links**: During migration, keep both
   ```
   "This content has moved to [How-to: Building Flavors](/how-to/customization/building-flavors).
   The old location is [deprecated](/legacy/gardenlinux/developers/build_image)."
   ```

### Content Adaptation Checklist

For each migrated file:

- [ ] **Remove role-based language** ("for developers", "for operators")
- [ ] **Add skill-level indicators** if needed ("beginner", "advanced")
- [ ] **Update outdated information** (versions, commands, screenshots)
- [ ] **Add prerequisites** section for how-tos and tutorials
- [ ] **Include expected outcomes** for tutorials
- [ ] **Add troubleshooting** for how-tos
- [ ] **Create cross-references** to related content
- [ ] **Update code blocks** with proper syntax highlighting
- [ ] **Verify all links** work in new structure
- [ ] **Add frontmatter** with proper metadata
- [ ] **Check images and media** paths are correct

### Handling Split Content

When splitting one file into multiple targets (e.g., kernel.md → architecture.md + kernels-and-modules.md):

1. **Create both target files** first
2. **Copy full source** to temporary location
3. **Extract conceptual content** → explanation file
4. **Extract factual content** → reference file
5. **Add cross-references** between the two
6. **Add redirect note** in legacy location pointing to both

Example redirect note:
```markdown
---
title: "Kernel Information (Deprecated)"
---

# This content has been reorganized

This document has been split into two locations:

- **Conceptual information**: See [Architecture](/explanation/architecture) for understanding Garden Linux kernel philosophy and design decisions
- **Technical reference**: See [Kernels and Modules](/reference/kernels-and-modules) for version tables and module lists

[View all documentation](/docs/)
```

### Handling Media Files

- Copy `.media/` directories to new locations
- Update image paths in markdown: `![alt](../../.media/image.png)` → `![alt](/assets/image.png)`
- Consider moving to centralized `/docs/public/assets/` directory
- Maintain media file organization by topic

### Special Cases

#### Architecture Decision Records (ADRs)
- **Do not copy all 32 files individually**
- Create summary document: `explanation/design-decisions.md`
- Categorize by theme
- Link to full ADRs on GitHub
- Highlight user-impacting decisions

#### Troubleshooting Content
- Maintain as separate section under how-to
- Clear problem-solution format
- Search-friendly titles ("Error: XYZ", "Problem: ABC")
- Link to related how-to guides

#### Deployment Guides
- Standardize structure across all platforms
- Common sections: Prerequisites, Steps, Verification, Troubleshooting
- Platform-specific variations clearly marked

## Script Modifications

The existing aggregation scripts need updates to support the new Diátaxis structure.

### Current Script Behavior

**scripts/aggregate-docs.sh**:
- Fetches docs from source repositories
- Places them in `docs/projects/`
- Runs transformation script

**scripts/transform_content.py**:
- Renames numbered directories
- Rewrites internal links
- Adds/fixes frontmatter
- Converts to VitePress format

### Required Modifications

#### Option 1: Dual-Target Approach (Recommended for Phase 2)

Keep aggregation to `docs/projects/` AND create migration script:

1. **Keep existing aggregation** (no changes to current scripts)
2. **Create new migration script**: `scripts/migrate_to_diataxis.py`
3. **Run migration as separate step** after aggregation

**Benefits**:
- Maintains current aggregation for legacy structure
- Allows gradual migration
- Can test new structure without breaking existing
- Easier rollback if needed

#### Option 2: Direct Migration Approach

Modify aggregation to target Diátaxis structure directly:

1. **Update `repos-config.json`** with new target mappings
2. **Modify `transform_content.py`** to handle Diátaxis categories
3. **Remove `docs/projects/` as aggregation target**

**Benefits**:
- Single source of truth
- No duplication
- Cleaner architecture

**Risks**:
- Requires all migrations done upfront
- More complex rollback

### Recommended: Option 1 Implementation

Create `scripts/migrate_to_diataxis.py` with this structure:

```python
#!/usr/bin/env python3
"""
Migrate aggregated content from docs/projects/ to Diátaxis structure
"""

MIGRATION_MAP = {
    # Introduction → Explanation & Reference
    "projects/gardenlinux/introduction/motivation.md": [
        ("explanation/use-cases.md", "adapt")
    ],
    "projects/gardenlinux/introduction/kernel.md": [
        ("explanation/architecture.md", "split_conceptual"),
        ("reference/kernels-and-modules.md", "split_factual")
    ],
    # ... more mappings
}

def migrate_file(source, target, action):
    """Migrate a single file with specified transformation"""
    pass

def split_content(source, targets):
    """Split one source into multiple targets"""
    pass

def merge_content(sources, target):
    """Merge multiple sources into one target"""
    pass
```

### Migration Script Features

1. **Content mapping** from `MIGRATION_MAP` configuration
2. **Transformation actions**:
   - `copy`: Direct copy with link updates
   - `adapt`: Copy with style adaptation
   - `split_conceptual`: Extract conceptual parts
   - `split_factual`: Extract reference parts
   - `merge`: Combine multiple sources
   - `summarize`: Create summary (for ADRs)

3. **Automatic tasks**:
   - Update internal links
   - Add proper frontmatter
   - Create redirect stubs in legacy locations
   - Validate migrated content

4. **Migration tracking**:
   - Track completed migrations
   - Generate migration report
   - Identify remaining files

### Configuration File

Create `scripts/diataxis-migration-config.json`:

```json
{
  "migrations": [
    {
      "source": "projects/gardenlinux/introduction/motivation.md",
      "targets": [
        {
          "path": "explanation/use-cases.md",
          "action": "adapt",
          "transformations": ["add_user_focus", "add_cross_references"]
        }
      ]
    },
    {
      "source": "projects/gardenlinux/introduction/kernel.md",
      "targets": [
        {
          "path": "explanation/architecture.md",
          "action": "split",
          "extract": "conceptual"
        },
        {
          "path": "reference/kernels-and-modules.md",
          "action": "split",
          "extract": "factual"
        }
      ]
    }
  ]
}
```

### Script Execution Order

```bash
# 1. Run existing aggregation (unchanged)
make aggregate-docs

# 2. Run new migration script
python scripts/migrate_to_diataxis.py \
    --config scripts/diataxis-migration-config.json \
    --source docs/projects/ \
    --target docs/ \
    --dry-run  # Test first

# 3. Verify results
python scripts/verify_migration.py

# 4. Generate report
python scripts/migration_report.py > MIGRATION-STATUS.md
```

### Update Makefile

Add new targets to `Makefile`:

```makefile
.PHONY: migrate-to-diataxis
migrate-to-diataxis:
	python scripts/migrate_to_diataxis.py \
		--config scripts/diataxis-migration-config.json \
		--source docs/projects/ \
		--target docs/

.PHONY: verify-migration
verify-migration:
	python scripts/verify_migration.py

.PHONY: migration-report
migration-report:
	python scripts/migration_report.py > MIGRATION-STATUS.md
```

## Migration Workflow

This section provides a detailed, step-by-step process for migrating content from the legacy structure to the new Diátaxis-based organization.

### Migration Strategy Overview

**Approach**: Batch migration with incremental delivery

- **Batch size**: 4-8 files per batch
- **Batch prioritization**: Based on content audit priorities (high → medium → low)
- **Delivery method**: One pull request per batch
- **Review gates**: Each batch reviewed and merged before starting next
- **Legacy preservation**: All legacy content remains accessible during migration

### Batch Organization

Migration is organized into 5 batches based on priority and content type:

#### Batch 1: Foundational Concepts (High Priority)
**Goal**: Establish core explanation and reference content  
**Files**: 6 items (1 summarization task)  
**Estimated effort**: 12-16 hours

1. `motivation.md` → `explanation/use-cases.md`
2. `kernel.md` → Split into `explanation/architecture.md` + `reference/kernels-and-modules.md`
3. `package-pipeline.md` → Merge into `explanation/architecture.md`
4. `release.md` → Split into `explanation/release-cadence.md` + `reference/releases/maintained-releases.md`
5. `boot_modes.md` → Split into `explanation/image-types.md` + `reference/image-formats.md`
6. `architecture/decisions/*.md` (32 ADRs) → Summarize into `explanation/design-decisions.md`

#### Batch 2: Developer & Build Content (High Priority)
**Goal**: Migrate development-focused how-to and contributing content  
**Files**: 9 items  
**Estimated effort**: 14-18 hours

1. `build_image.md` → `how-to/customization/building-flavors.md`
2. `build_image_openstack.md` → `how-to/platform-specific/openstack.md`
3. `build_packages.md` → `contributing/building-image.md`
4. `test_image.md` → `how-to/customization/testing-builds.md`
5. `contributing.md` → Merge into `contributing/README.md`
6. `bare_container.md` → `how-to/platform-specific/oci.md`
7. `github_pipelines.md` → Merge into `contributing/workflow.md`
8. `vmware-ova.md` → `how-to/platform-specific/vmware.md`
9. `troubleshooting/` → `how-to/troubleshooting/` (directory)

#### Batch 3: Operator & Security Content (High Priority)
**Goal**: Migrate operations and security how-to content  
**Files**: 10 items  
**Estimated effort**: 12-16 hours

1. `apt_repo.md` → Merge into `how-to/system-management.md`
2. `ssh-hardening.md` → `how-to/security/ssh-hardening.md`
3. `time-configuration.md` → `how-to/security/time-configuration.md`
4. `gardener-kernel-restart.md` → `how-to/platform-specific/gardener.md`
5. `lima-vm.md` → Split into `tutorials/first-boot-lima.md` + `how-to/platform-specific/lima.md`
6. `local-k8s-lima.md` → Merge into `how-to/platform-specific/lima.md`
7. `deployment/aws-secureboot.md` → `how-to/platform-specific/aws.md`
8. `deployment/gcp-secureboot.md` → `how-to/platform-specific/gcp.md`
9. `deployment/install-non-default.md` → Merge into `how-to/initial-configuration.md`
10. `deployment/ipxe-install.md` → `how-to/platform-specific/bare-metal.md`

#### Batch 4: Builder & Reference (Medium Priority)
**Goal**: Migrate builder documentation  
**Files**: 2 items  
**Estimated effort**: 4-6 hours

1. `builder/features.md` → `reference/feature-glossary.md`
2. `builder/getting_started.md` → Split into `how-to/customization/building-features.md` + content for `contributing/`

#### Batch 5: Python Library (Low Priority)
**Goal**: Convert and migrate Python library documentation  
**Files**: 4 items (RST → Markdown conversion)  
**Estimated effort**: 6-8 hours

1. `python-gardenlinux-lib/index.rst` → `reference/api/index.md`
2. `python-gardenlinux-lib/api.rst` → `reference/api/api.md`
3. `python-gardenlinux-lib/cli.rst` → `reference/api/cli.md`
4. `python-gardenlinux-lib/release.rst` → Merge into `reference/releases/`

### Per-Document Migration Workflow

For each document in a batch, follow this 10-step process:

#### Step 1: Read and Analyze Source Content

```bash
# Read the source file
cat docs/projects/gardenlinux/introduction/motivation.md

# Check for dependencies
grep -r "motivation" docs/projects/gardenlinux/
```

**Actions**:
- Read the complete source content
- Identify dependencies (files that link to this one)
- Note any media files (.media/ directory references)
- Identify the primary purpose and content type

#### Step 2: Classify Content Type

**Decision Matrix**:
- **Tutorial**: Step-by-step walkthrough, learning-oriented, beginner-friendly
- **How-to**: Task-oriented, problem-solving, assumes familiarity
- **Explanation**: Understanding-oriented, conceptual, discursive
- **Reference**: Information-oriented, lookup, factual
- **Contributing**: Process, workflow, standards

**Questions to ask**:
- Does it teach something new? → Tutorial
- Does it solve a specific problem? → How-to
- Does it explain concepts? → Explanation
- Is it a lookup table or spec? → Reference
- Is it about contributing? → Contributing

#### Step 3: Determine Target Location(s)

Based on content mapping in Section 4 of this document:

- **Single target**: Most documents map to one new location
- **Split target**: Some documents (kernel.md, release.md, boot_modes.md, lima-vm.md, getting_started.md) need splitting
- **Merge target**: Some documents (ADRs, lima docs, contributing docs) merge into existing files

**Create target path**:
```bash
# For single target
TARGET="docs/explanation/use-cases.md"

# For split targets
TARGET1="docs/explanation/architecture.md"
TARGET2="docs/reference/kernels-and-modules.md"
```

#### Step 4: Create or Update Target File

**For new files**:
```bash
# Create directory if needed
mkdir -p docs/explanation

# Create file with frontmatter template
cat > docs/explanation/use-cases.md << 'EOF'
---
title: "Use Cases"
description: "Why use Garden Linux and what problems it solves"
category: "explanation"
tags: ["use-cases", "overview"]
---

# Use Cases

[Content goes here]
EOF
```

**For split files**:
- Create both target files first
- Plan which sections go to each target
- Extract and transform each section appropriately

**For merge files**:
- Read existing target file
- Plan insertion point for new content
- Ensure consistent structure

#### Step 5: Transform Writing Style

Apply content type-specific transformations:

**For Tutorials**:
- Add clear learning objective at start
- Number steps (1, 2, 3...)
- Make commands copy-pasteable
- Show expected output
- Add success criteria at end
- Use conversational, encouraging tone

**For How-to Guides**:
- Clear goal/problem statement
- Add prerequisites section
- Use imperative mood ("Configure...", "Run...")
- Include variations and options
- Add troubleshooting tips
- Direct, professional tone

**For Explanation**:
- Introduce concept first
- Provide context and background
- Explain relationships and alternatives
- Remove step-by-step instructions
- Use discursive, thoughtful tone

**For Reference**:
- Use consistent format
- Create tables for structured data
- Be concise and factual
- Easy to scan
- Neutral, technical tone

#### Step 6: Update Frontmatter

Add proper frontmatter to the target file:

```yaml
---
title: "Use Cases"
description: "Why use Garden Linux and what problems it solves"
category: "explanation"
tags: ["use-cases", "overview", "introduction"]
---
```

**Validate**:
- Title is clear and descriptive
- Description is one sentence
- Category matches Diátaxis type
- Tags are relevant and useful

#### Step 7: Rewrite Links

Update all internal links to point to new structure:

```bash
# Find all links in the content
grep -o '\[.*\](.*\.md)' docs/explanation/use-cases.md

# Update each link manually or with sed
sed -i 's|/projects/gardenlinux/developers/build_image|/how-to/customization/building-flavors|g' docs/explanation/use-cases.md
```

**Link types to update**:
- Internal documentation links → new Diátaxis paths
- Relative links (../, ./) → absolute paths (/explanation/, /how-to/)
- Legacy project links → updated paths or external GitHub links
- Media references (.media/) → new asset locations

#### Step 8: Add Cross-References

Add navigation hints to related content:

```markdown
## Further Reading

- **Background**: See [Flavors and Features](/explanation/flavors-and-features) to understand how Garden Linux is structured
- **Tutorial**: Follow [First Boot on AWS](/tutorials/first-boot-aws) to deploy your first instance
- **How-to**: Learn to [Build Custom Flavors](/how-to/customization/building-flavors) for your use case
```

**Cross-reference rules**:
- Tutorials → link to related how-tos
- How-tos → link to explanation for background
- Explanation → link to tutorials and how-tos for practice
- Reference → link to explanation for context

#### Step 9: Create Legacy Redirect Stub

Create a redirect note in the legacy location:

```bash
# Create redirect file
cat > docs/projects/gardenlinux/introduction/motivation.md << 'EOF'
---
title: "Motivation (Moved)"
---

# This content has moved

This document has been migrated to the new documentation structure:

📍 **New location**: [Use Cases](/explanation/use-cases)

The new structure organizes documentation by content type (tutorials, how-to guides, explanation, reference) rather than by audience role.

[Browse all documentation](/)
EOF
```

#### Step 10: Verify in VitePress Dev Server

Test the migrated content:

```bash
# Start dev server
pnpm run docs:dev

# Open browser to http://localhost:5173
# Navigate to the new location
# Verify:
# - Content renders correctly
# - All links work
# - Images display
# - Frontmatter is correct
# - Navigation/sidebar works
```

**Verification checklist**:
- [ ] File renders without errors
- [ ] All internal links resolve
- [ ] All images display
- [ ] Code blocks have syntax highlighting
- [ ] Frontmatter displays correctly
- [ ] Sidebar navigation works
- [ ] Legacy redirect works
- [ ] Cross-references are valid

### Split-Document Workflow

For files that need splitting (kernel.md, release.md, boot_modes.md, lima-vm.md, getting_started.md):

#### Step 1: Analyze Content Sections

Read the source and identify sections:

```bash
# List all headings
grep '^##' docs/projects/gardenlinux/introduction/kernel.md

# Identify conceptual vs factual sections
# Conceptual: "Why we chose kernel X", "Philosophy"
# Factual: Version tables, module lists, specifications
```

#### Step 2: Create Both Target Files

```bash
# Create explanation file
mkdir -p docs/explanation
cat > docs/explanation/architecture.md << 'EOF'
---
title: "Architecture"
description: "Garden Linux system architecture and design philosophy"
category: "explanation"
tags: ["architecture", "kernel", "design"]
---

# Architecture

[Conceptual content goes here]
EOF

# Create reference file
mkdir -p docs/reference
cat > docs/reference/kernels-and-modules.md << 'EOF'
---
title: "Kernels and Modules"
description: "Kernel versions and module support matrix"
category: "reference"
tags: ["kernel", "modules", "specifications"]
---

# Kernels and Modules

[Factual content goes here]
EOF
```

#### Step 3: Extract and Place Content

**Conceptual sections → explanation file**:
- Philosophy and rationale
- Design decisions
- High-level descriptions
- "Why" explanations

**Factual sections → reference file**:
- Version tables
- Module lists
- Specifications
- Technical details

#### Step 4: Add Cross-References

In each file, reference the other:

```markdown
## Related Information

For technical specifications, see [Kernels and Modules Reference](/reference/kernels-and-modules).
```

#### Step 5: Create Two-Target Legacy Redirect

```markdown
---
title: "Kernel (Split)"
---

# This content has been reorganized

This document has been split into two locations:

- **Conceptual information**: [Architecture](/explanation/architecture) - kernel philosophy and design decisions
- **Technical reference**: [Kernels and Modules](/reference/kernels-and-modules) - version tables and module lists

[Browse all documentation](/)
```

### Merge-Document Workflow

For multiple sources merging into one target (ADRs, lima docs, contributing docs):

#### Step 1: Read All Source Files

```bash
# List all ADR files
ls docs/projects/gardenlinux/introduction/architecture/decisions/

# Read each one
for file in docs/projects/gardenlinux/introduction/architecture/decisions/*.md; do
    echo "=== $file ==="
    head -n 20 "$file"
done
```

#### Step 2: Create Summary Structure

```bash
cat > docs/explanation/design-decisions.md << 'EOF'
---
title: "Design Decisions"
description: "Key architecture decisions and their rationale"
category: "explanation"
tags: ["architecture", "decisions", "ADR"]
---

# Design Decisions

This document summarizes key architecture decisions (ADRs) that shape Garden Linux.

## Security Decisions

[Summarize security-related ADRs]

## Build System Decisions

[Summarize build-related ADRs]

## Testing Decisions

[Summarize test-related ADRs]

## Feature Decisions

[Summarize feature-related ADRs]

## Full ADR Archive

For complete details, see the [ADR archive on GitHub](https://github.com/gardenlinux/gardenlinux/tree/main/docs/architecture/decisions).
EOF
```

#### Step 3: Summarize Each Source

For each source document:
- Extract title and decision
- Summarize rationale (2-3 sentences)
- Link to full ADR on GitHub
---

## 8. Quality Assurance

### 8.1 Pre-Migration Checks
- Baseline content audit (count files, create inventory)
- Link inventory baseline (extract all internal links)
- Media file inventory

### 8.2 Per-File Validation

**Frontmatter**: Required fields (title, description, category), valid category values
**Links**: All internal links resolve, external links verified, no broken /projects/ links
**Content Type**: Matches declared category (tutorials have objectives, how-tos have prerequisites, etc.)
**Media**: Images exist, paths correct, alt text present

### 8.3 Per-Batch Validation

- VitePress build succeeds (`pnpm run docs:build`)
- Link validation passes for all migrated files
- Sidebar navigation updated and working
- Legacy redirects functional
- Cross-references resolve correctly

### 8.4 Automated Validation Scripts

Create these scripts in `scripts/`:
- `validate_frontmatter.py` - YAML structure validation
- `validate_links.py` - Link resolution checking
- `validate_content_type.py` - Content type compliance
- `verify_migration.py` - Master validation orchestrator

### 8.5 Manual Review Criteria

PR Review Checklist:
- [ ] Writing style matches content type
- [ ] No role-based language (developer/operator)
- [ ] Cross-references appropriate and working
- [ ] Legacy redirects in place
- [ ] Code examples tested
- [ ] Images display correctly
- [ ] Sidebar navigation updated

### 8.6 Final Validation

- Full site link check
- Production build succeeds
- Content completeness audit (all 59 files migrated)
- Search index includes new content
- Legacy URLs redirect properly

---

## 9. Implementation Checklist

### 9.1 Preparation (6 tasks)
- [ ] Review and approve migration plan
- [ ] Set up validation scripts
- [ ] Create migration config (diataxis-migration-config.json)
- [ ] Run baseline content audit
- [ ] Create preparation branch
- [ ] Test aggregation: `make aggregate-docs`

### 9.2 Batch 1: Foundational Concepts (6 files, 12-16 hours)

Branch: `phase2-batch-1-foundational-concepts`

- [ ] **1.1** motivation.md → explanation/use-cases.md (adapt, add use cases, cross-refs)
- [ ] **1.2** kernel.md → SPLIT (explanation/architecture.md + reference/kernels-and-modules.md)
- [ ] **1.3** package-pipeline.md → MERGE into explanation/architecture.md
- [ ] **1.4** release.md → SPLIT (explanation/release-cadence.md + reference/releases/maintained-releases.md)
- [ ] **1.5** boot_modes.md → SPLIT (explanation/image-types.md + reference/image-formats.md)
- [ ] **1.6** architecture/decisions/*.md → SUMMARIZE into explanation/design-decisions.md (32 ADRs)

**Completion**: Validate, test in dev server, update sidebar, create PR, review, merge

### 9.3 Batch 2: Developer & Build Content (9 files, 14-18 hours)

Branch: `phase2-batch-2-developer-content`

- [ ] **2.1** build_image.md → how-to/customization/building-flavors.md
- [ ] **2.2** build_image_openstack.md → how-to/platform-specific/openstack.md
- [ ] **2.3** build_packages.md → contributing/building-image.md
- [ ] **2.4** test_image.md → how-to/customization/testing-builds.md
- [ ] **2.5** contributing.md → MERGE into contributing/README.md
- [ ] **2.6** bare_container.md → how-to/platform-specific/oci.md
- [ ] **2.7** github_pipelines.md → MERGE into contributing/workflow.md
- [ ] **2.8** vmware-ova.md → how-to/platform-specific/vmware.md
- [ ] **2.9** troubleshooting/ → how-to/troubleshooting/ (directory copy)

**Completion**: Same validation and PR process

### 9.4 Batch 3: Operator & Security (10 files, 12-16 hours)

Branch: `phase2-batch-3-operator-security`

- [ ] **3.1** apt_repo.md → MERGE into how-to/system-management.md
- [ ] **3.2** ssh-hardening.md → how-to/security/ssh-hardening.md
- [ ] **3.3** time-configuration.md → how-to/security/time-configuration.md
- [ ] **3.4** gardener-kernel-restart.md → how-to/platform-specific/gardener.md
- [ ] **3.5** lima-vm.md → SPLIT (tutorials/first-boot-lima.md + how-to/platform-specific/lima.md)
- [ ] **3.6** local-k8s-lima.md → MERGE into how-to/platform-specific/lima.md
- [ ] **3.7** deployment/aws-secureboot.md → how-to/platform-specific/aws.md
- [ ] **3.8** deployment/gcp-secureboot.md → how-to/platform-specific/gcp.md
- [ ] **3.9** deployment/install-non-default.md → MERGE into how-to/initial-configuration.md
- [ ] **3.10** deployment/ipxe-install.md → how-to/platform-specific/bare-metal.md

**Completion**: Same validation and PR process

### 9.5 Batch 4: Builder (2 files, 4-6 hours)

Branch: `phase2-batch-4-builder-reference`

- [ ] **4.1** builder/features.md → reference/feature-glossary.md
- [ ] **4.2** builder/getting_started.md → SPLIT (how-to/customization/building-features.md + contributing/)

**Completion**: Same validation and PR process

### 9.6 Batch 5: Python Library (4 files, 6-8 hours) - OPTIONAL/PHASE 3

Branch: `phase2-batch-5-python-library`

- [ ] **5.1** python-gardenlinux-lib/index.rst → reference/api/index.md (RST→MD conversion)
- [ ] **5.2** python-gardenlinux-lib/api.rst → reference/api/api.md (RST→MD conversion)
- [ ] **5.3** python-gardenlinux-lib/cli.rst → reference/api/cli.md (RST→MD conversion)
- [ ] **5.4** python-gardenlinux-lib/release.rst → MERGE into reference/releases/

**Note**: RST conversion may require `pandoc` or manual conversion

### 9.7 Infrastructure Tasks (5 tasks)

- [ ] Update sidebar configuration in docs/.vitepress/config.mts with all new content
- [ ] Update Makefile with migration targets (migrate-to-diataxis, verify-migration, migration-report)
- [ ] Create verification script (scripts/verify_migration.py)
- [ ] Create migration report script (scripts/migration_report.py)
- [ ] Update docs/legacy/README.md with migration status tracking

### 9.8 Finalization (4 tasks)

- [ ] Run full link validation across entire site
- [ ] Verify all 59 files migrated (cross-check with baseline)
- [ ] Create final migration report: `make migration-report`
- [ ] Update documentation-reorganization-plan.md Phase 2 status to COMPLETE
- [ ] Announce migration completion to team

---

## Summary

**Total Migration Items**: 31 files + 32 ADR summaries = ~35