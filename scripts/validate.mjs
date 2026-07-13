#!/usr/bin/env node
/**
 * validate_cn.mjs — Integrity and DAG validation check for Chinese dataset.
 *
 * Verifies:
 * 1. File existence and valid JSON structure.
 * 2. Topic IDs uniqueness.
 * 3. Referential integrity (all edges point to valid topic IDs).
 * 4. No self-loops.
 * 5. Cycle detection (verifies that the dependency graph is a DAG).
 *
 * Run using:
 *   node scripts/validate_cn.mjs
 */

import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const DATA_DIR = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'data');
const errors = [];

function check(condition, message) {
  if (!condition) {
    errors.push(message);
  }
}

// 1. Load Files
const topicsPath = resolve(DATA_DIR, 'topics_cn.json');
const depsPath = resolve(DATA_DIR, 'dependencies_cn.json');

if (!existsSync(topicsPath)) {
  console.error(`✗ Error: ${topicsPath} does not exist.`);
  process.exit(1);
}
if (!existsSync(depsPath)) {
  console.error(`✗ Error: ${depsPath} does not exist.`);
  process.exit(1);
}

const topicsData = JSON.parse(readFileSync(topicsPath, 'utf8'));
const depsData = JSON.parse(readFileSync(depsPath, 'utf8'));

const topics = topicsData.topics || [];
const dependencies = depsData.dependencies || [];

console.log(`Checking database: ${topics.length} topics and ${dependencies.length} dependencies...`);

// 2. Validate Topics
const topicIds = new Set();
for (const t of topics) {
  check(typeof t.id === 'string' && t.id.length > 0, `Topic has empty or missing ID.`);
  if (t.id) {
    if (topicIds.has(t.id)) {
      errors.push(`Duplicate topic ID: "${t.id}"`);
    }
    topicIds.add(t.id);
  }
  check(typeof t.name === 'string' && t.name.length > 0, `Topic [${t.id}] has empty name.`);
  check(typeof t.subject === 'string' && t.subject.length > 0, `Topic [${t.id}] has empty subject.`);
}

// 3. Validate Dependencies (Referential Integrity & Self-Loops)
const adj = new Map(); // Adjacency list for DFS cycle detection
for (const id of topicIds) {
  adj.set(id, []);
}

for (const d of dependencies) {
  check(topicIds.has(d.topicId), `Dependency points to unknown topicId: "${d.topicId}"`);
  check(topicIds.has(d.prerequisiteId), `Dependency points to unknown prerequisiteId: "${d.prerequisiteId}"`);
  if (d.topicId === d.prerequisiteId) {
    errors.push(`Self-dependency loop on topic: "${d.topicId}"`);
  }
  
  if (topicIds.has(d.topicId) && topicIds.has(d.prerequisiteId)) {
    // Add directed edge: prerequisiteId -> topicId (prerequisite unlocks topic)
    adj.get(d.prerequisiteId).push(d.topicId);
  }
}

// 4. Cycle Detection (DFS with 3-state coloring)
// 0 = unvisited, 1 = visiting, 2 = visited
const visited = new Map();
for (const id of topicIds) {
  visited.set(id, 0);
}

let hasCycle = false;
function dfs(u) {
  visited.set(u, 1); // visiting
  const neighbors = adj.get(u) || [];
  for (const v of neighbors) {
    if (visited.get(v) === 1) {
      errors.push(`Dependency cycle detected: "${u}" and "${v}" are part of a closed loop.`);
      hasCycle = true;
      return;
    } else if (visited.get(v) === 0) {
      dfs(v);
      if (hasCycle) return;
    }
  }
  visited.set(u, 2); // visited
}

for (const id of topicIds) {
  if (visited.get(id) === 0) {
    dfs(id);
    if (hasCycle) break;
  }
}

// 5. Final Report
if (errors.length > 0) {
  console.error(`\n✗ Validation failed with ${errors.length} error(s):`);
  for (const err of errors.slice(0, 20)) {
    console.error(`  - ${err}`);
  }
  if (errors.length > 20) {
    console.error(`  - ...and ${errors.length - 20} more errors.`);
  }
  process.exit(1);
} else {
  console.log(`\n✓ Validation passed! Dataset integrity is 100% sound.`);
  console.log(`  - Total topics: ${topics.length}`);
  console.log(`  - Total dependency edges: ${dependencies.length}`);
  console.log(`  - Graph is a valid DAG (no cycles detected).`);
}
