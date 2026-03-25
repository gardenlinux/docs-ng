---
title: Revised Documentation Reorganization Approach
date: 2026-03-19
status: Active Implementation Plan
---

# Garden Linux Documentation - Revised Diátaxis Approach

## Executive Summary

This document outlines the **revised approach** to reorganizing Garden Linux documentation using the Diátaxis framework. The key change from the original plan is that **documentation stays in source repositories** and is reorganized there first, before being aggregated into the docs-ng site.

## Key Principles

### 1. Documentation Lives in Source Repositories

- **gardenlinux** repo: Contains most documentation
- **builder** repo: Contains builder-specific docs
- **python-gardenlinux-lib** repo: Contains API documentation

Each repo maintains its own `docs/` folder organized according to Diátaxis.

### 2. Reorganization Happens at Source

Content migration and Diátaxis reorganization happens in each repository on a `docs-ng` branch, NOT in the docs-ng aggregation repo.

### 3. Aggregation Pulls Organized Content

The docs-ng repository:
- Aggregates already-organized content from source repos
- Builds the final site with navigation and sidebar
- Does NOT transform or reorganize content (content is already organized)

## Implementation Phases

### Phase 1: Create Complete Skeleton (✅ DONE)

**Location**: docs-ng repository

**Status**: Completed

**What was created**:
- 42 placeholder files with TODO markers across all Diátaxis categories
- Each placeholder clearly states:
  - Which source repository owns the content
  - Which existing file(s) should be migrated
  - Whether it's new content or adaptation
  - The expected Diátaxis category (tutorials/how-to/explanation/reference)

**Finding TODOs**:
```bash
cd docs-ng
grep -r '<!-- TODO' docs/
```

**Result**: Complete documentation structure exists as placeholders, making it clear what content is needed where.

### Phase 2: Create docs-ng Branches in Source Repos (TODO)

**Location**: Each source repository (gardenlinux, builder, python-gardenlinux-lib)

**Action Items**:

1. **In gardenlinux repo**:
   ```bash
   cd /path/to/gardenlinux
   git checkout -b docs-ng
   # Reorganize docs/ according to Diátaxis
   # See REPO-MIGRATION-GARDENLINUX.md for details
   ```

2. **In builder repo**:
   ```bash
   cd /path/to/builder
   git checkout -b docs-ng
   # Adapt docs/ for Diátaxis
   # Primarily affects docs/features.md → reference/feature-glossary.md
   # Split docs/getting_started.md → how-to/customization/building-features.md
   ```

3. **In python-gardenlinux-lib repo**:
   ```bash
   cd /path/to/python-gardenlinux-lib
   git checkout -b docs-ng
   # Convert RST to Markdown
   # Organize API docs under reference/api/
   ```

### Phase 3: Content Migration in Source Repos (TODO)

**For each repository**, follow the migration guide:
- `REPO-MIGRATION-GARDENLINUX.md` - For gardenlinux repo
- `REPO-MIGRATION-BUILDER.md` - For builder repo (to be created)
- `REPO-MIGRATION-PYTHON-LIB.md` - For python-lib repo (to be created)

**Key Activities**:
1. Move files to new Diátaxis structure
2. Adapt writing style to match content type:
   - **Tutorials**: Conversational, step-by-step, beginner-friendly
   - **How-to**: Direct, task-focused, imperative mood
   - **Explanation**: Discursive, conceptual, understanding-focused
   - **Reference**: Concise, factual, lookup-oriented
3. Update internal links
4. Add proper frontmatter
5. Create new content where needed (marked as "NEW" in migration guides)

### Phase 4: Update Aggregation Configuration (TODO)

**Location**: docs-ng repository

**Action Items**:

1. Update `scripts/repos-config.json` to pull from `docs-ng` branches:
   ```json
   {
     "repos": [
       {
         "name": "gardenlinux",
         "url": "https://github.com/gardenlinux/gardenlinux",
         "docs_path": "docs",
         "target_path": "aggregated/gardenlinux",
         "branch": "docs-ng",  ← Changed from "main"
         "structure": "diataxis"
       }
     ]
   }
   ```

2. Update aggregation scripts to:
   - Pull from docs-ng branches
   - Map Diátaxis categories correctly
   - Preserve the already-organized structure

3. Update VitePress configuration with complete sidebar navigation

### Phase 5: Remove Placeholders, Enable Aggregation (TODO)

**Location**: docs-ng repository

**Action Items**:

1. Remove placeholder TODO files
2. Configure aggregation to pull organized content
3. Test the full site build
4. Verify all links work
5. Deploy

## Directory Structure Comparison

### Old Approach (Original Plan)

```
docs-ng/
└── docs/
    ├── projects/           ← Aggregated content here
    │   ├── gardenlinux/
    │   ├── builder/
    │   └── python-lib/
    └── [tutorials/how-to/explanation/reference organized in docs-ng]
```

**Problem**: Content transformation happens in aggregation layer, mixing concerns.

### New Approach (Current)

```
gardenlinux/
└── docs/                   ← Already organized by Diátaxis
    ├── tutorials/
    ├── how-to/
    ├── explanation/
    ├── reference/
    └── contributing/

builder/
└── docs/                   ← Already organized by Diátaxis
    ├── how-to/
    └── reference/

python-gardenlinux-lib/
└── docs/                   ← Already organized by Diátaxis
    └── reference/
        └── api/

docs-ng/
└── docs/                   ← Aggregates organized content
    ├── tutorials/          ← From gardenlinux + links
    ├── how-to/             ← From gardenlinux + builder + links
    ├── explanation/        ← From gardenlinux + links
    ├── reference/          ← From all repos + links
    └── contributing/       ← From gardenlinux + links
```

