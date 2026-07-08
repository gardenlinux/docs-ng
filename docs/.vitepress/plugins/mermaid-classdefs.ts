import type MarkdownIt from 'markdown-it'

/**
 * Shared classDef preamble injected into flowchart/graph mermaid fence blocks.
 *
 * Five canonical semantic categories:
 *   decision – conditional branches, diamond nodes
 *   input    – triggers, external sources
 *   process  – intermediate work, retries
 *   output   – successful terminal, published artefacts
 *   neutral  – sequential steps with no special role
 *
 * Authors use `class NodeA,NodeB neutral` in their diagrams and never
 * write hex color codes directly.
 *
 * Colors (both light-mode and dark-mode palettes) are defined in
 * docs/.vitepress/theme/style.css under the "Mermaid canonical classes"
 * section. The classDef lines below use only opacity:1 (a visually inert
 * no-op) so that mermaid does NOT emit fill/stroke/color/stroke-width
 * !important rules from classDef. The class name itself is what matters:
 * mermaid attaches the class name to the node's <g> element, and the
 * external CSS uses !important to beat the theme's SVG-scoped id-selector
 * rules (e.g. "#mermaid-123 .node rect { fill: ... }") that would otherwise
 * take precedence over plain class selectors.
 */
const CLASSDEFS_PREAMBLE =
    '    classDef decision opacity:1;\n' +
    '    classDef input    opacity:1;\n' +
    '    classDef process  opacity:1;\n' +
    '    classDef output   opacity:1;\n' +
    '    classDef neutral  opacity:1;\n'

/**
 * markdown-it plugin that injects shared mermaid classDef declarations
 * into every fenced flowchart/graph code block, inserted after the
 * diagram-type declaration line.
 *
 * Only `flowchart` and `graph` diagram types are modified; other types
 * (`sequenceDiagram`, `gantt`, `%%{init}%%`, etc.) are left untouched
 * because `classDef` is not valid syntax for those diagram types.
 *
 * Registration in VitePress config.mts:
 *
 *   import { mermaidClassDefs } from './plugins/mermaid-classdefs.js'
 *
 *   export default defineConfig({
 *     markdown: {
 *       config: (md) => md.use(mermaidClassDefs),
 *     },
 *   })
 */
export function mermaidClassDefs(md: MarkdownIt): void {
    // Must register after 'block' — that is the rule which parses fence tokens.
    // Registering after 'normalize' fires too early (tokens are empty at that point).
    md.core.ruler.after('block', 'mermaid-classdefs', (state) => {
        for (const token of state.tokens) {
            if (token.type !== 'fence') continue
            if (token.info.trim() !== 'mermaid') continue

            // Only inject into flowchart/graph diagrams; classDef is not
            // valid in sequenceDiagram, gantt, %%{init}%% blocks, etc.
            const firstLine = token.content.split('\n')[0].trim().toLowerCase()
            if (!firstLine.startsWith('flowchart') && !firstLine.startsWith('graph ')) continue

            // Insert preamble after the diagram-type declaration line so
            // the diagram-type keyword remains first (required by mermaid).
            const nl = token.content.indexOf('\n')
            token.content = nl === -1
                ? token.content + '\n' + CLASSDEFS_PREAMBLE
                : token.content.slice(0, nl + 1) + CLASSDEFS_PREAMBLE + token.content.slice(nl + 1)
        }
    })
}
