<script setup lang="ts">
import { useData } from 'vitepress';
import { computed } from 'vue';

const { page, theme } = useData();

interface SidebarItem {
  text: string;
  link?: string;
  items?: SidebarItem[];
}

// Get the current section path (e.g., '/tutorials/', '/how-to/')
const currentSection = computed(() => {
  const path = page.value.relativePath;
  const match = path.match(/^([^/]+)\//);
  return match ? `/${match[1]}/` : '/';
});

// Find items in the current section from sidebar
const sectionItems = computed(() => {
  const sidebar = theme.value.sidebar;
  if (!sidebar || !sidebar['/']) {
    return [];
  }

  // The sidebar is an array of groups
  const sidebarGroups = sidebar['/'];
  
  // Find the group that matches our section
  const currentGroup = sidebarGroups.find((group: any) => {
    // Check if this group's link or items match our section
    return group.link?.startsWith(currentSection.value) || 
           group.items?.some((item: SidebarItem) => 
             item.link?.startsWith(currentSection.value)
           );
  });

  if (!currentGroup?.items) {
    return [];
  }

  // Filter out the index page itself and collect all items
  const items: Array<{ text: string; link: string }> = [];
  
  const processItems = (itemList: SidebarItem[]) => {
    for (const item of itemList) {
      if (item.link && item.link !== currentSection.value && item.link.startsWith(currentSection.value)) {
        items.push({
          text: item.text,
          link: item.link,
        });
      }
      if (item.items) {
        processItems(item.items);
      }
    }
  };

  processItems(currentGroup.items);
  return items;
});

const sectionName = computed(() => {
  const section = currentSection.value.replace(/\//g, '');
  return section.charAt(0).toUpperCase() + section.slice(1).replace(/-/g, ' ');
});
</script>

<template>
  <div v-if="sectionItems.length > 0" class="section-index">
    <h2>Available {{ sectionName }}</h2>
    <ul class="section-list">
      <li v-for="item in sectionItems" :key="item.link">
        <a :href="item.link">{{ item.text }}</a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.section-index {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.section-index h2 {
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.25;
  margin-bottom: 1rem;
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 2rem;
}

.section-list {
  list-style: none;
  padding-left: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.5rem;
}

.section-list li {
  margin: 0;
}

.section-list a {
  display: block;
  padding: 0.5rem 0.75rem;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  font-size: 1rem;
  border-radius: 4px;
  transition: all 0.2s;
  border: 1px solid var(--vp-c-divider);
}

.section-list a:hover {
  background-color: var(--vp-c-bg-soft);
  border-color: var(--vp-c-brand-1);
  transform: translateX(2px);
}
</style>