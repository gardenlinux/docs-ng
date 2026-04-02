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
  
  // Post-process sidebar to fix folder titles and extract descriptions from frontmatter
  const fixFolderTitles = (items: any[]): any[] => {
    return items.map(item => {
      let frontmatter: Record<string, any> | undefined;

      if (item.link && item.link.endsWith('/')) {
        // This is a folder link - read frontmatter from its index.md
        const indexPath = path.join('docs', item.link, 'index.md');
        if (fs.existsSync(indexPath)) {
          try {
            const content = fs.readFileSync(indexPath, 'utf-8');
            frontmatter = matter(content).data;
            if (frontmatter?.title) {
              item.text = frontmatter.title;
            }
          } catch (err) {
            // Ignore errors, keep the original text
          }
        }
      } else if (item.link && item.link.endsWith('.md')) {
        // This is a file link - read frontmatter from the page
        const pagePath = path.join('docs', item.link);
        if (fs.existsSync(pagePath)) {
          try {
            const content = fs.readFileSync(pagePath, 'utf-8');
            frontmatter = matter(content).data;
          } catch (err) {
            // Ignore errors
          }
        }
      } else if (item.link && !item.link.includes('.')) {
        // Link has no extension (vitepress-sidebar strips .md for leaf pages)
        // Try appending .md to find the source file
        const pagePath = path.join('docs', item.link + '.md');
        if (fs.existsSync(pagePath)) {
          try {
            const content = fs.readFileSync(pagePath, 'utf-8');
            frontmatter = matter(content).data;
          } catch (err) {
            // Ignore errors
          }
        }
      }

      if (frontmatter?.description) {
        item.description = frontmatter.description;
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
