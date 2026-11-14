#!/usr/bin/env python3
"""
Convert doc.tex into a single-page navigable HTML documentation site.

Reads the LaTeX source, splits it into sections, converts markup to
Markdown (rendered client-side by marked.js + MathJax), and emits
docs/index.html with a sidebar, prev/next navigation, and responsive
mobile layout.

Usage:
    python3 tex2html.py                  # reads doc.tex, writes docs/index.html
    python3 tex2html.py input.tex        # custom input
    python3 tex2html.py input.tex out/   # custom input and output directory
"""

import html as html_lib
import re
import sys
import os
import subprocess
import tempfile
import textwrap


# ── Helpers: nested braces, protected spans ──────────────────────────

def brace_arg(s: str, open_idx: int) -> tuple[str, int]:
    """Return the content of the {...} group opening at s[open_idx], nested
    braces included, and the index just after its closing brace.  (A lazy
    regex such as \\caption\\{(.+?)\\} stops at the first '}', which cut
    captions in the middle of h_{\\text{hold}}.)"""
    depth, i = 0, open_idx
    while i < len(s):
        ch = s[i]
        if ch == '\\':
            i += 2
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return s[open_idx + 1:i], i + 1
        i += 1
    raise ValueError(f'unbalanced braces after: {s[open_idx:open_idx + 60]!r}')


def command_arg(s: str, cmd: str) -> str | None:
    """Argument of the first \\cmd{...} in s, or None."""
    m = re.search(r'\\' + cmd + r'\s*\{', s)
    return brace_arg(s, m.end() - 1)[0] if m else None


# Math is left to MathJax untouched: the text substitutions below (--, ~, \,)
# would otherwise rewrite it.  Display math first, then inline math.
MATH_RE = re.compile(r'\$\$.*?\$\$|(?<!\\)\$(?:\\.|[^$\\])+?\$', re.DOTALL)


def protect(s: str, pattern, store: list, tag: str) -> str:
    """Replace each match of pattern by a private-use placeholder."""
    def keep(m):
        store.append(m.group(0))
        return f'{tag}{len(store) - 1}'
    return pattern.sub(keep, s) if hasattr(pattern, 'sub') else re.sub(pattern, keep, s)


def restore(s: str, store: list, tag: str) -> str:
    return re.sub('' + tag + r'(\d+)' + '', lambda m: store[int(m.group(1))], s)


def latex_unescape(s: str) -> str:
    """Undo LaTeX escapes inside code: \\_ -> _, \\# -> #, etc."""
    return re.sub(r'\\([_#%&{}$])', r'\1', s)


# ── LaTeX to Markdown conversion ─────────────────────────────────────

def strip_preamble(tex: str) -> str:
    """Return everything after \\begin{document} and before \\end{document}."""
    m = re.search(r'\\begin\{document\}', tex)
    if m:
        tex = tex[m.end():]
    m = re.search(r'\\end\{document\}', tex)
    if m:
        tex = tex[:m.start()]
    # Strip \maketitle, \tableofcontents, \clearpage
    tex = re.sub(r'\\maketitle\b', '', tex)
    tex = re.sub(r'\\tableofcontents\b', '', tex)
    tex = re.sub(r'\\clearpage\b', '', tex)
    return tex


STANDALONE_TEMPLATE = r"""\documentclass[tikz,border=5pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usetikzlibrary{calc, angles, quotes, patterns, arrows.meta, decorations.markings, positioning}
\begin{document}
%s
\end{document}
"""


def extract_tikz_figures(tex: str) -> list[dict | None]:
    """Extract all figure environments containing TikZ from the document body."""
    body = strip_preamble(tex)
    figures = []
    for m in re.finditer(
        r'\\begin\{figure\}\[H\](.*?)\\end\{figure\}',
        body, re.DOTALL
    ):
        fig_body = m.group(1)
        tikz_match = re.search(
            r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})',
            fig_body, re.DOTALL
        )
        if not tikz_match:
            figures.append(None)
            continue
        label_match = re.search(r'\\label\{(fig:\w+)\}', fig_body)
        label = label_match.group(1) if label_match else f'fig:{len(figures)}'
        figures.append({
            'tikz': tikz_match.group(1),
            'label': label,
        })
    return figures


