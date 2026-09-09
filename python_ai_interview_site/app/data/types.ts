export type NotebookCell = { id: string; type: 'markdown' | 'code' | 'raw'; source: string; output: string };
export type Lesson = { slug: string; number: string; file: string; title: string; summary: string; duration: string; headings: string[]; cells: NotebookCell[] };
