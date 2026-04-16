import { h, nextTick, watch } from 'vue'
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'
import { createMermaidRenderer } from 'vitepress-mermaid-renderer'
import './style.css'
import SectionIndex from './components/SectionIndex.vue'
import RelatedTopics from './components/RelatedTopics.vue'

export default {
  extends: DefaultTheme,
  Layout: () => {
    const { isDark } = useData()

    const initMermaid = () => {
      createMermaidRenderer({
        // Use base theme; colors are set inline per diagram
        theme: isDark.value ? 'dark' : 'default',
      })
    }

    nextTick(() => initMermaid())

    watch(
      () => isDark.value,
      () => {
        initMermaid()
      }
    )

    return h(DefaultTheme.Layout)
  },
  enhanceApp({ app }) {
    app.component('SectionIndex', SectionIndex)
    app.component('RelatedTopics', RelatedTopics)
  },
} satisfies Theme
