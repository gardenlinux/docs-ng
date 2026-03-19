import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Gardenlinux Documentation",
  description: "All your documentation need - in one place",
  head: [
    [
      "link",
      { rel: "icon", type: "image/svg+xml", href: "/gardenlinux-logo.svg" },
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
      light: "/gardenlinux-logo.svg",
      dark: "/gardenlinux-logo.svg",
    },
    nav: [
      { text: "Home", link: "/" },
      { text: "Quick Start", link: "/users/quickstart" },
      {
        text: "Docs",
        items: [
          {
            text: "User Docs",
            items: [
              { text: "Quickstart", link: "/users/quickstart" },
              { text: "Installation Guide", link: "/users/installation" },
              { text: "Build an Image", link: "/users/build-image" },
            ],
          },
          {
            text: "Technical Documentation",
            items: [
              {
                text: "Garden Linux",
                link: "/projects/gardenlinux/introduction/index",
              },
              { text: "Builder", link: "/projects/builder/getting_started" },
              {
                text: "Python Library",
                link: "/projects/python-gardenlinux-lib/index",
              },
            ],
          },
          {
            text: "Contributing",
            link: "/contributing/",
          },
        ],
      },
    ],

    footer: {
      message: "Built with 💚 by the Gardenlinux Team.",
      copyright: "Copyright © 2026-present",
    },

    sidebar: {
      // Default sidebar for root pages
      "/": [
        {
          text: "Getting Started",
          items: [{ text: "Quick Start", link: "/users/quickstart" }],
        },
        {
          text: "Usage Docs",
          items: [
            { text: "Installation Guide", link: "/users/installation" },
            { text: "Build an Image", link: "/users/build-image" },
          ],
        },
        {
          text: "Technical Documentation",
          items: [
            {
              text: "Garden Linux",
              link: "/projects/gardenlinux/introduction/index",
            },
            { text: "Builder", link: "/projects/builder/getting_started" },
            {
              text: "Python Library",
              link: "/projects/python-gardenlinux-lib/index",
            },
          ],
        },
        {
          text: "Contributing",
          collapsed: true,
          items: [
            {
              text: "Development Environment",
              link: "/contributing/dev-environment",
            },
            { text: "Building an Image", link: "/contributing/building-image" },
            { text: "Testing an Image", link: "/contributing/testing-image" },
            { text: "Contribution Workflow", link: "/contributing/workflow" },
            { text: "Code Style", link: "/contributing/code-style" },
            {
              text: "Dependency Policy",
              link: "/contributing/dependency-policy",
            },
            {
              text: "Documentation Guide",
              link: "/contributing/documentation-guide",
            },
          ],
        },
      ],

      // Garden Linux project docs
      "/projects/gardenlinux/": [
        {
          text: "Introduction",
          collapsed: false,
          items: [
            {
              text: "Overview",
              link: "/projects/gardenlinux/introduction/index",
            },
            {
              text: "Linux Kernel",
              link: "/projects/gardenlinux/introduction/kernel",
            },
            {
              text: "Motivation",
              link: "/projects/gardenlinux/introduction/motivation",
            },
            {
              text: "Package Pipeline",
              link: "/projects/gardenlinux/introduction/package-pipeline",
            },
            {
              text: "Release Plan",
              link: "/projects/gardenlinux/introduction/release",
            },
          ],
        },
        {
          text: "Developers",
          collapsed: false,
          items: [
            {
              text: "Overview",
              link: "/projects/gardenlinux/developers/index",
            },
            {
              text: "Build Image",
              link: "/projects/gardenlinux/developers/build_image",
            },
            {
              text: "Build OpenStack Image",
              link: "/projects/gardenlinux/developers/build_image_openstack",
            },
            {
              text: "Build Packages",
              link: "/projects/gardenlinux/developers/build_packages",
            },
            {
              text: "Test Image",
              link: "/projects/gardenlinux/developers/test_image",
            },
            {
              text: "Contributing",
              link: "/projects/gardenlinux/developers/contributing",
            },
            {
              text: "Bare Container",
              link: "/projects/gardenlinux/developers/bare_container",
            },
            {
              text: "GitHub Pipelines",
              link: "/projects/gardenlinux/developers/github_pipelines",
            },
            {
              text: "VMware OVA",
              link: "/projects/gardenlinux/developers/vmware-ova",
            },
          ],
        },
        {
          text: "Operators",
          collapsed: false,
          items: [
            { text: "Overview", link: "/projects/gardenlinux/operators/index" },
            {
              text: "APT Repository",
              link: "/projects/gardenlinux/operators/apt_repo",
            },
            {
              text: "AWS Secure Boot",
              link: "/projects/gardenlinux/operators/deployment/aws-secureboot",
            },
            {
              text: "GCP Secure Boot",
              link: "/projects/gardenlinux/operators/deployment/gcp-secureboot",
            },
            {
              text: "Non-Default Install",
              link: "/projects/gardenlinux/operators/deployment/install-non-default",
            },
            {
              text: "iPXE Install",
              link: "/projects/gardenlinux/operators/deployment/ipxe-install",
            },
            {
              text: "Gardener Kernel Restart",
              link: "/projects/gardenlinux/operators/gardener-kernel-restart",
            },
            {
              text: "Lima VM",
              link: "/projects/gardenlinux/operators/lima-vm",
            },
            {
              text: "Local K8s with Lima",
              link: "/projects/gardenlinux/operators/local-k8s-lima",
            },
            {
              text: "SSH Hardening",
              link: "/projects/gardenlinux/operators/ssh-hardening",
            },
            {
              text: "Time Configuration",
              link: "/projects/gardenlinux/operators/time-configuration",
            },
          ],
        },
      ],

      // Builder project docs
      "/projects/builder/": [
        {
          text: "Builder",
          items: [
            {
              text: "Getting Started",
              link: "/projects/builder/getting_started",
            },
            { text: "Features", link: "/projects/builder/features" },
          ],
        },
      ],

      // Python library project docs
      "/projects/python-gardenlinux-lib/": [
        {
          text: "Python Garden Linux Library",
          items: [
            { text: "Overview", link: "/projects/python-gardenlinux-lib/" },
          ],
        },
      ],
    },

    socialLinks: [{ icon: "github", link: "https://github.com/gardenlinux" }],

    search: {
      provider: "local",
    },
  },
});
