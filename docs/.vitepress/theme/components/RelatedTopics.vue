<script setup lang="ts">
import { useData } from 'vitepress'
import { computed } from 'vue'

const { frontmatter } = useData()

const relatedPages = computed(() => {
  return frontmatter.value.resolvedRelated || []
})
</script>

<template>
  <div v-if="relatedPages.length" class="related-topics">
    <ul>
      <li v-for="(page, index) in relatedPages" :key="index">
        <a :href="page.url" class="topic-link">
          <span class="topic-title">{{ page.title }}</span>
          <span v-if="page.description" class="topic-description">{{ page.description }}</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.related-topics {
  margin-top: 1.25rem;
}

.related-topics h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.related-topics ul {
  list-style: disc;
  padding-left: 1.25rem;
  margin: 0;
}

.related-topics li {
  margin-bottom: 0.5rem;
}

.related-topics a.topic-link {
  display: block;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  line-height: 1.4;
}

.related-topics a.topic-link:hover {
  text-decoration: underline;
}

.related-topics .topic-title {
  font-weight: 500;
}

.related-topics .topic-description {
  display: block;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-top: 0.1rem;
}
</style>
