---
title: Documentation Workflow
description: How to Contribute Documentation to Gardenlinux
order: 1
---

# Documenting Gardenlinux

This guide will provide you a detailed overview over everything you need to know
to support our efforts in documenting the Gardenlinux project.

## When Is Documentation Necessary?

Documentation is always necessary when a piece of software, a process or
information is touched that has implications for other people. May they be
internal or external contributors, users or decision makers.

## What Should Be Documented?

In the context of this Documentation Hub, anything that has implication to the
"outside". Meaning other users, operators, developers or decision makers needs
to be documented accordingly.

This includes, but is not limited to:

- Usage of Gardenlinux and any supporting tool
- Features and components of the project
- Ways to contribute and where to find help
- Information about where to submit security incidents
- Information about who is developing the project

Of course this does not apply to purely internal changes like code cleanup
contributions or similar that have no outside effect.

## Who Is Responsible for Maintaining Documentation?

The question of _"who is responsible?"_ can be split into two roles: The
contributors and a documentation lead.

### Contributors

Contributors are defined as individuals, groups or organisations that submit
code or non-code contributions to the project. These should, in addition to
their submission, document their changes with appropriate changes to any
relevant pieces of documentation. This applies to _any contribution_ if the
change is relevant for others.

For example:

1. A person introduces a new feature to Gardenlinux and opens a Pull Request
2. A maintainer reviews said feature and advises the contributor to write
   documentation for it
3. Said documentation will reviewed by the maintainer in question or the
   documentation lead if applicable
4. If both the code and the documentation both fulfill their respective quality
   markers, the PR is merged

### The Documentation Lead

This is a more or less informal position that is quite common in many projects:
One maintainer/developer who is responsible for handling the documentation hub
and enforcing style and quality standards according to written design documents.

This can be a liaison to a formal documentation team who is briefed on the
project and works closely with the development team, a team member that is
permanently appointed to or volunteers for this position, or a rotating position
that anyone in the team may take on for a set amount of time.

However this may be implemented it is important to stress that _**documentation
is a team effort**_.

The responsibilities of this person are:

- Evaluating whether a contribution requires documentation & what scope that
  documentation needs to be
- Making sure that documentation is written and put in the correct place
- Ensuring that the documentation pipeline is running and the documentation
  website is accessible

## The Review Process

Any changes to documentation will be reviewed by maintainers for the quality
criteria mentioned below. Only after the review is successful will the changes
be merged. The review validates:

- **Technical accuracy and sufficient depth**: The document matches implemented
  behaviour and guides are executable.
- **Completeness**: All affected changes are documented.
- **Readability**: The documentation is free of typos and grammatical errors.
- **Style and Inclusivity**: Language follows the project's expectations and
  quality criteria, all images have appropriate alt text descriptions for people
  using screen readers.

In cases where there is a Documentation Lead, this person must review changes to
documentation for their adherence to the project's quality markers.

In cases where there is **no** dedicated Documentation Lead, documentation
changes must be reviewed by other team members and tweaked according to their
feedback until unanimous agreement is reached.

## Quality Markers

All documentation should have a professional and inclusive tone. Gender-neutral
language (like they/them or role based nouns like "maintainer", "developer" or
"user") should be used. Language specific idioms common amongst native speakers
should be avoided and project specific abbreviations should always link to their
respective Glossary section.

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

## Version Compatibility

Features that only apply to a specific versions of Gardenlinux or supporting
tools should be marked as such using admonishments.

Breaking changes between version should be indicated in a appropriately colored
warning or info box at the top of the document.