def compile_figures(figures: list[dict | None], out_dir: str) -> list[str | None]:
    """Compile TikZ figures to SVG files. Returns list of relative SVG paths."""
    fig_dir = os.path.join(out_dir, 'figures')
    os.makedirs(fig_dir, exist_ok=True)

    svg_paths = []
    for i, fig in enumerate(figures):
        if fig is None:
            svg_paths.append(None)
            continue

        svg_name = f'fig_{i}.svg'
        svg_path = os.path.join(fig_dir, svg_name)
        tex_content = STANDALONE_TEMPLATE % fig['tikz']

        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = os.path.join(tmpdir, 'figure.tex')
            with open(tex_file, 'w') as f:
                f.write(tex_content)

            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'figure.tex'],
                cwd=tmpdir, capture_output=True, text=True
            )
            pdf_file = os.path.join(tmpdir, 'figure.pdf')
            if not os.path.exists(pdf_file):
                print(f"  WARNING: pdflatex failed for figure {i} ({fig['label']})")
                svg_paths.append(None)
                continue

            subprocess.run(
                ['dvisvgm', '--pdf', '--no-fonts', 'figure.pdf', '-o', svg_path],
                cwd=tmpdir, capture_output=True, text=True
            )
            if os.path.exists(svg_path):
                print(f"  {svg_name} <- {fig['label']}")
                svg_paths.append(f'figures/{svg_name}')
            else:
                print(f"  WARNING: dvisvgm failed for figure {i}")
                svg_paths.append(None)

    return svg_paths


def split_sections(body: str) -> list[tuple[str, str]]:
    """Split on \\section{Title} and return [(title, content), ...]."""
    pattern = r'\\section\{([^}]+)\}'
    parts = re.split(pattern, body)
    pre = parts[0].strip()
    sections = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((title, content))
    # Prepend any meaningful content before the first \section to the first section
    if pre and len(pre) > 50 and sections:
        first_title, first_content = sections[0]
        sections[0] = (first_title, pre + '\n\n' + first_content)
    elif pre and len(pre) > 50:
        sections.insert(0, ("Introduction", pre))
    return sections