**Benefit**: Separation of concerns - repos organize their own docs, docs-ng just builds the site.

## Finding TODO Items

All placeholder files contain `<!-- TODO -->` markers. To find them:

```bash
# In docs-ng repo
grep -r '<!-- TODO' docs/ | wc -l
# Output: Shows count of TODO markers

# To see specific files:
grep -r '<!-- TODO: Content migration needed' docs/ -l

# To see source information:
grep -r 'Source:' docs/ | head -20
```

## Content Migration Priorities

### High Priority (Core Documentation)

1. **Explanation** - Foundational concepts users need to understand
   - use-cases.md (from motivation.md)
   - architecture.md (from kernel.md + package-pipeline.md)
   - image-types.md (from boot_modes.md)
   - release-cadence.md (from release.md)

2. **How-to Security** - Critical operational tasks
   - ssh-hardening.md
   - time-configuration.md

3. **Platform-Specific How-tos** - Most requested content
   - AWS, GCP, Azure deployment guides

### Medium Priority

1. **Tutorials** - Getting started guides
   - First boot tutorials for major platforms

2. **How-to Customization** - Advanced use cases
   - Building flavors and features

3. **Reference** - Lookup information
   - Feature glossary, flavor matrix

### Low Priority

1. **API Reference** - Specialized audience
   - Python library docs (requires RST conversion)

## Benefits of This Approach

### 1. Separation of Concerns
- Source repos: Own and organize their documentation
- docs-ng repo: Only responsible for aggregation and site building
- Clear ownership boundaries

### 2. Easier to Find Content
- All TODO markers clearly show what needs to be done
- Placeholder files show the final structure
- Migration guides provide step-by-step instructions

### 3. Maintainability
- Documentation lives with the code it documents
- Changes to features can update docs in the same PR
- No disconnect between code and docs

### 4. Scalability
- Easy to add new repositories to aggregation
- Each repo can work independently on documentation
- No central bottleneck for documentation updates

### 5. Clear Migration Path
- Placeholders show exactly what's needed
- Migration can happen incrementally
- Easy to track progress (count remaining TODOs)

## Next Steps

### Immediate (docs-ng repo)

1. ✅ Create placeholder structure (DONE - 42 files created)
2. ✅ Document new approach (DONE - this file)
3. ✅ Create gardenlinux migration guide (DONE - REPO-MIGRATION-GARDENLINUX.md)
4. ⏳ Create builder migration guide (TODO - REPO-MIGRATION-BUILDER.md)
5. ⏳ Create python-lib migration guide (TODO - REPO-MIGRATION-PYTHON-LIB.md)

### Source Repository Work (gardenlinux/builder/python-lib repos)

1. ⏳ Create `docs-ng` branches in each repository
2. ⏳ Reorganize documentation according to Diátaxis
3. ⏳ Migrate content following the migration guides
4. ⏳ Create new content where marked as "NEW"
5. ⏳ Test documentation builds locally

### Finalization (docs-ng repo)

1. ⏳ Update aggregation scripts to pull from `docs-ng` branches
2. ⏳ Update VitePress sidebar configuration
3. ⏳ Remove placeholder TODO files
4. ⏳ Enable content aggregation
5. ⏳ Test full site build
6. ⏳ Deploy

## Success Criteria

- [ ] All placeholder TODO files have corresponding content in source repos
- [ ] All source repos have `docs-ng` branches with Diátaxis structure
- [ ] Aggregation successfully pulls and combines content
- [ ] Site builds without errors
- [ ] All internal links work
- [ ] Navigation and search function correctly
- [ ] Content follows Diátaxis principles for each category

## Resources

- [Diátaxis Framework](https://diataxis.fr/)
- [Documentation Reorganization Plan](./documentation-reorganization-plan.md)
- [Phase 2 Implementation Plan](./PHASE-2-IMPLEMENTATION-PLAN.md)
- [Gardenlinux Migration Guide](./REPO-MIGRATION-GARDENLINUX.md)

## Questions & Decisions

### Q: Why not migrate content in docs-ng directly?

**A**: Keeping documentation in source repositories:
- Maintains single source of truth
- Allows documentation updates in same PRs as code changes
- Reduces complexity in aggregation layer
- Follows principle of separation of concerns

### Q: What happens to the current aggregated content in docs/projects/?

**A**: It remains temporarily as "legacy" documentation until migration is complete, then can be removed.

### Q: How do we handle cross-repo references?

**A**: Use absolute paths in the final aggregated site. During migration, document these cross-references so they can be properly linked after aggregation.

### Q: Can repositories still have different doc structures?

**A**: No - all repos must follow Diátaxis to ensure consistent user experience. However, not all repos need all categories (e.g., builder may only have how-to and reference).

## Contact & Support

For questions about this approach:
- Review the placeholder files to see what content is needed
- Check migration guides for specific repository instructions
- Use `grep -r '<!-- TODO' docs/` to find all remaining work

---

**Last Updated**: 2026-03-19  
**Status**: Phase 1 Complete, Phase 2 Ready to Begin  
**Next Action**: Create docs-ng branches in source repositories
