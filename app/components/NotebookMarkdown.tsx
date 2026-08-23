import type { ReactNode } from 'react';

function slugify(value: string) {
  return value.toLowerCase().replace(/[`*_]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function inline(text: string): ReactNode[] {
  const tokens = text.split(/(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\)|\*[^*]+\*)/g).filter(Boolean);
  return tokens.map((token, index) => {
    if (token.startsWith('**') && token.endsWith('**')) return <strong key={index}>{inline(token.slice(2, -2))}</strong>;
    if (token.startsWith('`') && token.endsWith('`')) return <code key={index}>{token.slice(1, -1)}</code>;
    if (token.startsWith('*') && token.endsWith('*')) return <em key={index}>{token.slice(1, -1)}</em>;
    const link = token.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
    if (link) return <a key={index} href={link[2]}>{link[1]}</a>;
    return token;
  });
}

function isBlockStart(line: string, next = '') {
  return /^#{1,6} |^```|^> |^[-*] |^\d+\. |^---+$|^<details>/.test(line) || (line.startsWith('|') && /^\|?\s*:?-+/.test(next.replace(/^\|/, '')));
}

export function NotebookMarkdown({ source, hideSolutionTitle = false }: { source: string; hideSolutionTitle?: boolean }) {
  const lines = source.split('\n');
  const blocks: ReactNode[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i].trimEnd();
    if (!line.trim()) { i += 1; continue; }
    if (hideSolutionTitle && /^#### Solution/.test(line)) { i += 1; continue; }

    if (line.startsWith('```')) {
      const language = line.slice(3).trim() || 'text';
      const code: string[] = [];
      i += 1;
      while (i < lines.length && !lines[i].trimStart().startsWith('```')) { code.push(lines[i]); i += 1; }
      i += 1;
      blocks.push(<div className="inline-code-block" key={`code-${i}`}><span>{language}</span><pre><code>{code.join('\n')}</code></pre></div>);
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const label = heading[2].replace(/`/g, '');
      if (level === 1) { i += 1; continue; }
      const Tag = `h${Math.min(level, 4)}` as 'h2' | 'h3' | 'h4';
      blocks.push(<Tag id={slugify(label)} key={`heading-${i}`}>{inline(label)}</Tag>);
      i += 1;
      continue;
    }

    const details = line.match(/^<details><summary>(.*?)<\/summary>(.*?)<\/details>$/);
    if (details) {
      blocks.push(<details className="hint" key={`details-${i}`}><summary>{details[1]}</summary><p>{inline(details[2])}</p></details>);
      i += 1;
      continue;
    }

    if (line.startsWith('|') && i + 1 < lines.length && lines[i + 1].includes('---')) {
      const rows: string[][] = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        rows.push(lines[i].trim().replace(/^\||\|$/g, '').split('|').map((cell) => cell.trim()));
        i += 1;
      }
      const [header, , ...body] = rows;
      blocks.push(<div className="table-wrap" key={`table-${i}`}><table><thead><tr>{header.map((cell, n) => <th key={n}>{inline(cell)}</th>)}</tr></thead><tbody>{body.map((row, r) => <tr key={r}>{row.map((cell, c) => <td key={c}>{inline(cell)}</td>)}</tr>)}</tbody></table></div>);
      continue;
    }

    if (/^[-*] /.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*[-*] /.test(lines[i])) { items.push(lines[i].trim().replace(/^[-*] /, '')); i += 1; }
      blocks.push(<ul key={`ul-${i}`}>{items.map((item, n) => <li key={n}>{inline(item)}</li>)}</ul>);
      continue;
    }

    if (/^\d+\. /.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*\d+\. /.test(lines[i])) { items.push(lines[i].trim().replace(/^\d+\. /, '')); i += 1; }
      blocks.push(<ol key={`ol-${i}`}>{items.map((item, n) => <li key={n}>{inline(item)}</li>)}</ol>);
      continue;
    }

    if (line.startsWith('> ')) {
      const quote: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith('> ')) { quote.push(lines[i].trim().slice(2)); i += 1; }
      blocks.push(<blockquote key={`quote-${i}`}>{inline(quote.join(' '))}</blockquote>);
      continue;
    }

    if (/^---+$/.test(line.trim())) { blocks.push(<hr key={`hr-${i}`} />); i += 1; continue; }

    const paragraph = [line.trim()];
    i += 1;
    while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i].trim(), lines[i + 1]?.trim() ?? '')) {
      paragraph.push(lines[i].trim());
      i += 1;
    }
    blocks.push(<p key={`p-${i}`}>{inline(paragraph.join(' '))}</p>);
  }

  return <>{blocks}</>;
}