def convert_section(tex: str, fig_svgs: list[str | None] = None,
                    fig_counter: list[int] = None) -> str:
    """Convert a single section's LaTeX body to Markdown."""
    md = tex
    if fig_svgs is None:
        fig_svgs = []
    if fig_counter is None:
        fig_counter = [0]

    # Remove \label{...}
    md = re.sub(r'\\label\{[^}]*\}', '', md)

    # Remove \noindent
    md = re.sub(r'\\noindent\b\s*', '', md)

    # ── Code listings ────────────────────────────────────────────────
    # Set aside first and restored last: convert_inline() turned the ``
    # of the ``` fences into a typographic quote (“`javascript), so no
    # listing was ever rendered as code.
    code_blocks: list[str] = []
    md = protect(
        md, re.compile(r'\\begin\{lstlisting\}(.*?)\\end\{lstlisting\}', re.DOTALL),
        code_blocks, 'L')
    code_blocks[:] = [
        '\n```javascript\n'
        + re.sub(r'^\\begin\{lstlisting\}(?:\[[^\]]*\])?|\\end\{lstlisting\}$', '', b).strip()
        + '\n```\n'
        for b in code_blocks
    ]

    # ── Figures: include SVG image + numbered caption ───────────────
    def replace_figure(m):
        body = m.group(1)
        idx = fig_counter[0]
        fig_counter[0] += 1

        raw = command_arg(body, 'caption')
        caption = md_inline_to_html(convert_inline(raw.strip())) if raw else ''
        label = f'Figure {idx + 1}.'
        alt = html_lib.escape(re.sub(r'<[^>]+>', '', caption) or label, quote=True)

        svg = fig_svgs[idx] if idx < len(fig_svgs) else None
        if svg:
            parts = ['\n<div style="text-align:center;margin:1.5rem 0">']
            parts.append(f'<img src="{svg}" alt="{alt}" style="max-width:100%">')
            if caption:
                parts.append(f'<br><em><strong>{label}</strong> {caption}</em>')
            parts.append('</div>\n\n')
            return ''.join(parts)

        if raw:
            return f'\n> **{label}** ' + re.sub(r'\s*\n\s*', ' ', convert_inline(raw.strip())) + '\n\n'
        return '\n'

    md = re.sub(
        r'\\begin\{figure\}\[H\](.*?)\\end\{figure\}',
        replace_figure, md, flags=re.DOTALL
    )

    # ── Tables ───────────────────────────────────────────────────────
    md = convert_tables(md)

    # ── Math environments ────────────────────────────────────────────
    # equation -> $$ ... $$
    md = re.sub(
        r'\\begin\{equation\}(.*?)\\end\{equation\}',
        lambda m: '\n$$\n' + clean_math(m.group(1)) + '\n$$\n',
        md, flags=re.DOTALL
    )
    # align / align* -> $$ \begin{aligned} ... \end{aligned} $$
    md = re.sub(
        r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}',
        lambda m: '\n$$\n\\begin{aligned}' + clean_math(m.group(1)) + '\\end{aligned}\n$$\n',
        md, flags=re.DOTALL
    )
    # display math \[ ... \]
    md = re.sub(
        r'\\\[(.*?)\\\]',
        lambda m: '\n$$\n' + clean_math(m.group(1)) + '\n$$\n',
        md, flags=re.DOTALL
    )

    # ── Lists ────────────────────────────────────────────────────────
    md = convert_lists(md)

    # ── Subsections / subsubsections ─────────────────────────────────
    md = re.sub(r'\\subsection\*?\{([^}]+)\}', r'\n## \1\n', md)
    md = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'\n### \1\n', md)

    # ── Inline markup ────────────────────────────────────────────────
    md = convert_inline(md)

    # ── Cleanup ──────────────────────────────────────────────────────
    # Remove leftover LaTeX comments (lines starting with %)
    md = re.sub(r'^%.*$', '', md, flags=re.MULTILINE)
    # Remove decoration lines (═══)
    md = re.sub(r'^[%═─\s]*$', '', md, flags=re.MULTILINE)
    # Collapse multiple blank lines
    md = re.sub(r'\n{4,}', '\n\n\n', md)

    return restore(md, code_blocks, 'L').strip()


def clean_math(s: str) -> str:
    """Clean up math content: remove labels, preserve content."""
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    return s.strip()


def convert_inline(s: str) -> str:
    """Convert inline LaTeX markup to Markdown.  Math ($...$, $$...$$) and
    code spans are set aside so that the text substitutions (--, ~, \\, ...)
    do not rewrite them."""
    # $\times$ -> ×, $\approx$ -> ≈ (whole formulas, before math is set aside)
    s = s.replace('$\\times$', '×')
    s = s.replace('$\\approx$', '≈')
    math: list[str] = []
    s = protect(s, MATH_RE, math, 'M')
    # \texttt{...} and \code{...} and \file{...} -> `...`, LaTeX escapes
    # undone (`click\_value\_mm` showed its backslashes)
    code: list[str] = []
    s = protect(s, re.compile(r'\\(?:texttt|code|file)\{((?:[^{}]|\{[^{}]*\})*)\}'), code, 'C')
    code[:] = ['`' + latex_unescape(re.sub(r'^\\\w+\{|\}$', '', c)) + '`' for c in code]
    # \href{url}{text} -> [text](url), \url{...} -> [url](url)
    s = re.sub(r'\\href\{([^}]*)\}\{([^}]*)\}', r'[\2](\1)', s)
    s = re.sub(r'\\url\{([^}]*)\}', r'[\1](\1)', s)
    s = protect(s, re.compile(r'\[[^\]\n]*\]\([^)\s]*\)'), code, 'C')
    # \textbf{...} -> **...**
    s = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', s)
    # \emph{...} and \textit{...} -> *...*
    s = re.sub(r'\\emph\{([^}]*)\}', r'*\1*', s)
    s = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', s)
    # \key{...} -> **...**
    s = re.sub(r'\\key\{([^}]*)\}', r'**\1**', s)
    # \textcolor{...}{...} -> just the text
    s = re.sub(r'\\textcolor\{[^}]*\}\{([^}]*)\}', r'\1', s)
    # \textsf{...} -> just the text
    s = re.sub(r'\\textsf\{([^}]*)\}', r'\1', s)
    # \cref{...} and \Cref{...} -> *Section Name*
    s = re.sub(r'\\[Cc]ref\{([^}]*)\}', lambda m: cref_replace(m.group(1)), s)
    # \cite{...} -> [keys]; the ~ before it is a space ("is[mccoy]" otherwise)
    s = re.sub(r'~\\cite\{([^}]*)\}', r' [\1]', s)
    s = re.sub(r'\\cite\{([^}]*)\}', r'[\1]', s)
    # --- -> —
    s = s.replace('---', '—')
    # -- -> –
    s = s.replace('--', '–')
    # `` and '' -> "
    s = s.replace("``", "“")
    s = s.replace("''", "”")
    # \, -> thin space (or just space in MD)
    s = re.sub(r'\\,', ' ', s)
    # \; and \: and \! -> space or nothing
    s = re.sub(r'\\[;:!]', ' ', s)
    # \@ -> nothing
    s = re.sub(r'\\@', '', s)
    # ~ -> non-breaking space (just regular space in MD)
    s = s.replace('~', ' ')
    # \% -> %
    s = s.replace('\\%', '%')
    # \S -> §
    s = re.sub(r'\\S(?![A-Za-z])\s*', '§ ', s)
    # Control space "\ " (vs.\ Parallel) -> space; not the "\\ " of a line break
    s = re.sub(r'(?<!\\)\\ ', ' ', s)
    # Remove \noindent
    s = re.sub(r'\\noindent\s*', '', s)
    # Remove remaining \centering
    s = re.sub(r'\\centering\s*', '', s)
    # Remove [nosep]
    s = re.sub(r'\[nosep\]', '', s)

    s = restore(s, code, 'C')
    return restore(s, math, 'M')


