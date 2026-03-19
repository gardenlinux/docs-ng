// https://vitepress.dev/guide/custom-theme
import { h } from "vue";
import type { Theme } from "vitepress";
import DefaultTheme from "vitepress/theme";
import "./style.css";
import VPFooter from "./components/VPFooter.vue";
import TaxonomyIndex from "./components/TaxonomyIndex.vue";

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      "doc-before": () => h(TaxonomyIndex),
      "layout-bottom": () => h(VPFooter),
    });
  },
  enhanceApp({ app }) {
    app.component(
      "YouTubeVideo",
      () => import("./components/YouTubeVideo.vue")
    );
    app.component(
      "ThemedTeamMembers",
      () => import("./components/ThemedTeamMembers.vue")
    );
  },
} satisfies Theme;
