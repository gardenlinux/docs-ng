# Garden Linux Documentation Reorganization Plan

## Executive Summary

This plan outlines the reorganization of Garden Linux documentation from the current role-based structure (users, developers, operators) to a Diátaxis framework-based structure that focuses on content types and skill levels. The plan integrates insights from the workshop-201601-docs-ng prototype and provides a clear migration path for existing aggregated documentation.

## Current State Analysis

### Current Structure (docs-ng)
- **Technology**: VitePress-based documentation site
- **Organization**: Role-based (users, developers, operators)
- **Content**: Aggregated from multiple repositories (gardenlinux, builder, python-gardenlinux-lib)
- **Location**: `/docs/projects/` contains aggregated legacy documentation
- **Issues**: 
  - Mixed content types within sections
  - No clear distinction between learning, task, understanding, and reference content
  - Difficult for users to find the right type of documentation for their needs

### Workshop Prototype (workshop-201601-docs-ng)
- **Technology**: Docusaurus-based
- **Organization**: Diátaxis framework with clear content type separation
- **Structure**: 00_start-here, 01_tutorials, 02_how-to, 03_explanation, 04_reference, 05_contributing
- **Strengths**: Clear purpose for each section, skill-level appropriate content

## Proposed Structure

### Diátaxis Framework Implementation

```
docs/
├── index.md                          # Landing page with clear navigation
├── tutorials/                        # 01_tutorials (Learning-oriented)
│   ├── README.md                     # Tutorials overview
│   ├── first-boot-aws.md            # Complete walkthrough
│   ├── first-boot-azure.md
│   ├── first-boot-gcp.md
│   ├── first-boot-openstack.md
│   ├── first-boot-kvm.md
│   ├── first-boot-oci.md
│   └── first-boot-bare-metal.md
│
├── how-to/                           # 02_how-to (Task-oriented)
│   ├── README.md                     # How-to guides overview
│   ├── getting-images.md            # Where to download
│   ├── choosing-flavors.md          # Flavor selection
│   ├── initial-configuration.md     # SSH keys, cloud-init
│   ├── system-management.md         # Updates, users, disks
│   ├── platform-specific/           # Platform-specific tasks
│   │   ├── aws.md
│   │   ├── azure.md
│   │   ├── gcp.md
│   │   ├── openstack.md
│   │   ├── kvm.md
│   │   └── oci.md
│   ├── security/                    # Security tasks
│   │   ├── ssh-hardening.md
│   │   ├── secure-boot.md
│   │   └── time-configuration.md
│   └── customization/               # Building custom content
│       ├── README.md
│       ├── building-features.md
│       ├── building-flavors.md
│       └── testing-builds.md
│
├── explanation/                      # 03_explanation (Understanding-oriented)
│   ├── README.md                     # Explanation overview
│   ├── use-cases.md                 # Why use Garden Linux?
│   ├── flavors-and-features.md      # Conceptual explanation
│   ├── image-types.md               # Image formats and boot modes
│   ├── security-posture.md          # Security philosophy
│   ├── release-cadence.md           # Release lifecycle
│   ├── architecture.md              # High-level architecture
│   └── design-decisions.md          # Why things are the way they are
│
├── reference/                        # 04_reference (Information-oriented)
│   ├── README.md                     # Reference overview
│   ├── flavor-matrix.md             # Complete flavor table
│   ├── feature-glossary.md          # All features documented
│   ├── platform-compatibility.md    # Platform-feature matrix
│   ├── image-formats.md             # Image naming and formats
│   ├── kernels-and-modules.md       # Kernel versions and modules
│   ├── releases/                    # Release information
│   │   ├── README.md
│   │   ├── maintained-releases.md
│   │   └── release-notes.md
│   └── api/                         # API reference (if applicable)
│       └── ...
│
├── contributing/                     # 05_contributing
│   ├── README.md                     # Contributing overview
│   ├── documentation-guide.md       # How to write docs
│   ├── building-image.md            # Build process
│   ├── testing-image.md             # Testing process
│   ├── workflow.md                  # Git workflow
│   ├── code-style.md                # Coding standards
│   └── dependency-policy.md         # Dependency management
│
└── legacy/                           # Legacy documentation (temporary)
    ├── README.md                     # Migration status and guide
    ├── gardenlinux/                  # Aggregated from gardenlinux repo
    │   ├── introduction/
    │   ├── developers/
    │   └── operators/
    ├── builder/                      # Aggregated from builder repo
    └── python-gardenlinux-lib/       # Aggregated from python-lib repo
```