# \label key -> readable name, filled by build_label_map() from the document
# itself.  (The map used to be written by hand, copied from the rifle
# simulator: none of this document's labels was in it, so \Cref{fig:cantfig}
# came out as "fig:cantfig".)
CREF_MAP: dict[str, str] = {}


def clean_title(title: str) -> str:
    r"""Section title as displayed (vs.\ Parallel -> vs. Parallel)."""
    return re.sub(r'\s+', ' ', convert_inline(title)).strip()


def build_label_map(body: str) -> dict[str, str]:
    r"""Map each \label to the title of its \section, or to "Figure N" for a
    figure (numbered in order, as in the PDF and in the captions here)."""
    labels: dict[str, str] = {}
    section, figure, in_figure, table, in_table = '', 0, False, 0, False
    for m in re.finditer(r'\\section\{([^}]+)\}|\\(?:begin|end)\{(?:figure|table)\}|\\label\{([^}]+)\}', body):
        tok = m.group(0)
        if m.group(1) is not None:
            section = clean_title(m.group(1))
        elif tok.startswith('\\begin{figure'):
            figure, in_figure = figure + 1, True
        elif tok.startswith('\\end{figure'):
            in_figure = False
        elif tok.startswith('\\begin{table'):
            table, in_table = table + 1, True
        elif tok.startswith('\\end{table'):
            in_table = False
        else:
            key = m.group(2)
            if in_figure and key.startswith('fig:'):
                labels[key] = f'Figure {figure}'
            elif in_table and key.startswith('tab:'):
                labels[key] = f'Table {table}'
            else:
                labels[key] = section
    return labels


def cref_replace(keys: str) -> str:
    """Replace \\cref{key1,key2} with readable names."""
    parts = [k.strip() for k in keys.split(',')]
    names = []
    seen = set()
    for p in parts:
        if p not in CREF_MAP:
            print(f'  WARNING: unknown reference {p!r}')
        name = CREF_MAP.get(p, p)
        if name not in seen:
            names.append(name if name.startswith(('Figure ', 'Table ')) else f'*{name}*')
            seen.add(name)
    return ' and '.join(names) if len(names) <= 2 else ', '.join(names)


def md_inline_to_html(s: str) -> str:
    """Convert markdown bold/italic/code to HTML for use inside HTML elements
    (marked leaves the inside of an HTML block alone).  Math is skipped."""
    math: list[str] = []
    s = protect(s, MATH_RE, math, 'M')
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    s = re.sub(r'`(.+?)`', lambda m: '<code>' + html_lib.escape(m.group(1)) + '</code>', s)
    s = re.sub(r'\[([^\]\n]*)\]\(([^)\s]*)\)', r'<a href="\2">\1</a>', s)
    return restore(s, math, 'M')


