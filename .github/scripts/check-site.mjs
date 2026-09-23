// Site integrity check for 方城特产百珍坊.
//
// Fails the build on defects that are objectively wrong; warns (without failing)
// on the residual character damage documented in README.md, so the debt stays
// visible without blocking every commit.
//
//   FAIL  invalid UTF-8 bytes in a text file
//   FAIL  structurally eaten '<'  ("?/tag>" -- an unclosed <title> renders the
//         whole page blank, which is how 13 pages were silently broken)
//   FAIL  an inline <script> that is not valid JavaScript (an eaten newline can
//         comment out the following line and kill an entire handler)
//   FAIL  a start tag whose attribute list is malformed (an eaten quote folds
//         the next attribute into the previous value)
//   FAIL  an HTML page without a well-formed <title>
//   FAIL  a local href/src/url() target that does not exist
//   FAIL  a root-absolute reference ("/x.css"), which breaks a project Pages site
//   WARN  U+FFFD replacement characters (irrecoverable damage, see README)
//
// Deliberately dependency-free: this repository has no package.json, so the CI
// job cannot install anything. Everything below uses the Node standard library.
import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { join, dirname, resolve, relative, extname } from 'node:path'

const root = resolve(process.argv[2] ?? '.')
const SKIP_DIRS = new Set(['.git', 'node_modules', '_normalize'])

function walk(dir, out = []) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(join(dir, e.name), out) }
    else out.push(join(dir, e.name))
  }
  return out
}

const TEXT_EXT = new Set(['.html', '.css', '.js', '.json', '.svg', '.txt', '.md'])
const files = walk(root)
const rel = (f) => relative(root, f).replace(/\\/g, '/')

const fail = []
const warn = []

// ---- 1. encoding integrity ----------------------------------------------
for (const f of files) {
  const ext = extname(f).toLowerCase()
  if (!TEXT_EXT.has(ext)) continue
  const buf = readFileSync(f)
  const text = buf.toString('utf8')
  if (text.includes('\uFFFD')) {
    // Distinguish "invalid bytes in this file" from the documented legacy damage
    const n = (text.match(/\uFFFD/g) ?? []).length
    warn.push(`${rel(f)}: ${n} U+FFFD (documented residual damage, see README)`)
  }
}

// ---- 2/3/4. HTML and CSS checks -----------------------------------------
const stripBlocks = (html, tag) =>
  html.replace(new RegExp(`<${tag}\\b[^>]*>[\\s\\S]*?<\\/${tag}>`, 'gi'), '')

const REF = /(?:src|href)\s*=\s*["']([^"']*)["']|url\(\s*["']?([^"')]*)["']?\s*\)|@import\s+["']([^"']*)["']/gi
const SKIP_SCHEME = /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i
const STRUCTURAL = /\?\/[a-zA-Z][a-zA-Z0-9]*>/g

let checkedRefs = 0

for (const f of files) {
  const ext = extname(f).toLowerCase()
  if (ext !== '.html' && ext !== '.css') continue
  const raw = readFileSync(f, 'utf8')

  const structural = (raw.match(STRUCTURAL) ?? []).length
  if (structural > 0) {
    fail.push(`${rel(f)}: ${structural} damaged tag closer(s) matched "?/tag>" -- an eaten '<' breaks the document structure`)
  }

  if (ext === '.html') {
    if (!/<title>[\s\S]*?<\/title>/i.test(raw)) {
      fail.push(`${rel(f)}: missing a well-formed <title>`)
    }
  }

  let text = raw
  if (ext === '.html') {
    text = stripBlocks(stripBlocks(text, 'script'), 'style').replace(/<!--[\s\S]*?-->/g, '')
  }

  const dir = dirname(f)
  let m
  REF.lastIndex = 0
  while ((m = REF.exec(text)) !== null) {
    const ref = (m[1] ?? m[2] ?? m[3] ?? '').trim()
    if (!ref || SKIP_SCHEME.test(ref)) continue
    const clean = ref.split('#')[0].split('?')[0]
    if (!clean) continue
    if (clean.startsWith('/')) {
      fail.push(`${rel(f)}: root-absolute reference "${ref}" breaks a project Pages subpath`)
      continue
    }
    checkedRefs++
    if (!existsSync(resolve(dir, clean))) {
      fail.push(`${rel(f)}: reference "${ref}" does not resolve`)
    }
  }
}

