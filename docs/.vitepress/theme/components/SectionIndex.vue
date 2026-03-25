<script setup lang="ts">
import { useData } from "vitepress";
import { computed } from "vue";

const { page, theme } = useData();

interface SidebarItem {
  text: string;
  link?: string;
  items?: SidebarItem[];
}

interface TreeNode {
  text: string;
  link?: string;
  depth: number;
  children?: TreeNode[];
}

// Get the current directory path from the current page
// e.g., 'how-to/' for how-to/index.md or 'how-to/platform-specific/' for how-to/platform-specific/index.md
const currentDirectory = computed(() => {
  const path = page.value.relativePath;
  // Remove /index.md or .md and get directory path
  const dirPath = path.replace(/\/index\.md$/, "").replace(/\.md$/, "");
  // If it's a directory, add trailing slash
  return dirPath ? dirPath + "/" : "";
});

// Find items in the current section/subsection from sidebar and build a tree structure
const sectionItems = computed(() => {
  const sidebar = theme.value.sidebar;
  if (!sidebar || !sidebar["/"]) {
    return [];
  }

  const sidebarGroups = sidebar["/"];
  const currentPagePath = page.value.relativePath.replace(/\.md$/, "");
  const targetPath = currentDirectory.value;

  // Recursively search for the sidebar node matching our current directory
  const findMatchingNode = (
    items: SidebarItem[],
    searchPath: string
  ): SidebarItem | null => {
    for (const item of items) {
      // Check if this item's link matches our target path
      if (item.link) {
        const itemPath =
          item.link.replace(/\.md$/, "").replace(/\/index$/, "") + "/";
        if (itemPath === searchPath) {
          return item;
        }
      }

      // Recursively search in children
      if (item.items && item.items.length > 0) {
        const found = findMatchingNode(item.items, searchPath);
        if (found) return found;
      }
    }
    return null;
  };

  // Find the node matching our current directory
  let matchingNode: SidebarItem | null = null;

  for (const group of sidebarGroups) {
    // Check if the group itself matches
    if (group.link) {
      const groupPath =
        group.link.replace(/\.md$/, "").replace(/\/index$/, "") + "/";
      if (groupPath === targetPath) {
        matchingNode = group;
        break;
      }
    }

    // Search in group items
    if (group.items) {
      matchingNode = findMatchingNode(group.items, targetPath);
      if (matchingNode) break;
    }
  }

  if (!matchingNode || !matchingNode.items) {
    return [];
  }

  // Build a tree structure preserving hierarchy up to 3 levels

  const buildTree = (items: SidebarItem[], depth: number = 0): TreeNode[] => {
    if (depth >= 3) {
      // Flatten any items beyond level 3
      const flattened: TreeNode[] = [];
      for (const item of items) {
        if (item.link && item.link !== currentPagePath) {
          let formattedLink = item.link
            .replace(/\.md$/, "")
            .replace(/\/index$/, "");
          if (!formattedLink.startsWith("/")) {
            formattedLink = "/" + formattedLink;
          }
          flattened.push({
            text: item.text,
            link: formattedLink,
            depth: 2, // Treat as depth 2 (child of sub-group)
          });
        }
        if (item.items) {
          flattened.push(...buildTree(item.items, depth + 1));
        }
      }
      return flattened;
    }

    const nodes: TreeNode[] = [];

    for (const item of items) {
      // Skip the current page itself
      if (item.link === currentPagePath) {
        continue;
      }

      // If this item has children, it's a group/sub-group
      if (item.items && item.items.length > 0) {
        const children = buildTree(item.items, depth + 1);
        // Only include the group if it has valid children
        if (children.length > 0) {
          // Format link: remove .md and add leading slash
          let formattedLink = item.link;
          if (formattedLink) {
            formattedLink = formattedLink
              .replace(/\.md$/, "")
              .replace(/\/index$/, "");
            if (!formattedLink.startsWith("/")) {
              formattedLink = "/" + formattedLink;
            }
          }
          nodes.push({
            text: item.text,
            link: formattedLink,
            depth,
            children,
          });
        }
      } else if (item.link) {
        // This is a leaf item - format link properly
        let formattedLink = item.link
          .replace(/\.md$/, "")
          .replace(/\/index$/, "");
        if (!formattedLink.startsWith("/")) {
          formattedLink = "/" + formattedLink;
        }
        nodes.push({
          text: item.text,
          link: formattedLink,
          depth,
        });
      }
    }

    return nodes;
  };

  return buildTree(matchingNode.items);
});

const sectionName = computed(() => {
  // Get the last segment of the directory path for the section name
  const dir = currentDirectory.value.replace(/\/+$/, "");
  const segments = dir.split("/");
  const lastSegment = segments[segments.length - 1] || "";
  return lastSegment.charAt(0).toUpperCase() + lastSegment.slice(1);
});
</script>

