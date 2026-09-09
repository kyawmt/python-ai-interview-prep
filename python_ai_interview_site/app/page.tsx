const modules = [
  ['01', 'Python Data Structures', 'Lists, dicts, sets, tuples', '3–4 hrs', 'green'],
  ['02', 'Functions & Classes', 'Core Python, typing, generators', '3–4 hrs', 'blue'],
  ['03', 'Collections', 'Comprehensions and standard tools', '2–3 hrs', 'purple'],
  ['04', 'NumPy for AI', 'Arrays, shapes, broadcasting', '4–5 hrs', 'orange'],
  ['05', 'pandas for AI', 'DataFrames and ML workflows', '4–5 hrs', 'pink'],
  ['06', 'Clean Python', 'Readable code and edge cases', '4 hrs', 'yellow'],
  ['07', 'LeetCode Patterns', '20 essential coding problems', '6–8 hrs', 'cyan'],
  ['08', 'Mock Interview', 'A full five-round simulation', '2 hrs', 'red'],
] as const;

export default function Home() {
  return (
    <main>
      <nav className="nav-shell" aria-label="Primary navigation">
        <a className="brand" href="#top" aria-label="PyReady home"><span className="brand-mark">py</span><span>PyReady</span></a>
        <div className="nav-links"><a href="#curriculum">Curriculum</a><a href="#practice">Practice</a><a className="nav-cta" href="#curriculum">Start learning</a></div>
      </nav>

      <section className="hero" id="top">
        <div className="hero-copy">
          <div className="eyebrow"><span /> Python for AI engineers</div>
          <h1>Learn the Python<br />that <em>interviews</em> test.</h1>
          <p className="hero-lede">A focused, notebook-backed course for building real Python fluency—from data structures to NumPy, pandas, and coding interviews.</p>
          <div className="hero-actions">
            <a className="primary-button" href="#curriculum">Explore the course <span>→</span></a>
            <span className="time-note"><strong>9 notebooks</strong><br />25+ hours of practice</span>
          </div>
          <div className="trust-row"><span>✓ Built from your notebooks</span><span>✓ 100+ exercises</span><span>✓ Progress saved locally</span></div>
        </div>

        <div className="hero-code" aria-label="Python code example">
          <div className="code-window">
            <div className="window-bar"><div><span className="dot red" /><span className="dot amber" /><span className="dot green" /></div><span>interview.py</span><span className="file-type">PY</span></div>
            <pre><code><span className="line-no">1</span><span className="kw">def</span> <span className="fn">top_k_frequent</span>(items, k):{`\n`}<span className="line-no">2</span>    <span className="comment"># Count in one clean pass</span>{`\n`}<span className="line-no">3</span>    counts = Counter(items){`\n`}<span className="line-no">4</span>{`\n`}<span className="line-no">5</span>    <span className="kw">return</span> counts.<span className="fn">most_common</span>(k){`\n`}<span className="line-no">6</span>{`\n`}<span className="line-no">7</span>labels = [<span className="str">&quot;cat&quot;</span>, <span className="str">&quot;dog&quot;</span>, <span className="str">&quot;cat&quot;</span>]{`\n`}<span className="line-no">8</span><span className="fn">print</span>(<span className="fn">top_k_frequent</span>(labels, <span className="num">1</span>))</code></pre>
            <div className="output"><span>›</span> [(&apos;cat&apos;, 2)] <b>✓</b></div>
          </div>
          <div className="floating-badge badge-one"><b>O(n)</b><span>Time complexity</span></div><div className="floating-badge badge-two"><b>100+</b><span>Practice prompts</span></div>
        </div>
      </section>

      <section className="curriculum-section" id="curriculum">
        <div className="section-heading"><div><p className="kicker">A complete learning path</p><h2>Eight modules. One confident Python engineer.</h2></div><p>Move in order or jump straight to the skill you need. Every module mirrors a companion Jupyter notebook.</p></div>
        <div className="module-grid">
          {modules.map(([number, title, description, time, tone]) => (
            <article className={`module-card ${tone}`} key={number}>
              <div className="module-top"><span>{number}</span><span>{time}</span></div>
              <div className="module-icon" aria-hidden="true">{number === '04' ? '∑' : number === '05' ? '▦' : number === '07' ? '⌁' : number === '08' ? '◎' : '{}'}</div>
              <h3>{title}</h3><p>{description}</p><a href={`/learn/${number}`}>Open module <span>→</span></a>
            </article>
          ))}
        </div>
      </section>

      <section className="practice-strip" id="practice"><div><span className="mini-label">Interview mode</span><h2>Knowledge sticks when you use it.</h2></div><p>Work through TODOs, reveal hints only when needed, then test yourself in a timed five-round mock interview.</p><a href="/learn/08">Try the mock interview <span>→</span></a></section>
      <footer><a className="brand" href="#top"><span className="brand-mark">py</span><span>PyReady</span></a><p>Your notebook companion for Python + AI interviews.</p><span>Learn. Practice. Get ready.</span></footer>
    </main>
  );
}
