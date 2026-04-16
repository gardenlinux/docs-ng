import { defineConfig } from "vitepress";
import { generateDocumentationSidebar } from "./sidebar.js";
import { readdir, readFile } from "fs/promises";
import { join } from "path";
import matter from "gray-matter";

// Get base URL from environment variable (for GitHub Pages deployment)
const base = process.env.BASE_URL || "/";

// Generate sidebar dynamically at build time
const documentationSidebar = generateDocumentationSidebar();

// Build a map of URL -> { title, description, url } for all markdown pages
async function buildPageMap(pagesDir: string): Promise<Record<string, { title: string; description: string; url: string }>> {
  const map: Record<string, { title: string; description: string; url: string }> = {};
  const skipDirs = ['.vitepress', 'node_modules', 'dist', '_build', '.venv'];

  async function scanDir(dir: string, basePath: string = "") {
    const dirName = dir.split('/').pop() || '';
    if (skipDirs.includes(dirName)) {
      return;
    }
    
    try {
      const entries = await readdir(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = join(dir, entry.name);
        if (entry.isDirectory()) {
          await scanDir(fullPath, basePath + entry.name + "/");
        } else if (entry.name.endsWith(".md")) {
          try {
            const content = await readFile(fullPath, "utf-8");
            const { data } = matter(content);
            let url = basePath + entry.name.replace(/\.md$/, ".html");
            url = url.replace(/\/index\.html$/, "/");
            if (!url.startsWith("/")) {
              url = "/" + url;
            }
            map[url] = {
              title: data.title || entry.name.replace(/\.md$/, ""),
              description: data.description || "",
              url,
            };
          } catch (e) {
            // Skip files that can't be read
          }
        }
      }
    } catch (e) {
      // Skip directories that can't be read
    }
  }

  await scanDir(pagesDir);
  return map;
}

// Normalize a related_topics path to a URL
function normalizeUrl(ref: string): string {
  // Remove .md extension if present
  let url = ref.replace(/\.md$/, "");
  // If no extension and no trailing slash, add .html
  if (!url.endsWith("/") && !url.includes(".")) {
    url = url + ".html";
  }
  // Handle /index paths
  url = url.replace(/\/index\.html$/, "/");
  // Ensure leading slash
  if (!url.startsWith("/")) {
    url = "/" + url;
  }
  return url;
}

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
    // Ignore specific release notes pages that don't exist
    /release-notes\/1592-17/,
    /release-notes\/1877-11/,
    /release-notes\/1877-12/,
    // Ignore LICENSE files (e.g. from aggregated repos)
    /LICENSE$/,
    // Ignore broken links inside features for now
    /features\/_ephemeral/,
    /features\/_tpm2/,
    /features\/bare/,
    /features\/libc/,
    /test\//,
    /tests\//,
    /samples\//,
    /boot_modes/,
    /cis\//,
    /firewall\//,
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
        if (
          frontmatter.github_org &&
          frontmatter.github_repo &&
          frontmatter.github_source_path
        ) {
          const branch = frontmatter.github_branch || "main";
          return `https://github.com/${frontmatter.github_org}/${frontmatter.github_repo}/edit/${branch}/${frontmatter.github_source_path}`;
        }
        // Fallback for pages native to docs-ng (no GitHub metadata)
        return `https://github.com/gardenlinux/docs-ng/edit/main/docs/${filePath}`;
      },
      text: "Edit this page on GitHub",
    },

    search: {
      provider: "local",
    },
  },
  async transformPageData(pageData, { siteConfig }) {
    // Build page map - NOT cached globally due to VitePress config execution issues
    const pagesDir = siteConfig.root;
    const pageMap = await buildPageMap(pagesDir);
    
    // Resolve related_topics if present
    const relatedTopics = pageData.frontmatter?.related_topics;
    if (relatedTopics && Array.isArray(relatedTopics)) {
      // Get current page URL
      let currentPageUrl = "/" + pageData.relativePath.replace(/\.md$/, ".html");
      currentPageUrl = currentPageUrl.replace(/\/index\.html$/, "/");
      
      pageData.frontmatter.resolvedRelated = relatedTopics
        .map((ref: string) => {
          // Normalize the file path to URL
          const url = normalizeUrl(ref);
          const page = pageMap[url];

          // ERROR: File not found
          if (!page) {
            throw new Error(
              `RelatedTopics: File not found "${ref}" (resolved to "${url}") in ${pageData.relativePath}`
            );
          }

          // ERROR: Title missing in frontmatter
          if (!page.title) {
            throw new Error(
              `RelatedTopics: File "${ref}" has no title in frontmatter (in ${pageData.relativePath})`
            );
          }

          // OK: Description is optional
          return {
            url,
            title: page.title,
            description: page.description || "",
          };
        })
        .filter((page) => page.url !== currentPageUrl); // Remove self-references
    }
  },
});
