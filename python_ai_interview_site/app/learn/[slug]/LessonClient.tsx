'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { NotebookMarkdown } from '../../components/NotebookMarkdown';
import type { Lesson, NotebookCell } from '../../data/types';

function CodeCell({ cell }: { cell: NotebookCell }) {
  const [copied, setCopied] = useState(false);
  const isTodo = /TODO|pass\s*$/.test(cell.source);
  async function copyCode() {
    await navigator.clipboard.writeText(cell.source);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }
  return (
    <div className={`lesson-code ${isTodo ? 'todo-code' : ''}`}>
      <div className="lesson-code-bar"><span>{isTodo ? 'Your turn' : 'Python'}</span><button type="button" onClick={copyCode}>{copied ? 'Copied ✓' : 'Copy'}</button></div>
      <pre><code>{cell.source}</code></pre>
      {cell.output && <div className="cell-output"><span>Output</span><pre>{cell.output}</pre></div>}
    </div>
  );
}

export default function LessonClient({ lesson, lessons }: { lesson: Lesson; lessons: Lesson[] }) {
  const [completed, setCompleted] = useState<string[]>([]);
  const [search, setSearch] = useState('');
  const [scrollProgress, setScrollProgress] = useState(0);
  const [menuOpen, setMenuOpen] = useState(false);
  const searchRef = useRef<HTMLInputElement>(null);
  const lessonIndex = lessons.findIndex((item) => item.slug === lesson.slug);

  useEffect(() => {
    const stored = window.localStorage.getItem('pyready-completed');
    if (stored) setCompleted(JSON.parse(stored));
    const onScroll = () => {
      const height = document.documentElement.scrollHeight - window.innerHeight;
      setScrollProgress(height > 0 ? Math.min(100, (window.scrollY / height) * 100) : 0);
    };
    const onKey = (event: KeyboardEvent) => {
      if (event.key === '/' && document.activeElement?.tagName !== 'INPUT') { event.preventDefault(); searchRef.current?.focus(); }
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('keydown', onKey);
    return () => { window.removeEventListener('scroll', onScroll); window.removeEventListener('keydown', onKey); };
  }, []);

  const results = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return [];
    return lessons.filter((item) => `${item.title} ${item.summary} ${item.headings.join(' ')}`.toLowerCase().includes(query)).slice(0, 6);
  }, [search, lessons]);

  function toggleComplete() {
    const next = completed.includes(lesson.slug) ? completed.filter((slug) => slug !== lesson.slug) : [...completed, lesson.slug];
    setCompleted(next);
    window.localStorage.setItem('pyready-completed', JSON.stringify(next));
  }

  return (
    <main className="lesson-shell">
      <div className="reading-progress" style={{ width: `${scrollProgress}%` }} />
      <header className="lesson-header">
        <button className="menu-button" type="button" aria-label="Toggle course menu" onClick={() => setMenuOpen(!menuOpen)}>☰</button>
        <a className="brand" href="/"><span className="brand-mark">py</span><span>PyReady</span></a>
        <div className="course-search">
          <span aria-hidden="true">⌕</span><input ref={searchRef} value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search the course" aria-label="Search the course" /><kbd>/</kbd>
          {search && <div className="search-results">{results.length ? results.map((item) => <a key={item.slug} href={`/learn/${item.slug}`}><small>{item.number}</small><span><strong>{item.title}</strong><em>{item.summary}</em></span></a>) : <p>No matching lessons yet.</p>}</div>}
        </div>
        <div className="header-progress"><span>{completed.length} / 8 core modules</span><div><i style={{ width: `${Math.min(100, completed.filter((slug) => slug !== 'cheat-sheet').length / 8 * 100)}%` }} /></div></div>
      </header>

      <aside className={`course-sidebar ${menuOpen ? 'open' : ''}`}>
        <div className="sidebar-label">Learning path</div>
        <nav aria-label="Course modules">
          {lessons.slice(0, 8).map((item) => <a className={item.slug === lesson.slug ? 'active' : ''} href={`/learn/${item.slug}`} key={item.slug} onClick={() => setMenuOpen(false)}><span className={completed.includes(item.slug) ? 'done' : ''}>{completed.includes(item.slug) ? '✓' : item.number}</span><div><strong>{item.title}</strong><small>{item.duration}</small></div></a>)}
        </nav>
        <div className="sidebar-reference"><span>Quick reference</span><a className={lesson.slug === 'cheat-sheet' ? 'active' : ''} href="/learn/cheat-sheet"><b>⌘</b><div><strong>Interview Cheat Sheet</strong><small>120 rapid-fire questions</small></div></a></div>
        <a className="back-home" href="/">← Course overview</a>
      </aside>
      {menuOpen && <button className="sidebar-scrim" aria-label="Close course menu" onClick={() => setMenuOpen(false)} />}

      <article className="lesson-article">
        <div className="lesson-breadcrumb"><a href="/">Course</a><span>›</span><span>Module {lesson.number}</span></div>
        <header className="lesson-title">
          <div className="lesson-number">{lesson.number}</div>
          <div><p>{lesson.slug === 'cheat-sheet' ? 'Quick reference' : 'Python interview path'} · {lesson.duration}</p><h1>{lesson.title}</h1><span>{lesson.summary}</span></div>
        </header>
        <div className="lesson-meta"><span>{lesson.cells.filter((cell) => cell.type === 'code').length} code examples</span><span>{lesson.headings.length} sections</span><span>From {lesson.file.replace('.ipynb', '')}</span></div>

        <div className="notebook-content">
          {lesson.cells.map((cell, index) => {
            const previousIsSolution = index > 0 && /^#### Solution/.test(lesson.cells[index - 1].source);
            if (cell.type === 'markdown') return <section className="markdown-cell" key={cell.id}><NotebookMarkdown source={cell.source} hideSolutionTitle /></section>;
            if (cell.type === 'code' && previousIsSolution) return <details className="solution-block" key={cell.id}><summary>Reveal solution <span>Open only after attempting</span></summary><CodeCell cell={cell} /></details>;
            if (cell.type === 'code') return <CodeCell key={cell.id} cell={cell} />;
            return null;
          })}
        </div>

        <section className={`completion-card ${completed.includes(lesson.slug) ? 'complete' : ''}`}><div><span>{completed.includes(lesson.slug) ? '✓' : '→'}</span><div><p>{completed.includes(lesson.slug) ? 'Module complete' : 'Finished this module?'}</p><small>Your progress is saved on this device.</small></div></div><button type="button" onClick={toggleComplete}>{completed.includes(lesson.slug) ? 'Mark incomplete' : 'Mark as complete'}</button></section>
        <nav className="lesson-pager" aria-label="Lesson navigation">{lessonIndex > 0 ? <a href={`/learn/${lessons[lessonIndex - 1].slug}`}><small>← Previous</small><strong>{lessons[lessonIndex - 1].title}</strong></a> : <span />}{lessonIndex < lessons.length - 1 && <a className="next" href={`/learn/${lessons[lessonIndex + 1].slug}`}><small>Next →</small><strong>{lessons[lessonIndex + 1].title}</strong></a>}</nav>
      </article>

      <aside className="lesson-toc"><p>On this page</p>{lesson.headings.slice(0, 10).map((heading) => <a href={`#${heading.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')}`} key={heading}>{heading}</a>)}</aside>
    </main>
  );
}
