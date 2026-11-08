/* Problem topics in a sensible learning order, with a picture and a one-line "in plain words". */
export const TOPICS = [
  ['Arrays & Hashing', 'hashmap', '🗂', 'Lists of things, plus the magic "remember it instantly" dictionary.'],
  ['Two Pointers', 'twopointers', '👉', 'Two fingers walking along a list, often toward each other.'],
  ['Sliding Window', 'window', '🪟', 'A frame that slides and stretches over a list or string.'],
  ['Stack', 'stack', '🥞', 'A pile of pancakes: last one on is the first one off.'],
  ['Binary Search', 'binarysearch', '🔍', 'Halve the search every guess, like finding a page in a book.'],
  ['Linked List', 'linkedlist', '🚂', 'A train: each car only knows the next car.'],
  ['Trees', 'tree', '🌳', 'A family tree: every node has kids below it.'],
  ['Heap', 'heap', '👑', 'A pile that always hands you the smallest (or biggest) first.'],
  ['Tries', 'trie', '🔤', 'A tree of letters for super-fast word lookups.'],
  ['Backtracking', 'backtracking', '🧭', 'Try a choice, explore, undo, try the next one.'],
  ['Graphs', 'graph', '🕸', 'Dots and lines: maps, friends, networks.'],
  ['1-D Dynamic Programming', 'dp', '🪜', 'Solve small versions first and save the answers.'],
  ['2-D Dynamic Programming', 'dp', '🧮', 'Save answers in a grid instead of a row.'],
  ['Greedy', 'challenges', '🍪', 'Grab the best-looking choice right now, and it works out.'],
  ['Intervals', 'queue', '📅', 'Time blocks that might overlap, like meetings.'],
  ['Math & Bits', 'array', '🔢', 'Number tricks and playing with 0s and 1s.'],
  ['Sorting', 'sorting', '🐧', 'Put things in order, many clever ways.'],
];
export const topicInfo = name => TOPICS.find(t => t[0] === name) || [name, 'array', '📦', ''];
export const XP = { Easy: 10, Medium: 20, Hard: 40 };
