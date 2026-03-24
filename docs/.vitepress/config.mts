import { defineConfig } from "vitepress";

// Get base URL from environment variable (for GitHub Pages deployment)
const base = process.env.BASE_URL || "/";

// Shared sidebar for all documentation categories
const documentationSidebar = [
  {
    text: "Overview",
    link: "/overview/",
  },
  {
    text: "Tutorials",
    collapsed: true,
    items: [
      { text: "Overview", link: "/tutorials/" },
      { text: "First Boot - AWS", link: "/tutorials/first-boot-aws" },
      { text: "First Boot - Azure", link: "/tutorials/first-boot-azure" },
      {
        text: "First Boot - Bare Metal",
        link: "/tutorials/first-boot-bare-metal",
      },
      { text: "First Boot - GCP", link: "/tutorials/first-boot-gcp" },
      { text: "First Boot - KVM", link: "/tutorials/first-boot-kvm" },
      { text: "First Boot - Lima", link: "/tutorials/first-boot-lima" },
      { text: "First Boot - OCI", link: "/tutorials/first-boot-oci" },
      {
        text: "First Boot - OpenStack",
        link: "/tutorials/first-boot-openstack",
      },
    ],
  },
  {
    text: "How-to Guides",
    collapsed: true,
    items: [
      { text: "Overview", link: "/how-to/" },
      { text: "Choosing Flavors", link: "/how-to/choosing-flavors" },
      { text: "Getting Images", link: "/how-to/getting-images" },
      { text: "Initial Configuration", link: "/how-to/initial-configuration" },
      { text: "System Management", link: "/how-to/system-management" },
      {
        text: "Customization",
        collapsed: true,
        items: [
          { text: "Overview", link: "/how-to/customization/" },
          {
            text: "Building Features",
            link: "/how-to/customization/building-features",
          },
          {
            text: "Building Flavors",
            link: "/how-to/customization/building-flavors",
          },
          {
            text: "Testing Builds",
            link: "/how-to/customization/testing-builds",
          },
        ],
      },
      {
        text: "Platform-Specific",
        collapsed: true,
        items: [
          { text: "Overview", link: "/how-to/platform-specific/" },
          { text: "AWS", link: "/how-to/platform-specific/aws" },
          { text: "Azure", link: "/how-to/platform-specific/azure" },
          { text: "Bare Metal", link: "/how-to/platform-specific/bare-metal" },
          { text: "Gardener", link: "/how-to/platform-specific/gardener" },
          { text: "GCP", link: "/how-to/platform-specific/gcp" },
          { text: "KVM", link: "/how-to/platform-specific/kvm" },
          { text: "Lima", link: "/how-to/platform-specific/lima" },
          { text: "OCI/Containers", link: "/how-to/platform-specific/oci" },
          { text: "OpenStack", link: "/how-to/platform-specific/openstack" },
          { text: "VMware", link: "/how-to/platform-specific/vmware" },
        ],
      },
      {
        text: "Security",
        collapsed: true,
        items: [
          { text: "Overview", link: "/how-to/security/" },
          { text: "Secure Boot", link: "/how-to/security/secure-boot" },
          { text: "SSH Hardening", link: "/how-to/security/ssh-hardening" },
          {
            text: "Time Configuration",
            link: "/how-to/security/time-configuration",
          },
        ],
      },
    ],
  },
  {
    text: "Explanation",
    collapsed: true,
    items: [
      { text: "Overview", link: "/explanation/" },
      { text: "Architecture", link: "/explanation/architecture" },
      { text: "Design Decisions", link: "/explanation/design-decisions" },
      {
        text: "Flavors and Features",
        link: "/explanation/flavors-and-features",
      },
      { text: "Image Types", link: "/explanation/image-types" },
      { text: "Release Cadence", link: "/explanation/release-cadence" },
      { text: "Security Posture", link: "/explanation/security-posture" },
      { text: "Use Cases", link: "/explanation/use-cases" },
    ],
  },
  {
    text: "Reference",
    collapsed: true,
    items: [
      { text: "Overview", link: "/reference/" },
      { text: "Feature Glossary", link: "/reference/feature-glossary" },
      { text: "Flavor Matrix", link: "/reference/flavor-matrix" },
      { text: "Image Formats", link: "/reference/image-formats" },
      { text: "Kernels & Modules", link: "/reference/kernels-and-modules" },
      {
        text: "Platform Compatibility",
        link: "/reference/platform-compatibility",
      },
      {
        text: "API",
        collapsed: true,
        items: [
          { text: "Overview", link: "/reference/api/" },
          { text: "CLI", link: "/reference/api/cli" },
          { text: "Python Library", link: "/reference/api/python-lib" },
        ],
      },
      {
        text: "Releases",
        collapsed: true,
        items: [
          { text: "Overview", link: "/reference/releases/" },
          {
            text: "Maintained Releases",
            link: "/reference/releases/maintained-releases",
          },
          { text: "Release Notes", link: "/reference/releases/release-notes" },
        ],
      },
    ],
  },
  {
    text: "Contributing",
    collapsed: true,
    items: [
      { text: "Overview", link: "/contributing/" },
      {
        text: "Documentation Guide",
        link: "/contributing/documentation-guide",
      },
      { text: "Building an Image", link: "/contributing/building-image" },
      { text: "Testing an Image", link: "/contributing/testing-image" },
      { text: "Contribution Workflow", link: "/contributing/workflow" },
      { text: "Code Style", link: "/contributing/code-style" },
      {
        text: "Dependency Policy",
        link: "/contributing/dependency-policy",
      },
    ],
  },
];

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base,
  title: "Garden Linux",
  // description: "Operating system built for cloud native workloads.",
  ignoreDeadLinks: [
    // Ignore dead links in legacy documentation
    /\/how-to\/troubleshooting\//,
    /localhost/,
    /\/projects\/gardenlinux\/02_operators\/deployment/,
  ],
  head: [
    [
      "link",
      {
        rel: "icon",
        type: "image/svg+xml",
        href: `/gardenlinux-logo.svg`,
      },
    ],
    ["meta", { name: "theme-color", content: "#009f76" }],
    ["meta", { property: "og:type", content: "website" }],
    ["meta", { property: "og:site_name", content: "Garden Linux" }],
    [
      "meta",
      {
        property: "og:image",
        content:
          "https://raw.githubusercontent.com/gardenlinux/gardenlinux/main/logo/gardenlinux-logo-black-text.svg",
      },
    ],
    ["meta", { property: "og:url", content: "https://gardenlinux.io/" }],
  ],
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: {
      light: `/gardenlinux-logo.svg`,
      dark: `/gardenlinux-logo.svg`,
    },
    nav: [
      { text: "Start Here", link: "/" },
      {
        text: "Documentation",
        items: [
          {
            text: "Overview",
            link: "/overview/",
          },
          {
            text: "Tutorials",
            link: "/tutorials/",
          },
          {
            text: "How-to Guides",
            link: "/how-to/",
          },
          {
            text: "Explanation",
            link: "/explanation/",
          },
          {
            text: "Reference",
            link: "/reference/",
          },
          {
            text: "Contributing",
            link: "/contributing/",
          },
        ],
      },
      // {
      //   text: "Legacy Docs",
      //   items: [
      //     {
      //       text: "Garden Linux",
      //       link: "/projects/gardenlinux/introduction/index",
      //     },
      //     { text: "Builder", link: "/projects/builder/getting_started" },
      //     {
      //       text: "Python Library",
      //       link: "/projects/python-gardenlinux-lib/index",
      //     },
      //   ],
      // },
      // { text: "Contributing", link: "/contributing/" },
    ],

    // footer: {
    //   message: "Built with 💚 by the Gardenlinux Team.",
    //   copyright: "Copyright © 2026-present",
    // },

    sidebar: {
      // Shared sidebar for all documentation categories
      "/overview/": documentationSidebar,
      "/tutorials/": documentationSidebar,
      "/how-to/": documentationSidebar,
      "/explanation/": documentationSidebar,
      "/reference/": documentationSidebar,
      "/contributing/": documentationSidebar,
    },

    socialLinks: [{ icon: "github", link: "https://github.com/gardenlinux" }],

    search: {
      provider: "local",
    },
  },
});
