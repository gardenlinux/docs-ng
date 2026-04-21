---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Garden Linux"
  text: "Purpose-built Linux for cloud-native workloads"
  tagline: "Debian-based, fully open source, and optimized for Kubernetes and containers"
  actions:
    - theme: brand
      text: Start Here
      link: /overview/
    - theme: alt
      text: First Boot
      link: /tutorials
    - theme: alt
      text: Releases
      link: /reference/releases/maintained-releases
  image:
    src: /gardenlinux-logo.svg
    alt: Garden Linux Logo

features:
  ### # use cases
  ### - title: Container Runtime
  ###   details: The preferred Kubernetes worker node for 90% of cloud applications deployed with Gardener
  ###   link: /overview/
  ### - title: Container Base Images
  ###   details: Package applications according to the OCI specification
  ###   link: /how-to/container-base-image
  ### - title: Virtual Machine Host
  ###   details: OS for deploying hypervisor nodes to run Kubernetes nodes
  ###   link: /tutorials/
  # documentation
  - title: Tutorials
    details: Step-by-step walkthroughs to get you started with Garden Linux
    link: /tutorials/
  - title: How-to Guides
    details: Task-focused guides for specific problems and goals
    link: /how-to/
  - title: Explanation
    details: Understanding-oriented content that provides context and background
    link: /explanation/
  # - title: Reference
  #   details: Information-oriented technical specifications and lookup tables
  #   link: /reference/
  - title: Contributing
    details: Guides for contributing to Garden Linux documentation and development
    link: /contributing/
  - title: Releases
    details: Overview which Garden Linux Releases are available
    link: /reference/releases/
  - title: Report an Issue
    details: Learn how to report any issue you face with Garden Linux
    link: /how-to/reporting-issues

migration_status: "adapt"
migration_issue: https://github.com/gardenlinux/gardenlinux/issues/4622
migration_stakeholder: "@tmang0ld, @yeoldegrove, @ByteOtter"
migration_approved: false
---
