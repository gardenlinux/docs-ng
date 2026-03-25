import { generateSidebar } from 'vitepress-sidebar';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export function generateDocumentationSidebar(): any {
  const sidebar = generateSidebar({
    documentRootPath: 'docs',
    scanStartPath: '',
    resolvePath: '/',
    collapsed: true,
    useTitleFromFileHeading: true,
    useTitleFromFrontmatter: true,
    useFolderLinkFromIndexFile: true,
    useFolderTitleFromIndexFile: true,
    excludePattern: ['projects'],
    sortMenusByFrontmatterOrder: true,
    frontmatterOrderDefaultValue: 999,
    prefixSeparator: '/',
  });
  
  // Post-process sidebar to fix folder titles for single-file directories
  // When a folder only has index.md, vitepress-sidebar may not apply the frontmatter title correctly
  const fixFolderTitles = (items: any[]): any[] => {
    return items.map(item => {
      if (item.link && item.link.endsWith('/')) {
        // This is a folder link - try to read title from its index.md
        const indexPath = path.join('docs', item.link, 'index.md');
        if (fs.existsSync(indexPath)) {
          try {
            const content = fs.readFileSync(indexPath, 'utf-8');
            const { data } = matter(content);
            if (data.title) {
              item.text = data.title;
            }
          } catch (err) {
            // Ignore errors, keep the original text
          }
        }
      }
      
      // Recursively fix nested items
      if (item.items && Array.isArray(item.items)) {
        item.items = fixFolderTitles(item.items);
      }
      
      return item;
    });
  };
  
  const fixedSidebar = fixFolderTitles(sidebar);
  
  // vitepress-sidebar returns an array, but we need an object with path keys
  // Wrap the array result in an object with the root path
  return {
    '/': fixedSidebar
  };
}