## Content Type Definitions

### 1. Tutorials (Learning-oriented)
**Purpose**: Teach users through hands-on, step-by-step walkthroughs
**Audience**: Beginners or those new to a specific topic
**Characteristics**:
- Start from zero knowledge
- Guaranteed successful outcome if followed exactly
- Minimal theory, maximum action
- Build confidence and familiarity
- Should be completable in one sitting

**Examples**:
- First boot on AWS (from image selection to running instance)
- First boot on Azure
- Building your first custom flavor

### 2. How-to Guides (Task-oriented)
**Purpose**: Solve specific problems or accomplish specific tasks
**Audience**: Users who know what they want to do
**Characteristics**:
- Goal-focused
- Assumes some familiarity
- Step-by-step instructions
- Can be adapted to different situations
- May require combining multiple guides

**Examples**:
- How to configure SSH hardening
- How to resize disks
- How to build custom features
- How to deploy on AWS with secure boot

### 3. Explanation (Understanding-oriented)
**Purpose**: Provide context, background, and conceptual understanding
**Audience**: Users who want to understand how and why
**Characteristics**:
- Discursive and conceptual
- Provides context and background
- Helps users think about the system
- No step-by-step instructions
- Connects concepts together

**Examples**:
- What are flavors and how do they work?
- Why is Garden Linux immutable?
- How does the security model work?
- What is the release lifecycle?

### 4. Reference (Information-oriented)
**Purpose**: Provide accurate, complete technical specifications
**Audience**: Users who need to look something up
**Characteristics**:
- Accurate and complete
- Concise and to the point
- Organized for quick lookup
- Consistent structure
- Comprehensive coverage

**Examples**:
- Flavor matrix (complete table)
- Feature glossary
- Platform compatibility matrix
- Image format specifications
- Kernel version and module list

## Audience and Skill Level Approach

Rather than organizing by role (user, developer, operator), we organize by **content type** and **skill level**:

### Skill Levels Within Each Content Type

**Beginner** (New to Garden Linux):
- Tutorials: First boot guides
- How-to: Basic configuration tasks
- Explanation: What is Garden Linux? Why use it?
- Reference: Basic terminology

**Intermediate** (Familiar with Garden Linux):
- Tutorials: Building custom flavors
- How-to: Platform-specific deployments, security hardening
- Explanation: Architecture, design decisions
- Reference: Flavor matrix, feature details

**Advanced** (Expert users):
- Tutorials: Advanced customization workflows
- How-to: Complex deployments, troubleshooting
- Explanation: Deep architectural concepts
- Reference: Complete API specs, kernel details

### Writing for Different Audiences

**For Beginners**:
- Use simple language
- Provide context and background
- Include more examples
- Link to explanations
- Avoid jargon

**For Intermediate Users**:
- Assume basic knowledge
- Focus on practical tasks
- Provide clear steps
- Include common pitfalls

**For Advanced Users**:
- Be concise and direct
- Assume deep knowledge
- Focus on edge cases and advanced topics
- Provide complete reference information

## Migration Strategy

### Phase 1: Structure Setup (Current)
- [x] Create new folder structure following Diátaxis
- [x] Create placeholder README files in each section
- [x] Update main navigation and sidebar configuration
- [x] Create this information architecture document

### Phase 2: Content Migration (Next)
- [ ] Audit existing aggregated documentation
- [ ] Categorize each document by Diátaxis type
- [ ] Move and adapt content to new structure
- [ ] Create cross-links between old and new locations
- [ ] Update internal links and references

### Phase 3: Content Enhancement (Following)
- [ ] Fill content gaps identified during migration
- [ ] Create missing tutorials
- [ ] Expand platform-specific content
- [ ] Add visual aids and diagrams
- [ ] Improve writing for each content type

### Phase 4: Legacy Cleanup (Final)
- [ ] Remove legacy directory once migration is complete
- [ ] Update all external references
- [ ] Final review and quality assurance

## Splitting Aggregated Documentation

### Current Aggregated Structure
The aggregated documentation from the gardenlinux repository is organized as:
- `introduction/` - Conceptual content
- `developers/` - Development-focused content
- `operators/` - Operations-focused content

