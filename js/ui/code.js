/* Python code helpers: pull out "#>" teaching notes and colour the syntax. */
import { esc } from '../viz/values.js';

export function splitNotes(src) {
  const notes = {};
  const lines = src.replace(/\t/g, '    ').split('\n').map((line, i) => {
    const m = line.match(/^(.*?)\s*#>\s?(.*)$/);
    if (m && !inString(m[1])) { notes[i + 1] = m[2]; return m[1].replace(/\s+$/, ''); }
    return line;
  });
  while (lines.length && !lines[lines.length - 1].trim()) lines.pop();
  return { code: lines.join('\n'), notes };
}
function inString(s) { return ((s.match(/'/g) || []).length % 2) || ((s.match(/"/g) || []).length % 2); }

const KW = new Set('def class return if elif else for while in not and or is None True False break continue pass import from as with try except finally raise lambda yield global nonlocal del assert'.split(' '));
const BI = new Set('len range print min max sum abs sorted reversed enumerate zip list dict set tuple int str float bool map filter any all ord chr isinstance heappush heappop heapify deque defaultdict Counter self inf'.split(' '));

export function highlight(line) {
  const re = /(#.*$)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+)|(.)/g;
  let out = '', m, prevDef = false;
  while ((m = re.exec(line))) {
    const [t, com, str, num, id] = m;
    if (com) out += `<span class="tk-c">${esc(com)}</span>`;
    else if (str) out += `<span class="tk-s">${esc(str)}</span>`;
    else if (num) out += `<span class="tk-n">${num}</span>`;
    else if (id) {
      if (prevDef) out += `<span class="tk-f">${id}</span>`;
      else if (KW.has(id)) out += `<span class="tk-k">${id}</span>`;
      else if (BI.has(id)) out += `<span class="tk-b">${id}</span>`;
      else out += esc(id);
      prevDef = id === 'def' || id === 'class';
      continue;
    } else out += esc(t);
    if (!/^\s+$/.test(t)) prevDef = false;
  }
  return out || ' ';
}

export const indentOf = s => s.match(/^\s*/)[0].length;
