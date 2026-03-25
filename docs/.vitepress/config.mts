import { defineConfig } from "vitepress";
import { generateDocumentationSidebar } from "./sidebar.js";

// Get base URL from environment variable (for GitHub Pages deployment)
const base = process.env.BASE_URL || "/";

// Generate sidebar dynamically at build time
const documentationSidebar = generateDocumentationSidebar();

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
    // Ignore section index links without trailing slash (VitePress internal)
    /\/tutorials\/index$/,
    /\/how-to\/index$/,
    /\/explanation\/index$/,
    /\/reference\/index$/,
    /\/contributing\/index$/,
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

    sidebar: documentationSidebar,

    socialLinks: [{ icon: "github", link: "https://github.com/gardenlinux" }],

    editLink: {
      pattern: ({ filePath, frontmatter }) => {
        // If page has GitHub metadata from aggregated content, use it
        if (frontmatter.github_org && frontmatter.github_repo && frontmatter.github_source_path) {
          const branch = frontmatter.github_branch || 'main';
          return `https://github.com/${frontmatter.github_org}/${frontmatter.github_repo}/edit/${branch}/${frontmatter.github_source_path}`;
        }
        // Fallback for pages native to docs-ng (no GitHub metadata)
        return `https://github.com/gardenlinux/docs-ng/edit/main/docs/${filePath}`;
      },
      text: 'Edit this page on GitHub'
    },

    search: {
      provider: "local",
    },
  },
});