<template>
  <div class="section-index">
    <h2>Available {{ sectionName }} documentation</h2>
    <div v-if="sectionItems.length > 0" class="section-tree">
      <!-- Recursive rendering of tree nodes -->
      <template v-for="node in sectionItems" :key="node.link || node.text">
        <!-- Leaf node at depth 0 (top-level item) -->
        <div
          v-if="!node.children"
          class="section-item"
          :class="`depth-${node.depth}`">
          <a :href="node.link">{{ node.text }}</a>
        </div>

        <!-- Group node (has children) -->
        <div v-else class="section-group" :class="`depth-${node.depth}`">
          <!-- Group header -->
          <div class="section-group-header">
            <a v-if="node.link" :href="node.link" class="group-link">{{
              node.text
            }}</a>
            <span v-else class="group-title">{{ node.text }}</span>
          </div>

          <!-- Group children -->
          <div class="section-group-children">
            <template
              v-for="child in node.children"
              :key="child.link || child.text">
              <!-- Child leaf node -->
              <div
                v-if="!child.children"
                class="section-item"
                :class="`depth-${child.depth}`">
                <a :href="child.link">{{ child.text }}</a>
              </div>

              <!-- Child group node (level 3) -->
              <div v-else class="section-group" :class="`depth-${child.depth}`">
                <div class="section-group-header">
                  <a v-if="child.link" :href="child.link" class="group-link">{{
                    child.text
                  }}</a>
                  <span v-else class="group-title">{{ child.text }}</span>
                </div>

                <!-- Level 3 children -->
                <div class="section-group-children">
                  <div
                    v-for="grandchild in child.children"
                    :key="grandchild.link || grandchild.text"
                    class="section-item"
                    :class="`depth-${grandchild.depth}`">
                    <a :href="grandchild.link">{{ grandchild.text }}</a>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </template>
    </div>
    <div v-else class="section-empty">
      <p>No documentation available yet in this section.</p>
      <p class="section-empty-hint">
        Content will appear here after running aggregation to populate this
        section with documentation from source repositories.
      </p>
    </div>
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

.section-tree {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Top-level items (depth 0) - displayed as grid */
.section-item.depth-0 {
  display: inline-block;
}

/* Create a grid container for top-level items */
.section-tree > .section-item.depth-0 {
  display: block;
}

/* Group for depth 0 and 1 items at the root level */
.section-tree {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.5rem;
}

/* Group containers should span full width */
.section-group {
  grid-column: 1 / -1;
  margin-top: 1rem;
}

.section-group.depth-0 {
  margin-top: 1.5rem;
}

.section-group.depth-1 {
  margin-top: 1rem;
  margin-left: 1rem;
}

/* Group headers */
.section-group-header {
  margin-bottom: 0.75rem;
}

.section-group.depth-0 .section-group-header {
  font-size: 1.2rem;
  font-weight: 600;
  padding: 0.5rem 0;
}

.section-group.depth-1 .section-group-header {
  font-size: 1.05rem;
  font-weight: 500;
  padding: 0.4rem 0;
  padding-left: 1rem;
  opacity: 0.9;
}

.section-group-header .group-link {
  color: var(--vp-c-text-1);
  text-decoration: none;
  transition: color 0.2s;
}

.section-group-header .group-link:hover {
  color: var(--vp-c-brand-1);
}

.section-group-header .group-title {
  color: var(--vp-c-text-1);
}

/* Group children containers */
.section-group-children {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.5rem;
}

.section-group.depth-1 .section-group-children {
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.4rem;
}

/* Nested groups in children should span full width */
.section-group-children > .section-group {
  grid-column: 1 / -1;
}

/* Section items (leaf nodes) */
.section-item a {
  display: block;
  padding: 0.5rem 0.75rem;
  color: var(--vp-c-brand-1);
  text-decoration: none;
  font-size: 1rem;
  border-radius: 4px;
  transition: all 0.2s;
  border: 1px solid var(--vp-c-divider);
}

.section-item a:hover {
  background-color: var(--vp-c-bg-soft);
  border-color: var(--vp-c-brand-1);
  transform: translateX(2px);
}

/* Depth-specific styling for items */
.section-item.depth-1 a {
  font-size: 0.95rem;
  padding: 0.45rem 0.7rem;
}

.section-item.depth-2 a {
  font-size: 0.9rem;
  padding: 0.4rem 0.65rem;
  border-color: var(--vp-c-divider-light);
  opacity: 0.95;
}

.section-empty {
  padding: 2rem;
  background-color: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  text-align: center;
}

.section-empty p {
  margin: 0.5rem 0;
  color: var(--vp-c-text-2);
}

.section-empty-hint {
  font-size: 0.9rem;
  font-style: italic;
  color: var(--vp-c-text-3);
}
</style>
