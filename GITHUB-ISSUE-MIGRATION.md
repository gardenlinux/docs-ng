# Documentation Migration to Diátaxis Framework - gardenlinux repo

**What would you like to be added**:

Reorganize [gardenlinux repo](https://github.com/gardenlinux/gardenlinux) from the current numbered structure (`00_introduction/`, `01_developers/`, `02_operators/`) to the [Diátaxis framework](https://diataxis.fr/) with four categories: **Tutorials**, **How-To Guides**, **Explanation**, and **Reference**.

### Current Structure

```
docs/
├── 00_introduction/     → explanation/ + reference/
├── 01_developers/       → how-to/customization/ + contributing/
├── 02_operators/        → how-to/platform-specific/ + how-to/security/
├── architecture/        → explanation/design-decisions.md
└── boot_modes.md        → explanation/ + reference/
```

### New Structure

```
docs/
├── tutorials/           (first-boot guides for each platform)
├── how-to/              (practical task-oriented guides)
│   ├── platform-specific/
│   ├── security/
│   ├── customization/
│   └── troubleshooting/
├── explanation/         (concepts, architecture, design)
├── reference/           (specs, matrices, release info)
│   └── releases/
└── contributing/        (development workflow)
```

## Migration Tracking System

Each file includes **frontmatter metadata** for tracking progress:

```yaml
---
title: "Document Title"
migration_status: "new" # new | adapt | merge | done
migration_source: "old/path.md" # source file(s) to migrate from
migration_issue: "gardenlinux#42" # this issue number
migration_stakeholder: "@tmang0ld, @yeoldegrove, @ByteOtter"
migration_approved: false # true when approved
---
```

Use the migration tracker script from the [docs-ng](https://github.com/gardenlinux/docs-ng) repo:

```bash
scripts/migration_tracker.py --dir /path/to/gardenlinux/docs
```

**Example Output:**

```markdown
## Documentation Migration Progress

**Last updated:** 2026-03-19 15:57

### Summary

| Status   | Count | Percentage |
| -------- | ----- | ---------- |
| ✅ done  | 0     | 0%         |
| 🆕 new   | 23    | 44%        |
| 🔄 adapt | 25    | 48%        |
| 🔀 merge | 4     | 8%         |

**Approved:** 0/58 (0%)

...
```
