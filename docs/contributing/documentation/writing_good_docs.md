---
title: Documentation Quality Markers
description: Writing Good Documentation
order: 2
---

# Documentation Quality Markers

Good documentation should follow concrete and actionable quality markers to be
as helpful and professional as possible.

These markers can roughly be split into required markers, that every
documentation submission should have, and those which are context dependent and
therefore optional.

## Required Markers

### Accuracy & Completeness

It should go without saying that all documentation should be correct in an
informational sense. Meaning all code and commands need to be tested and any
tutorials & guides that are meant to lead a user through a process should be
executed by the reviewer once to see if they do what they were written for.

All code examples should:

- Be tested and verified to work
- Include expected output
- Cover common error cases where applicable
- Use realistic, representative examples

All documents should cover all the aspects of their respective topics and not
exclude edge cases even if they appear infrequent.

Each document should clearly state:

- Prerequisites (required knowledge, tools, or setup)
- Context (when and why this information is relevant)
- Next steps or related documentation

### Readability

One of the most important factors of good documentation is readability. This
means that good documents should have a clear structure separated by concise
headlines that serves both as a navigation aid and a red string through the
topic.

Another aspect of good readability is a well thought out **separation of
thoughts**. Ideally, every thought should have its own paragraph. This goes hand
in hand with keeping the sentence structure as short as possible and avoid
overly complex or nested sentences if possible.

Additional readability guidelines:

- Use active voice over passive voice
- Keep sentences focused (aim for 15-25 words)
- Use progressive disclosure (introduce simple concepts before complex ones)
- Break up long procedures into numbered steps

### Style & Language

All documentation should have a professional and inclusive tone. Gender-neutral
language (like they/them or role based nouns like "maintainer", "developer" or
"user") should be used. Language specific idioms common amongst native speakers
should be avoided and project specific abbreviations should always link to their
respective Glossary section.

Hand in hand with the last point goes formulating documents with **consistent
terminology**. To avoid confusion, especially in tutorials, certain terms like
"install" and "set up" should not be used as synonyms, but instead have their
own respective meanings.

Documentation should go into appropriate detail for the intended audience (i.e.
Users or Developers) and not omit any details or become vague when talking about
specific topics.

If a feature is not yet implemented or there are currently known bugs or Issues,
a "Known Issues" section should be appended to the bottom of the document
listing these issues and their corresponding GitHub issue if applicable.

Include expected output or other steps which the reader can use to verify
operation outcomes in any instructional guides.

Use examples liberally across the documentation for any document that advises
readers to action.

### Usability & Accessibility

Every person browsing documentation has different means and needs. Not only in
the information they are looking for, but also how they access and process this
documentation. Language barriers or disabilities may present barriers when
attempting to look for something in documentation.

There are a few things contributors can do to lower these barriers:

- Use descriptive link texts instead of a simple "click here"
- Images should have a descriptive alt text that explains what the image shows
- Headings should have a proper hierarchy to ease browsing (don't skip heading
  levels)
- Code examples should have syntax highlighting
- Navigation via keyboard must be possible across the site, the search bar
  should ideally be accessible via key combination
- In graphs and other visual media, **color alone must never be the only
  indicator of differences or importance** - use icons, labels, or patterns as
  well
- All links should be verified as working (no dead links)
- Links to external resources should specify version where applicable

### Discoverability

The best documentation is useless if no one can find it. All documents must be
discoverable on all index pages or navigation bars and be linked in the
appropriate context.

Documents should:

- Have clear, descriptive titles
- Be placed in the appropriate section (Tutorial, How-to, Explanation,
  Reference)
- Be cross-referenced from related documentation
- Include relevant keywords for search

### Maintainability

Documentation should be structured to minimize maintenance burden:

- Follow the "single source of truth" principle; don't duplicate information
  across multiple pages
- Include version information where relevant
- Clearly indicate ownership:
  - For subproject documentation, the maintainers of that subproject
    (identifiable via git blame) are responsible for updates
  - For documentation hub content (like these guides), the Documentation Lead
    owns maintenance if that role exists
- Use includes or references for content that appears in multiple places

## Conditional Markers

### Version Compatibility

Features that only apply to specific versions of Garden Linux or supporting
tools should be marked as such using markdown admonishments or any other
suitable formatting to make them stand out.

Breaking changes between versions should be indicated in an appropriately
colored warning or info box at the top of the document.

Version-specific content should include:

- Minimum version required
- Version where feature was introduced
- Deprecation warnings if applicable

## Checklist

Use this checklist when reviewing or submitting documentation:

### Core Markers

- ✅ All code and commands are tested and working
- ✅ Prerequisites are clearly stated
- ✅ Expected output is shown for verification steps
- ✅ Document has clear structure with descriptive headings
- ✅ One main idea per paragraph
- ✅ Sentences are concise and use active voice
- ✅ Neutral and professional language throughout
- ✅ Gender-neutral language used
- ✅ Consistent terminology (no synonym confusion)
- ✅ Project-specific abbreviations link to Glossary
- ✅ All images have descriptive alt text
- ✅ Links use descriptive text (not "click here")
- ✅ Proper heading hierarchy maintained
- ✅ Code examples have syntax highlighting
- ✅ Color is not the only indicator in visual media
- ✅ All links verified as working
- ✅ Document is discoverable via navigation/index
- ✅ Cross-referenced from related documentation
- ✅ Clear ownership indicated

### Conditional Markers

- ✅ Version compatibility noted (if applicable)
- ✅ Breaking changes highlighted (if applicable)
- ✅ Known issues section included (if applicable)
- ✅ External dependencies documented (if applicable)

## Next Steps

Before you get started, you might want to check out the following docs:

- [Documentation Workflow](./documentation_workflow.md)
- [Documentation Aggregator Architecture](./aggregation-architecture.md)
- [How to Documentation - Adding Repos to Aggregate](./adding-repos.md)
- [How to Documentation - Working With the Aggregator Locally](./working-locally.md)
- [Documentation Aggregator Technical Reference](./technical.md)
- [Documentation Aggregator Local Testing Guide](./testing.md)
- [Working with the Documentation Hub on Your Machine](./working-locally.md)
