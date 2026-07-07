import type MarkdownIt from 'markdown-it'

/**
 * Shared classDef preamble injected into flowchart/graph mermaid fence blocks.
 *
 * Five canonical semantic categories:
 *   decision – conditional branches, diamond nodes      (blue)
 *   input    – triggers, external sources               (yellow/amber)
 *   process  – intermediate work, retries               (gray)
 *   output   – successful terminal, published artefacts (green)
 *   neutral  – sequential steps with no special role    (violet)
 *
 * Authors use `class NodeA,NodeB neutral` in their diagrams and never
 * write hex color codes directly. All color definitions live here.
 */
const CLASSDEFS_PREAMBLE =
    '    classDef decision fill:#e1f5ff,stroke:#3b82f6,color:#0b1e3a;\n' +
    '    classDef input    fill:#fff4e1,stroke:#d97706,color:#3a2408;\n' +
    '    classDef process  fill:#f0f0f0,stroke:#6b7280,color:#111827;\n' +
    '    classDef output   fill:#d4edda,stroke:#16a34a,color:#0b2e13;\n' +
    '    classDef neutral  fill:#f0e6ff,stroke:#7c3aed,color:#1e0a3c;\n'

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
