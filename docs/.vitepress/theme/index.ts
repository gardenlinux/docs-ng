import DefaultTheme from 'vitepress/theme'
import './style.css'
import SectionIndex from './components/SectionIndex.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('SectionIndex', SectionIndex)
  }
}