TABULAR_RE = re.compile(r'\\begin\{tabular\}\{((?:[^{}]|\{[^{}]*\})*)\}(.*?)\\end\{tabular\}', re.DOTALL)


def convert_tables(md: str) -> str:
    """Convert LaTeX tables to HTML: table floats, and bare tabulars (usually
    inside a center environment), which used to be left as raw LaTeX."""
    pattern = r'\\begin\{table\}\[H\](.*?)\\end\{table\}'
    def numbered(m):
        TABLE_COUNTER[0] += 1
        return _convert_one_table(m.group(1), TABLE_COUNTER[0])
    md = re.sub(pattern, numbered, md, flags=re.DOTALL)
    md = re.sub(
        r'(?:\\begin\{center\}\s*)?(\\begin\{tabular\}.*?\\end\{tabular\})(?:\s*\\end\{center\})?',
        lambda m: _convert_one_table(m.group(1)), md, flags=re.DOTALL)
    return md


# Table floats numbered in document order, as in the PDF; reset before each pass.
TABLE_COUNTER = [0]


def _convert_one_table(body: str, number: int | None = None) -> str:
    """Convert a single table environment body to an HTML table."""
    raw_caption = command_arg(body, 'caption')
    caption = md_inline_to_html(convert_inline(raw_caption.strip())) if raw_caption else ''

    tab_match = TABULAR_RE.search(body)
    if not tab_match:
        return f'\n<p><strong>{caption}</strong></p>\n' if caption else '\n'

    # Column alignment from the spec ({lccc}, {@{}ll@{}}, {|l|r|} ...)
    spec = re.sub(r'@\{[^{}]*\}|[|]', '', tab_match.group(1))
    aligns = [{'l': 'left', 'c': 'center', 'r': 'right'}.get(ch[0], 'left')
              for ch in re.findall(r'[lcrp](?:\{[^{}]*\})?', spec)]

    tab = tab_match.group(2)
    tab = re.sub(r'\\(toprule|midrule|bottomrule|hline)\s*', '', tab)
    tab = re.sub(r'\\(small|centering)\s*', '', tab)

    rows = [r.strip() for r in tab.split('\\\\') if r.strip()]
    if not rows:
        return f'\n<p><strong>{caption}</strong></p>\n' if caption else '\n'

    # A blank-line-free HTML block: marked passes it through untouched.  The
    # wrapper scrolls sideways instead of widening a narrow screen.
    html = '\n\n<div class="table-scroll"><table>\n'
    if caption:
        html += f'<caption><strong>Table{" " + str(number) if number else ""}.</strong> {caption}</caption>\n'

    for i, row in enumerate(rows):
        cells = [md_inline_to_html(convert_inline(c.strip())) for c in re.split(r'(?<!\\)&', row)]
        tag = 'th' if i == 0 else 'td'
        html += '<tr>' + ''.join(
            f'<{tag} style="text-align:{aligns[j] if j < len(aligns) else "left"}">{c}</{tag}>'
            for j, c in enumerate(cells)) + '</tr>\n'

    html += '</table></div>\n\n'
    return html


def convert_lists(md: str) -> str:
    """Convert LaTeX enumerate/itemize to Markdown lists."""
    def replace_list(m):
        env = m.group(1)  # enumerate or itemize
        body = m.group(2)
        items = re.split(r'\\item\s*', body)
        items = [i.strip() for i in items if i.strip()]

        result = '\n'
        for idx, item in enumerate(items):
            item = item.rstrip().rstrip('\\')
            if env == 'enumerate':
                result += f'{idx + 1}. {item}\n'
            else:
                result += f'- {item}\n'
        result += '\n'
        return result

    # Handle nested or sequential lists
    md = re.sub(
        r'\\begin\{(enumerate|itemize)\}(?:\[[^\]]*\])?\s*(.*?)\\end\{\1\}',
        replace_list, md, flags=re.DOTALL
    )
    return md


