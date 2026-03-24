import { generateSidebar } from 'vitepress-sidebar';

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
  
  // vitepress-sidebar returns an array, but we need an object with path keys
  // Wrap the array result in an object with the root path
  return {
    '/': sidebar
  };
}
