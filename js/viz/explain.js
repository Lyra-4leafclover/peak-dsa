/* Turns a recorded step into a plain-English sentence a total beginner can follow. */
import { describe } from './diff.js';
import { fmt, esc } from './values.js';
import { indentOf } from '../ui/code.js';

const c = s => `<code>${esc(s)}</code>`;

export function stateAt(steps, k) {
  const s = steps[k];
  if (!s) return null;
  if (s.e === 'return' || s.e === 'exception' || k === steps.length - 1) return s;
  return steps[k + 1];
}

function enteredBody(steps, k, lines) {
  const s = steps[k], n = steps[k + 1];
  if (!n || n.e !== 'line' || n.c !== s.c) return null;
  const myIndent = indentOf(lines[s.l - 1] || '');
  return n.l > s.l && indentOf(lines[n.l - 1] || '') > myIndent;
}

export function explain(trace, k, lines, notes) {
  const steps = trace.steps;
  const s = steps[k];
  if (!s) return { head: 'Press ▶ to start!', changes: [] };
  const raw = (lines[s.l - 1] || '').trim();
  const top = s.st[s.st.length - 1];
  let head = '▶ Run this line.';
  const call = (trace.calls || [])[s.c - 1];

  if (s.e === 'call') {
    head = top && top.f === '<module>' ? 'The program starts at the top.' : `Jumping into ${c(`${top.f}(${call ? call.a : ''})`)}. A fresh notebook of variables opens for this call.`;
  } else if (s.e === 'return') {
    head = top && top.f === '<module>' ? 'The program is finished!' : `↩ ${c(top.f)} is done and hands back ${c(s.rs ?? fmt(s.ret, s.h))} to whoever called it.`;
  } else if (s.e === 'exception') {
    head = `Something went wrong here: ${c(s.exc || 'error')}`;
  } else if (s.x) {
    const { cond, sub, val, kind } = s.x;
    const show = sub && sub !== cond ? `${c(cond)} → ${c(sub)}` : c(cond);
    if (kind === 'while') head = `Should we keep looping? Is ${show}? ${val ? '<b>Yes</b> → go around again.' : '<b>No</b> → the loop stops here.'}`;
    else head = `Check: is ${show}? ${val ? '<b>Yes</b> → run the indented lines below.' : '<b>No</b> → skip them.'}`;
  } else {
    head = lineSentence(raw, steps, k, lines);
  }
  let changes = [];
  const after = stateAt(steps, k);
  if (after !== s) changes = describe(s, after);
  return { head, changes, note: notes && notes[s.l], line: s.l };
}

