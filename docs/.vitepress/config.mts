import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Gardenlinux Documentation",
  description: "All your documentation need - in one place",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Quick Start', link: '/quickstart' },
      { 
        text: 'Docs',
        items: [
          {
            text: 'Usage Docs',
            items: [
              { text: 'Installation Guide', link: '/usage/installation' },
              { text: 'Build an Image', link: '/usage/build-image' }
            ]
          },
          {
            text: 'Technical Documentation',
            items: [
              { text: 'Technical Docs', link: '/technical/' }
            ]
          },
          {
            text: 'Contributing',
            items: [
              { text: 'Development Environment', link: '/contributing/dev-environment' },
              { text: 'Building an Image', link: '/contributing/building-image' },
              { text: 'Testing an Image', link: '/contributing/testing-image' },
              { text: 'Contribution Workflow', link: '/contributing/workflow' },
              { text: 'Code Style', link: '/contributing/code-style' },
              { text: 'Dependency Policy', link: '/contributing/dependency-policy' },
              { text: 'Documentation Guide', link: '/contributing/documentation-guide' }
            ]
          }
        ]
      },
      { text: 'Examples', link: '/markdown-examples' }
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Quick Start', link: '/quickstart' }
        ]
      },
      {
        text: 'Usage Docs',
        items: [
          { text: 'Installation Guide', link: '/usage/installation' },
          { text: 'Build an Image', link: '/usage/build-image' }
        ]
      },
      {
        text: 'Technical Documentation',
        items: [
          { text: 'Technical Docs', link: '/technical/' }
        ]
      },
      {
        text: 'Examples',
        items: [
          { text: 'Markdown Examples', link: '/markdown-examples' },
          { text: 'Runtime API Examples', link: '/api-examples' }
        ]
      },
      {
        text: 'Contributing',
        collapsed: true,
        items: [
          { text: 'Development Environment', link: '/contributing/dev-environment' },
          { text: 'Building an Image', link: '/contributing/building-image' },
          { text: 'Testing an Image', link: '/contributing/testing-image' },
          { text: 'Contribution Workflow', link: '/contributing/workflow' },
          { text: 'Code Style', link: '/contributing/code-style' },
          { text: 'Dependency Policy', link: '/contributing/dependency-policy' },
          { text: 'Documentation Guide', link: '/contributing/documentation-guide' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
    ]
  }
})
