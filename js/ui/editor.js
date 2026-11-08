/* Code editor: CodeMirror 5 when available, plain textarea otherwise. */
export function createEditor(el, value, { onChange, minLines = 12 } = {}) {
  el.classList.add('editor');
  if (window.CodeMirror) {
    const cm = window.CodeMirror(el, {
      value, mode: 'python', lineNumbers: true, indentUnit: 4, tabSize: 4, indentWithTabs: false,
      matchBrackets: true, viewportMargin: Infinity, lineWrapping: false,
      extraKeys: { Tab: c => c.somethingSelected() ? c.indentSelection('add') : c.replaceSelection('    '), 'Shift-Tab': c => c.indentSelection('subtract') },
    });
    if (onChange) cm.on('change', () => onChange(cm.getValue()));
    cm.getWrapperElement().style.minHeight = `${minLines * 22}px`;
    setTimeout(() => cm.refresh(), 30);
    return {
      get: () => cm.getValue(), set: v => cm.setValue(v), refresh: () => cm.refresh(),
      mark(line) { cm.getAllMarks?.(); cm.eachLine(l => cm.removeLineClass(l, 'background', 'cm-err')); if (line) cm.addLineClass(line - 1, 'background', 'cm-err'); },
    };
  }
  const ta = document.createElement('textarea');
  ta.className = 'plain-editor'; ta.value = value; ta.spellcheck = false; ta.rows = minLines;
  ta.addEventListener('keydown', e => {
    if (e.key === 'Tab') { e.preventDefault(); const s = ta.selectionStart; ta.setRangeText('    ', s, ta.selectionEnd, 'end'); }
  });
  if (onChange) ta.addEventListener('input', () => onChange(ta.value));
  el.appendChild(ta);
  return { get: () => ta.value, set: v => { ta.value = v; }, refresh() {}, mark() {} };
}

export async function waitForCM(ms = 4000) {
  const t0 = Date.now();
  while (!window.CodeMirror && Date.now() - t0 < ms) await new Promise(r => setTimeout(r, 60));
}