### Proposed Splitting Strategy

#### Introduction Content → Explanation + Reference
- `motivation.md` → `explanation/use-cases.md`
- `kernel.md` → `explanation/architecture.md` + `reference/kernels-and-modules.md`
- `package-pipeline.md` → `explanation/architecture.md`
- `release.md` → `explanation/release-cadence.md` + `reference/releases/`
- `boot_modes.md` → `explanation/image-types.md` + `reference/image-formats.md`
- `architecture/decisions/` → `explanation/design-decisions.md` (summarized)

#### Developers Content → How-to + Contributing
- `build_image.md` → `how-to/customization/building-flavors.md`
- `build_image_openstack.md` → `how-to/platform-specific/openstack.md`
- `build_packages.md` → `contributing/building-image.md`
- `test_image.md` → `how-to/customization/testing-builds.md`
- `contributing.md` → `contributing/README.md`
- `bare_container.md` → `how-to/platform-specific/oci.md`
- `github_pipelines.md` → `contributing/workflow.md`
- `vmware-ova.md` → `how-to/platform-specific/vmware.md` (new)
- `troubleshooting/` → `how-to/troubleshooting/` (new section)

#### Operators Content → How-to + Reference
- `apt_repo.md` → `how-to/system-management.md`
- `ssh-hardening.md` → `how-to/security/ssh-hardening.md`
- `time-configuration.md` → `how-to/security/time-configuration.md`
- `gardener-kernel-restart.md` → `how-to/platform-specific/gardener.md` (new)
- `lima-vm.md` → `how-to/platform-specific/lima.md` (new)
- `local-k8s-lima.md` → `how-to/platform-specific/lima.md` (new)
- `deployment/` → `how-to/platform-specific/` (split by platform)

### Content Transformation Guidelines

When splitting and moving content:

1. **Identify the primary purpose** of each document
2. **Determine the appropriate Diátaxis category**
3. **Adjust writing style** to match the category:
   - Tutorials: Conversational, step-by-step
   - How-to: Direct, task-focused
   - Explanation: Discursive, conceptual
   - Reference: Concise, factual
4. **Update internal links** to new locations
5. **Add appropriate frontmatter** for the new structure
6. **Create cross-references** where content relates to multiple categories

## Navigation and Information Architecture

### Main Navigation Structure

```
Start Here (Home)
├── Tutorials
│   ├── First Boot on AWS
│   ├── First Boot on Azure
│   ├── First Boot on GCP
│   ├── First Boot on OpenStack
│   ├── First Boot on KVM
│   └── First Boot on OCI
│
├── How-to Guides
│   ├── Getting Images
│   ├── Choosing Flavors
│   ├── Initial Configuration
│   ├── System Management
│   ├── Platform-Specific
│   ├── Security
│   └── Customization
│
├── Explanation
│   ├── Use Cases
│   ├── Flavors and Features
│   ├── Image Types
│   ├── Security Posture
│   ├── Release Cadence
│   └── Architecture
│
├── Reference
│   ├── Flavor Matrix
│   ├── Feature Glossary
│   ├── Platform Compatibility
│   ├── Image Formats
│   ├── Kernels and Modules
│   └── Releases
│
└── Contributing
    ├── Documentation Guide
    ├── Building Images
    ├── Testing Images
    ├── Workflow
    ├── Code Style
    └── Dependency Policy
```

### Sidebar Organization

Each section should have its own sidebar that:
- Lists all documents in that category
- Groups related content logically
- Provides clear navigation within the category
- Links to related content in other categories where appropriate

### Cross-Linking Strategy

- **Tutorials** should link to relevant **How-to guides** for variations
- **How-to guides** should link to **Explanation** for background
- **Explanation** should link to **Reference** for detailed specs
- **Reference** should link to **Tutorials** and **How-to guides** for examples

## Initial Content Items

### Tutorials (7 items)
1. **First Boot on AWS** - Complete walkthrough from image to running instance
2. **First Boot on Azure** - Complete walkthrough from image to running instance
3. **First Boot on GCP** - Complete walkthrough from image to running instance
4. **First Boot on OpenStack** - Complete walkthrough from image to running instance
5. **First Boot on KVM** - Complete walkthrough from download to running VM
6. **First Boot on OCI** - Complete walkthrough for container deployments
7. **First Boot on Bare Metal** - Complete walkthrough for physical hardware