function lineSentence(t, steps, k, lines) {
  let m;
  const ent = () => enteredBody(steps, k, lines);
  if ((m = t.match(/^def (\w+)\s*\((.*)\)/))) return `Writing down a recipe called ${c(m[1])}. It doesn't run yet, only when someone calls it.`;
  if ((m = t.match(/^class (\w+)/))) return `Making a blueprint called ${c(m[1])}.`;
  if ((m = t.match(/^for (.+?) in (.+):\s*$/))) {
    const e = ent();
    if (e === false) return `${c(m[2])} has no items left, so the ${c('for')} loop is finished.`;
    if (/^range\(/.test(m[2])) return `Loop: give ${c(m[1])} the next number from ${c(m[2])}.`;
    if (/^enumerate\(/.test(m[2])) return `Loop: grab the next item <i>and</i> its position from ${c(m[2].slice(10, -1))} → ${c(m[1])}.`;
    return `Loop: take the next item out of ${c(m[2])} and call it ${c(m[1])}.`;
  }
  if ((m = t.match(/^while (.+):/))) {
    const e = ent();
    return e === false ? `Check ${c(m[1])} → it's false, so the loop stops.` : `Check ${c(m[1])} → still true, so we go around the loop again.`;
  }
  if ((m = t.match(/^(el)?if (.+):/))) {
    const e = ent();
    return e === null ? `Check ${c(m[2])}.` : `Check ${c(m[2])} → ${e ? 'true, so we go inside.' : 'false, so we skip it.'}`;
  }
  if (/^else\s*:/.test(t)) return '↪ None of the checks above were true, so we take the <b>else</b> path.';
  if ((m = t.match(/^return\s*(.*)$/))) return m[1] ? `Hand back the answer: ${c(m[1])}.` : 'Stop here and go back to the caller.';
  if (/^break\b/.test(t)) return '<b>break</b>: jump out of the loop right now.';
  if (/^continue\b/.test(t)) return '<b>continue</b>: skip the rest of this round and start the next one.';
  if (/^pass\b/.test(t)) return '<b>pass</b>: do nothing.';
  if (/^print\(/.test(t)) return 'Print something on the screen (see “Printed output”).';
  if (/^(import|from) /.test(t)) return 'Bring in a ready-made toolbox.';
  if (/^(nonlocal|global) /.test(t)) return `Let this function change the outer variable ${c(t.split(/\s+/).slice(1).join(' '))}.`;
  if ((m = t.match(/heappush\((\w[\w.]*)\s*,\s*(.+)\)/))) return `Push ${c(m[2])} into the heap ${c(m[1])}. The heap reshuffles so the <b>smallest</b> sits on top.`;
  if ((m = t.match(/heappop\((\w[\w.]*)\)/))) return `Pop the <b>smallest</b> item off the top of heap ${c(m[1])}.`;
  if ((m = t.match(/heapify\((\w[\w.]*)\)/))) return `Turn ${c(m[1])} into a heap (smallest item first).`;
  if ((m = t.match(/^([\w.\[\]]+)\.append\((.+)\)$/))) return `Put ${c(m[2])} at the end of ${c(m[1])}.`;
  if ((m = t.match(/^([\w.\[\]]+)\.appendleft\((.+)\)$/))) return `Put ${c(m[2])} at the front of ${c(m[1])}.`;
  if ((m = t.match(/([\w.\[\]]+)\.popleft\(\)/))) return `Take the first item out of the queue ${c(m[1])} (first in, first out).`;
  if ((m = t.match(/([\w.\[\]]+)\.pop\(0\)/))) return `Take the first item out of ${c(m[1])}.`;
  if ((m = t.match(/([\w.\[\]]+)\.pop\(\)/))) return `Take the last item off the top of ${c(m[1])}.`;
  if ((m = t.match(/^([\w.\[\]]+)\.add\((.+)\)$/))) return `Drop ${c(m[2])} into the set ${c(m[1])} (sets ignore duplicates).`;
  if ((m = t.match(/^([\w.\[\]]+)\.remove\((.+)\)$/))) return `Remove ${c(m[2])} from ${c(m[1])}.`;
  if ((m = t.match(/^del (.+)$/))) return `Delete ${c(m[1])}.`;
  if ((m = t.match(/^([\w.]+)\.sort\(/))) return `Sort ${c(m[1])} from small to big.`;
  if ((m = t.match(/^([\w.\[\]]+)\s*([+\-*/%]|\/\/|\*\*|\||&|\^)=\s*(.+)$/))) {
    const op = { '+': 'Add', '-': 'Subtract', '*': 'Multiply by', '/': 'Divide by', '//': 'Divide by', '%': 'Keep the remainder after dividing by' }[m[2]] || 'Update with';
    return `${op} ${c(m[3])} ${m[2] === '+' ? 'to' : m[2] === '-' ? 'from' : '→'} ${c(m[1])}.`;
  }
  if ((m = t.match(/^([\w.]+)\[(.+)\]\s*=\s*(.+)$/))) return `Write ${c(m[3])} into slot ${c(m[2])} of ${c(m[1])}.`;
  if ((m = t.match(/^([\w.]+(?:\s*,\s*[\w.]+)+)\s*=\s*(.+)$/))) {
    const lhs = m[1].split(',').map(x => x.trim());
    return /^\w[\w.]*(\s*,\s*\w[\w.]*)+$/.test(m[2]) && m[2].split(',').length === lhs.length
      ? `Update ${lhs.map(c).join(', ')} all at the same time (Python works out the right side first).`
      : `Work out ${c(m[2])} and unpack it into ${lhs.map(c).join(', ')}.`;
  }
  if ((m = t.match(/^([\w.]+)\s*(?::\s*[^=]+)?=\s*(.+)$/))) {
    const rhs = m[2];
    if (/^\[\]$|^list\(\)$/.test(rhs)) return `Make an empty list called ${c(m[1])}.`;
    if (/^\{\}$|^dict\(\)$/.test(rhs)) return `Make an empty dictionary (a lookup table) called ${c(m[1])}.`;
    if (/^set\(\)$/.test(rhs)) return `Make an empty set called ${c(m[1])}.`;
    if (/^deque\(/.test(rhs)) return `Make a queue (line of people) called ${c(m[1])}.`;
    if (/^defaultdict\(/.test(rhs)) return `Make a dictionary ${c(m[1])} that fills in missing keys automatically.`;
    if (/^Counter\(/.test(rhs)) return `Count how many times each thing appears and store it in ${c(m[1])}.`;
    if (/^\[.*for .* in /.test(rhs)) return `Build a list using a mini-loop and save it in ${c(m[1])}.`;
    if (/^ListNode\(|^TreeNode\(|^Node\(/.test(rhs)) return `Make a brand-new node and call it ${c(m[1])}.`;
    if (/\(/.test(rhs)) return `Work out ${c(rhs)} and save the result in ${c(m[1])}.`;
    return `Save ${c(rhs)} into ${c(m[1])}.`;
  }
  return `▶ Run ${c(t)}.`;
}