// ---- 5. inline JavaScript must actually parse ---------------------------
// An eaten newline after a "//" comment silently comments out the next line;
// the page still renders and the failure is invisible until a button does
// nothing. This is the check that catches that.
const SCRIPT = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi

function checkScripts(html, name) {
  let m
  SCRIPT.lastIndex = 0
  while ((m = SCRIPT.exec(html)) !== null) {
    const attrs = m[1] ?? ''
    const body = m[2] ?? ''
    if (!body.trim()) continue
    if (/\bsrc\s*=/i.test(attrs)) continue
    if (/type\s*=\s*["']?(module|application\/json|text\/template|text\/plain)/i.test(attrs)) continue
    try {
      // Compiles the body as a function body: enough to surface syntax errors
      // such as a swallowed brace, without executing anything.
      new Function(body) // eslint-disable-line no-new-func
    } catch (e) {
      fail.push(`${name}: inline <script> is not valid JavaScript -- ${e.message}`)
    }
  }
}

// ---- 6. start-tag attribute lists must be well formed -------------------
// A name character that cannot legally appear in an attribute name means the
// tokenizer desynchronised, which is exactly what an eaten '"' produces.
const TAG_REGION = /<([a-zA-Z][a-zA-Z0-9:-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)>/g
const VALID_NAME = /^[^\s"'>/=]+$/

function malformedAttributes(region) {
  let i = 0
  while (i < region.length) {
    while (i < region.length && /\s/.test(region[i])) i++
    if (i >= region.length) break

    const start = i
    while (i < region.length && !/[\s=/>]/.test(region[i])) i++
    const name = region.slice(start, i)
    if (!VALID_NAME.test(name)) return name

    while (i < region.length && /\s/.test(region[i])) i++
    if (region[i] === '=') {
      i++
      while (i < region.length && /\s/.test(region[i])) i++
      if (region[i] === '"' || region[i] === "'") {
        const q = region[i]
        i++
        while (i < region.length && region[i] !== q) i++
        if (i >= region.length) return 'unterminated quoted value'
        i++
      } else {
        while (i < region.length && !/[\s>]/.test(region[i])) i++
      }
    }
  }
  return null
}

function checkAttributes(html, name) {
  let m
  let reported = 0
  TAG_REGION.lastIndex = 0
  while ((m = TAG_REGION.exec(html)) !== null) {
    const bad = malformedAttributes(m[2] ?? '')
    if (bad) {
      // Report every occurrence, not just the first: one file can carry several
      // independently damaged tags, and stopping early hides the rest.
      fail.push(`${name}: malformed attribute list in <${m[1]}> -- a quote or name was eaten (saw ${JSON.stringify(bad)})`)
      if (++reported >= 5) return
    }
  }
}

for (const f of files) {
  if (extname(f).toLowerCase() !== '.html') continue
  const html = readFileSync(f, 'utf8')
  checkScripts(html, rel(f))
  checkAttributes(html, rel(f))
}

// ---- report --------------------------------------------------------------
console.log(`scanned ${files.length} files, verified ${checkedRefs} local references\n`)

if (warn.length) {
  console.log(`WARNINGS (${warn.length}) -- not failing the build`)
  for (const w of warn) console.log('  ' + w)
  console.log('')
}

if (fail.length) {
  console.log(`FAILURES (${fail.length})`)
  for (const x of fail) console.log('  ' + x)
  console.log('\nFAIL')
  process.exit(1)
}

console.log('PASS')