def convert_bibliography(tex: str) -> list[tuple[str, str]] | None:
    """Extract bibliography entries and return as a section if present."""
    bib_match = re.search(
        r'\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}',
        tex, re.DOTALL
    )
    if not bib_match:
        return None

    body = bib_match.group(1)
    entries = re.findall(r'\\bibitem\{(\w+)\}\s*(.*?)(?=\\bibitem|\Z)', body, re.DOTALL)

    lines = []
    for key, content in entries:
        content = content.strip()
        content = convert_inline(content)
        content = re.sub(r'\s+', ' ', content)
        lines.append(f'- **[{key}]** {content}')

    return '\n'.join(lines)


# ── HTML template ────────────────────────────────────────────────────

HTML_TEMPLATE = '''\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ISSF Rifle Sighting Simulator — Documentation</title>

<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$']],
    displayMath: [['$$', '$$']],
    processEscapes: true
  }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }}
}};
</script>
<script src="vendor/mathjax/tex-chtml.js" async></script>
<script src="vendor/marked/marked.min.js"></script>

<style>
:root {{
  --sidebar-w: 280px;
  --bg: #fafafa;
  --fg: #222;
  --accent: #2563eb;
  --sidebar-bg: #1e293b;
  --sidebar-fg: #cbd5e1;
  --sidebar-active: #60a5fa;
  --border: #e2e8f0;
  --code-bg: #f1f5f9;
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--fg);
  line-height: 1.7;
}}

/* ── Sidebar ───────────────────────────────────────────────── */
#sidebar {{
  position: fixed; top: 0; left: 0;
  width: var(--sidebar-w); height: 100vh;
  background: var(--sidebar-bg);
  color: var(--sidebar-fg);
  overflow-y: auto;
  padding: 1.5rem 0;
  z-index: 10;
  transition: transform .25s;
}}
#sidebar h2 {{
  font-size: .85rem; text-transform: uppercase; letter-spacing: .08em;
  padding: 0 1.2rem .8rem; color: #94a3b8; border-bottom: 1px solid #334155;
  margin-bottom: .6rem;
}}
#sidebar ul {{ list-style: none; }}
#sidebar li a {{
  display: block; padding: .45rem 1.2rem;
  color: var(--sidebar-fg); text-decoration: none;
  font-size: .92rem; border-left: 3px solid transparent;
  transition: background .15s, border-color .15s;
  cursor: pointer;
}}
#sidebar li a:hover {{ background: #334155; }}
#sidebar li a.active {{
  color: var(--sidebar-active); border-left-color: var(--sidebar-active);
  background: rgba(96,165,250,.08);
}}

/* ── Hamburger (mobile) ────────────────────────────────────── */
#menu-btn {{
  display: none; position: fixed; top: .8rem; left: .8rem;
  z-index: 20; background: var(--sidebar-bg); color: #fff;
  border: none; border-radius: 6px; padding: .4rem .6rem;
  font-size: 1.3rem; cursor: pointer;
}}

/* ── Main ──────────────────────────────────────────────────── */
#main {{
  margin-left: var(--sidebar-w);
  max-width: 52rem;
  padding: 2.5rem 2.5rem 6rem;
}}
#main h1 {{ font-size: 1.8rem; margin-bottom: .3rem; }}
#main h2 {{ font-size: 1.35rem; margin-top: 2rem; margin-bottom: .5rem; border-bottom: 1px solid var(--border); padding-bottom: .3rem; }}
#main h3 {{ font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: .4rem; }}
#main p {{ margin: .7rem 0; }}
#main ol, #main ul {{ margin: .5rem 0 .5rem 1.6rem; }}
#main li {{ margin: .25rem 0; }}
#main blockquote {{
  border-left: 4px solid var(--accent); background: #eff6ff;
  padding: .7rem 1rem; margin: 1rem 0; border-radius: 0 6px 6px 0;
}}
#main table {{
  border-collapse: collapse; margin: 1rem 0; width: 100%;
  font-size: .93rem;
}}
#main th, #main td {{
  border: 1px solid var(--border); padding: .4rem .7rem; text-align: left;
}}
#main th {{ background: #f1f5f9; font-weight: 600; }}
#main caption {{
  caption-side: top; text-align: left;
  font-size: .93rem; margin-bottom: .4rem; color: #374151;
}}
#main pre {{
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 1rem; overflow-x: auto;
  font-size: .88rem; line-height: 1.5; margin: 1rem 0;
}}
#main code {{
  font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace;
  font-size: .9em;
}}
#main .table-scroll {{ overflow-x: auto; margin: 1rem 0; }}
#main .table-scroll table {{ margin: 0; }}
#main :not(pre) > code {{
  background: var(--code-bg); padding: .15em .35em; border-radius: 4px;
}}
.MathJax {{ font-size: 1.05em !important; }}
/* A display formula wider than a phone screen scrolls in its own frame
   instead of widening the page (at 320 px: 928 px wide in section 3). */
#main mjx-container[display="true"] {{ overflow-x: auto; overflow-y: hidden; max-width: 100%; }}

/* ── Nav buttons ───────────────────────────────────────────── */
#nav-bar {{
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 3rem; padding-top: 1.2rem;
  border-top: 1px solid var(--border);
}}
#nav-bar button {{
  background: var(--accent); color: #fff; border: none;
  padding: .55rem 1.4rem; border-radius: 6px;
  font-size: .95rem; cursor: pointer; transition: opacity .15s;
}}
#nav-bar button:hover {{ opacity: .85; }}
#nav-bar button:disabled {{ opacity: .35; cursor: default; }}
#nav-bar .page-info {{ font-size: .85rem; color: #64748b; }}

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 860px) {{
  #sidebar {{ transform: translateX(-100%); }}
  #sidebar.open {{ transform: translateX(0); }}
  #menu-btn {{ display: block; }}
  #main {{ margin-left: 0; padding: 2rem 1.2rem 5rem; }}
}}
</style>
</head>
<body>

<button id="menu-btn" onclick="document.getElementById('sidebar').classList.toggle('open')">&#9776;</button>

<nav id="sidebar">
  <h2>Documentation</h2>
  <ul id="toc"></ul>
</nav>

<main id="main">
  <div id="content"></div>
  <div id="nav-bar">
    <button id="btn-prev" onclick="go(-1)">&larr; Previous</button>
    <span class="page-info" id="page-info"></span>
    <button id="btn-next" onclick="go(1)">Next &rarr;</button>
  </div>
</main>

{pages}

<script>
const pageEls = document.querySelectorAll('script[type="text/markdown"]');
const pages = Array.from(pageEls).map(el => ({{
  title: el.dataset.title,
  md: el.textContent
}}));

let cur = 0;
// marked reads "\\\\" as an escaped backslash and _..._ or *...* as emphasis:
// multi-line formulas (cases, aligned) reached MathJax on a single line.
// Formulas are set aside before marked.parse() and put back untouched;
// code blocks first, so that a "$" in code is not taken for math.
function parseWithMath(md) {{
  const code = [], math = [];
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  md = md.replace(/^```[\\s\\S]*?^```[ \\t]*$/gm, s => '\\uE000C' + (code.push(s) - 1) + '\\uE001');
  md = md.replace(/\\$\\$[\\s\\S]+?\\$\\$|(?<!\\\\)\\$(?:\\\\.|[^$\\\\])+?\\$/g,
                  s => '\\uE000M' + (math.push(s) - 1) + '\\uE001');
  md = md.replace(/\\uE000C(\\d+)\\uE001/g, (_, k) => code[k]);
  return marked.parse(md).replace(/\\uE000M(\\d+)\\uE001/g, (_, k) => esc(math[k]));
}}

function render(i) {{
  cur = i;
  const html = parseWithMath(pages[i].md);
  document.getElementById('content').innerHTML = '<h1>' + pages[i].title + '</h1>\\n' + html;

  if (window.MathJax && MathJax.typeset) {{
    MathJax.typesetClear();
    MathJax.typeset();
  }}

  document.querySelectorAll('#toc a').forEach((a, j) => {{
    a.classList.toggle('active', j === i);
  }});

  document.getElementById('btn-prev').disabled = (i === 0);
  document.getElementById('btn-next').disabled = (i === pages.length - 1);
  document.getElementById('page-info').textContent = (i+1) + ' / ' + pages.length;

  window.scrollTo(0, 0);
  location.hash = '#' + i;

  // close mobile sidebar
  document.getElementById('sidebar').classList.remove('open');
}}

function go(delta) {{
  const next = cur + delta;
  if (next >= 0 && next < pages.length) render(next);
}}

// build TOC
const toc = document.getElementById('toc');
pages.forEach((p, i) => {{
  const li = document.createElement('li');
  const a = document.createElement('a');
  a.textContent = p.title;
  a.onclick = () => render(i);
  li.appendChild(a);
  toc.appendChild(li);
}});

// keyboard nav
document.addEventListener('keydown', e => {{
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowLeft' && e.altKey) go(-1);
  if (e.key === 'ArrowRight' && e.altKey) go(1);
}});

// initial page from hash
const initPage = parseInt(location.hash.slice(1)) || 0;
render(Math.min(initPage, pages.length - 1));
</script>
</body>
</html>
'''


