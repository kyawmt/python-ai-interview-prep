import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(here, '..');
const notebookRoot = path.resolve(projectRoot, '../python_ai_interview');

const definitions = [
  ['01', '01_Python_Data_Structures.ipynb', 'Python Data Structures', 'Lists, dictionaries, sets, tuples, references, and copying.', '3–4 hrs'],
  ['02', '02_Functions_Classes_and_Python_Core.ipynb', 'Functions, Classes & Python Core', 'Functions, scope, composition, typing, errors, decorators, and generators.', '3–4 hrs'],
  ['03', '03_Comprehensions_and_Collections.ipynb', 'Comprehensions & Collections', 'Expressive comprehensions plus Counter, defaultdict, deque, and standard tools.', '2–3 hrs'],
  ['04', '04_NumPy_for_AI_Engineers.ipynb', 'NumPy for AI Engineers', 'Arrays, shapes, masking, broadcasting, reshaping, and linear algebra.', '4–5 hrs'],
  ['05', '05_Pandas_for_AI_Engineers.ipynb', 'pandas for AI Engineers', 'DataFrame fundamentals, missing data, GroupBy, merge, and ML features.', '4–5 hrs'],
  ['06', '06_Clean_Python_and_Interview_Patterns.ipynb', 'Clean Python & Interview Patterns', 'Readable design, edge cases, complexity, debugging, and fundamentals drills.', '4 hrs'],
  ['07', '07_LeetCode_Patterns_for_AI_Engineers.ipynb', 'LeetCode Patterns for AI Engineers', 'A problem-solving framework and 20 guided algorithm patterns.', '6–8 hrs'],
  ['08', '08_AI_Engineer_Python_Mock_Interview.ipynb', 'AI Engineer Python Mock Interview', 'A realistic five-round mock interview with solutions and scoring.', '2 hrs'],
  ['cheat-sheet', 'Python_Interview_Cheat_Sheet.ipynb', 'Python Interview Cheat Sheet', 'Fast references, core patterns, complexity traps, and 120 rapid-fire questions.', 'Reference'],
];

function sourceText(source) {
  const text = Array.isArray(source) ? source.join('') : source ?? '';
  let fenced = false;
  return text.split('\n').map((line) => {
    if (line.trimStart().startsWith('```')) {
      const next = line.replace(/^ {4}/, '');
      fenced = !fenced;
      return next;
    }
    return fenced ? line : line.replace(/^ {4}/, '');
  }).join('\n').trim();
}

function outputText(outputs = []) {
  return outputs.flatMap((output) => {
    if (output.output_type === 'stream') return [sourceText(output.text)];
    const plain = output.data?.['text/plain'];
    return plain ? [sourceText(plain)] : [];
  }).filter(Boolean).join('\n');
}

const lessons = definitions.map(([slug, file, title, summary, duration], index) => {
  const notebook = JSON.parse(fs.readFileSync(path.join(notebookRoot, file), 'utf8'));
  const cells = notebook.cells.map((cell, cellIndex) => ({
    id: `${slug}-${cellIndex + 1}`,
    type: cell.cell_type,
    source: sourceText(cell.source),
    output: outputText(cell.outputs),
  })).filter((cell) => cell.source || cell.output);
  const headings = cells
    .filter((cell) => cell.type === 'markdown')
    .flatMap((cell) => cell.source.split('\n'))
    .filter((line) => /^## (?!Table of contents)/.test(line))
    .map((line) => line.replace(/^## /, '').replace(/`/g, ''));
  return { slug, number: index < 8 ? String(index + 1).padStart(2, '0') : 'REF', file, title, summary, duration, headings, cells };
});

fs.mkdirSync(path.join(projectRoot, 'app/data'), { recursive: true });
fs.writeFileSync(path.join(projectRoot, 'app/data/lessons.json'), `${JSON.stringify(lessons, null, 2)}\n`);
console.log(`Imported ${lessons.length} notebooks and ${lessons.reduce((sum, lesson) => sum + lesson.cells.length, 0)} cells.`);