### How-to Guides (15+ items)
1. **Getting Images** - Where to download releases and nightly builds
2. **Choosing Flavors** - Understanding flavor naming and selection
3. **Initial Configuration** - SSH keys, cloud-init, Ignition
4. **System Management** - Updates, users, disks, APT repos
5. **AWS Deployment** - Platform-specific deployment tasks
6. **Azure Deployment** - Platform-specific deployment tasks
7. **GCP Deployment** - Platform-specific deployment tasks
8. **OpenStack Deployment** - Platform-specific deployment tasks
9. **KVM Deployment** - Platform-specific deployment tasks
10. **OCI Deployment** - Platform-specific deployment tasks
11. **SSH Hardening** - Security configuration
12. **Secure Boot** - Secure boot configuration
13. **Time Configuration** - NTP and time sync
14. **Building Custom Features** - Feature development
15. **Building Custom Flavors** - Flavor development
16. **Testing Builds** - Testing in various environments

### Explanation (7 items)
1. **Use Cases** - Why use Garden Linux? (SAP Gardener, Kubernetes, containers, etc.)
2. **Flavors and Features** - What are they? How do they work?
3. **Image Types** - Different formats and boot modes
4. **Security Posture** - Immutable images, secure boot, CIS compliance
5. **Release Cadence** - Release lifecycle, versioning, update strategy
6. **Architecture** - High-level system architecture
7. **Design Decisions** - Why things are the way they are (summarized from ADRs)

### Reference (7+ items)
1. **Flavor Matrix** - Complete table of all flavors
2. **Feature Glossary** - All features documented
3. **Platform Compatibility** - Which platforms support which features
4. **Image Formats** - Naming conventions and format specifications
5. **Kernels and Modules** - Kernel versions and module support
6. **Maintained Releases** - Current releases with dates and status
7. **Release Notes** - Release notes from GitHub

### Contributing (6 items)
1. **Documentation Guide** - How to write and contribute docs
2. **Building Images** - Build process documentation
3. **Testing Images** - Testing process documentation
4. **Workflow** - Git workflow and contribution process
5. **Code Style** - Coding standards and conventions
6. **Dependency Policy** - Dependency management guidelines

## Implementation Recommendations

### Technology Choice
- **Current**: VitePress
- **Workshop**: Docusaurus
- **Recommendation**: Keep VitePress for now, as it's already set up and working. The Diátaxis structure is technology-agnostic and can be implemented in either system.

### Content Management
- Keep the aggregation system for pulling content from source repos
- Update the transformation scripts to place content in the new Diátaxis structure
- Maintain the legacy directory during migration for reference

### Quality Assurance
- Create a style guide for each content type
- Implement automated checks for:
  - Proper frontmatter
  - Internal link validity
  - Content type consistency
  - Writing style guidelines

### Community Involvement
- Make it easy for contributors to understand where new content belongs
- Provide templates for each content type
- Create contribution guidelines specific to documentation

## Success Metrics

### User Experience
- Users can quickly find the right type of documentation
- Reduced time to complete common tasks
- Fewer support questions about basic topics

### Content Quality
- Clear separation of content types
- Consistent writing style within each type
- Complete coverage of all topics

### Maintainability
- Easy to add new content in the right place
- Clear ownership and update process
- Automated quality checks

## Next Steps

1. **Review and approve this plan** with stakeholders
2. **Set up the new folder structure** in docs-ng
3. **Create placeholder content** for all sections
4. **Begin content migration** starting with the most-used documents
5. **Update aggregation scripts** to support the new structure
6. **Create contribution guidelines** for each content type
7. **Implement quality checks** and automation
8. **Gather user feedback** and iterate

## References

- [Diátaxis Framework](https://diataxis.fr/)
- [Divio Documentation System](https://docs.divio.com/documentation-system/)
- [Mintlify Content Types Guide](https://www.mintlify.com/guides/content-types)
- [Mintlify Navigation Guide](https://www.mintlify.com/guides/navigation)
- [Mintlify Audience Guide](https://www.mintlify.com/guides/know-your-audience)
- Workshop prototype: `/home/yeoldegrove/kunden/SAP/gardenlinux/workshop-201601-docs-ng/`