def build_page_script(index: int, title: str, md_content: str) -> str:
    """Wrap Markdown content in a <script type="text/markdown"> tag."""
    # Escape </script> inside content (shouldn't occur, but safety)
    safe = md_content.replace('</script>', '<\\/script>')
    return (f'<script type="text/markdown" data-title="{html_lib.escape(title, quote=True)}" '
            f'id="page-{index}">\n{safe}\n</script>')


def main():
    # Parse arguments
    tex_path = 'doc.tex'
    out_dir = 'docs'

    if len(sys.argv) >= 2:
        tex_path = sys.argv[1]
    if len(sys.argv) >= 3:
        out_dir = sys.argv[2]

    # Resolve paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(tex_path):
        tex_path = os.path.join(script_dir, tex_path)
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(script_dir, out_dir)

    print(f"Reading {tex_path}")
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex = f.read()

    # Extract and compile TikZ figures to SVG
    print("Compiling TikZ figures to SVG...")
    figures = extract_tikz_figures(tex)
    fig_svgs = compile_figures(figures, out_dir)
    print(f"  {sum(1 for s in fig_svgs if s):d}/{len(figures)} figures compiled")

    # Extract body.  The bibliography gets a page of its own (below): left in
    # the body, it was also appended as raw LaTeX to the last section.
    body = strip_preamble(tex)
    body = re.sub(r'\\begin\{thebibliography\}.*?\\end\{thebibliography\}', '', body, flags=re.DOTALL)
    CREF_MAP.update(build_label_map(body))

    # Split into sections
    sections = split_sections(body)

    # Check for bibliography (it's after the last section in the original body)
    bib_md = convert_bibliography(tex)

    # Convert each section (shared counter tracks figure order across sections)
    fig_counter = [0]
    TABLE_COUNTER[0] = 0
    pages = []
    for title, content in sections:
        md = convert_section(content, fig_svgs, fig_counter)
        pages.append((clean_title(title), md))

    # Add bibliography as final page if present
    if bib_md:
        pages.append(("References", bib_md))

    print(f"Found {len(pages)} pages:")
    for i, (title, _) in enumerate(pages):
        print(f"  {i:2d}. {title}")

    # Build page script tags
    page_scripts = []
    for i, (title, md) in enumerate(pages):
        page_scripts.append(build_page_script(i, title, md))

    pages_html = '\n'.join(page_scripts)
    html = HTML_TEMPLATE.format(pages=pages_html)

    # Write output
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Wrote {out_path} ({len(html):,} bytes)")

    # Markdown export, one file per page, when <out_dir>/md exists.  Figures
    # are quoted captions (no SVG).  It used to be regenerated by hand.
    md_dir = os.path.join(out_dir, 'md')
    if os.path.isdir(md_dir):
        md_counter = [0]          # figures numbered across pages, as in the HTML
        TABLE_COUNTER[0] = 0
        md_pages = [(clean_title(t), convert_section(c, [], md_counter)) for t, c in sections]
        if bib_md:
            md_pages.append(("References", bib_md))
        for i, (title, md) in enumerate(md_pages):
            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            with open(os.path.join(md_dir, f'{i:02d}-{slug}.md'), 'w', encoding='utf-8') as f:
                f.write(f'# {title}\n\n{md}\n')
        print(f"Wrote {len(md_pages)} Markdown pages to {md_dir}")


if __name__ == '__main__':
    main()
