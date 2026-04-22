# Link Resolution in Hugo Pretty-URL Mode

Cross-quadrant links in Diataxis content are surprisingly easy to get
wrong. The bug is not in Hugo or the theme — it is in the gap between
how writers think about Markdown (source-tree terms) and how browsers
actually resolve relative links in rendered HTML (URL terms, per
RFC 3986). This reference explains why, documents the correct form
for every source-location × target-location pair, and describes the
lints that catch miswritten links before build.

## Why relative links break: pretty URLs + RFC 3986

Hugo's pretty-URL mode publishes `content/tutorials/foo.md` to
`public/tutorials/foo/index.html`, so the browser serves it at the URL
`/tutorials/foo/` — **with a trailing slash**. That trailing slash is
load-bearing. When the browser resolves a relative link on that page,
RFC 3986 §5.3 does the following:

1. Take the base URL of the current page. If the path ends with `/`,
   everything up to and including that `/` is the "reference
   directory."
2. Append the relative reference to the reference directory.
3. Normalize `.` and `..` segments.

So from a page loaded at `/tutorials/foo/`:

| Relative link            | Resolution                                     | Result                |
|--------------------------|------------------------------------------------|-----------------------|
| `bar/`                   | `/tutorials/foo/` + `bar/`                     | `/tutorials/foo/bar/` |
| `../bar/`                | `/tutorials/foo/` + `../bar/` → pop `foo/`, add `bar/` | `/tutorials/bar/`     |
| `../../bar/`             | pop `foo/`, pop `tutorials/`, add `bar/`       | `/bar/`               |
| `../../explanation/bar/` | pop two, add `explanation/bar/`                | `/explanation/bar/`   |

The **intuition trap**: writers think of `../` as "one directory up from
this source file." From `tutorials/foo.md`, `../explanation/bar.md`
points to the sibling `explanation/` directory in the source tree —
correct in a filesystem. But the rendered URL is `/tutorials/foo/`,
one level *deeper* than the source implies. The first `../` only exits
the page's own URL directory (`/tutorials/foo/` → `/tutorials/`); it
does not exit the quadrant. Every `../` must be counted in URL space,
not source space.

## Hugo does not rewrite directory-form relative links

With `relativeURLs = true`, Hugo rewrites *absolute* URLs
(`/explanation/bar/`) to the correct page-relative form during
rendering. Absolute paths "just work" everywhere.

**Directory-form relative links pass through unchanged.** Hugo has no
way to tell whether `../explanation/bar/` means a page reference or an
arbitrary URL path, so it does not touch them. The browser resolves
them per RFC 3986.

There is one exception: links written with a `.md` suffix (like
`[x](../explanation/bar.md)`) can be resolved by Hugo's render-link
hooks, which a theme may register to produce canonical URLs regardless
of source depth. The Hextra theme used by this skill does **not**
register such a hook, and Diataxis's authoring convention forbids `.md`
suffixes anyway. So directory-form links must be correct by
construction.

## The correct form by source location

### Content files (`tutorials/foo.md` and siblings)

Served at `/tutorials/foo/` — two URL segments deep.

| Target                    | Preferred (absolute) | Relative form            |
|---------------------------|----------------------|--------------------------|
| Same-quadrant sibling     | n/a — rare to use absolute for a sibling | `../bar/` |
| Cross-quadrant target     | `/explanation/bar/`  | `../../explanation/bar/` |
| Exercise bundle           | `/exercises/bar/`    | `../../exercises/bar/`   |
| Site homepage             | `/`                  | `../../`                 |

### Quadrant landing pages (`tutorials/_index.md`)

Served at `/tutorials/` — one URL segment deep.

| Target                   | Preferred (absolute) | Relative form         |
|--------------------------|----------------------|-----------------------|
| Same-quadrant content    | `/tutorials/bar/`    | `bar/` (no `../`)     |
| Cross-quadrant target    | `/explanation/bar/`  | `../explanation/bar/` |
| Exercise bundle          | `/exercises/bar/`    | `../exercises/bar/`   |

Note that the relative forms on `_index.md` are different from the ones
on content files: one fewer `../` everywhere, because the landing page's
URL is one segment shallower.

### Site homepage (`index.md`)

Served at `/` — zero URL segments deep.

| Target                | Preferred (absolute) | Relative form       |
|-----------------------|----------------------|---------------------|
| Any page              | `/tutorials/bar/`    | `tutorials/bar/`    |
| Exercise bundle       | `/exercises/bar/`    | `exercises/bar/`    |

## Three patterns that look right but are wrong

1. **`[x](../explanation/bar/)` inside a tutorial file.** Feels natural
   because `explanation/` is a sibling of `tutorials/` in source space.
   But the URL is `/tutorials/foo/`, so `../` only gets you to
   `/tutorials/`. Result: 404 at `/tutorials/explanation/bar/`.

2. **`[x](bar/)` (no `../`) inside any content file.** Feels like
   "a page named `bar` in the same section." Resolves to
   `/tutorials/foo/bar/` — a nested URL that does not exist.
   Same-quadrant siblings always need `../bar/`.

3. **`[x](../tutorials/bar/)` inside a tutorial file.** Same bug with
   an extra layer: source says "go up, then into `tutorials/`" (fine in
   source space), but the URL resolves it to `/tutorials/tutorials/bar/`.
   Same-quadrant targets use `../bar/`, never `../<own-quadrant>/bar/`.

## A safer authoring rule: prefer absolute paths

Because `relativeURLs = true` rewrites absolute URLs to the correct
per-page form at build time, authors who use absolute paths
(`/explanation/bar/`, `/reference/api/`, `/exercises/foo/`) never have
to count `../` segments. This is the recommended authoring style for
cross-quadrant and exercise links; use `../bar/` for same-quadrant
siblings only (because absolute paths for siblings add noise without
benefit).

## A mental trick for getting relative forms right

If you need a relative form, ignore the source-file layout and work
purely in URL space:

1. Write the current page's URL with its trailing slash:
   `/tutorials/foo/`.
2. Write the target URL: `/explanation/bar/`.
3. Starting at the source URL's trailing slash, count `../` steps up
   until you reach the site root (`/`), then append the target path
   without its leading `/`.

Example: `/tutorials/foo/` → `/explanation/bar/`

- One `../` → `/tutorials/`
- Another `../` → `/`
- Append `explanation/bar/` → `/explanation/bar/`
- Total: `../../explanation/bar/`

The mechanical version: "every `/` in the source URL after the first
one is one `../`."

## Lints and verification

Two deterministic lints live in `skill/checks/check-link-form.nu` and
run as part of `nu checks/run-checks.nu`:

1. `](../<same-quadrant>/...)` inside any content file in that
   quadrant — resolves to `/<quadrant>/<quadrant>/...`; fix by dropping
   the quadrant name (`](../...)`).
2. `](../<other-quadrant>/...)` inside any content file — resolves to
   `/<quadrant>/<other>/...` (404); fix by adding another `../`
   (`](../../<other>/...)`) or switching to absolute
   (`](/<other>/...)`).

The check skips `_index.md` and `index.md` because their correct forms
are different — see the tables above. Fenced code blocks and inline
code are stripped before scanning so illustrative examples do not trip
the lint.

Build-time verification is also useful: after `make build`, grep the
rendered HTML for telltale paths that indicate a miswritten link
slipped through in a form the lint did not anticipate:

```bash
grep -ohE 'href="[^"]*"' public/ -r \
  | grep -E '(tutorials/tutorials|reference/reference|howto/howto|explanation/explanation)'
```

A non-empty result means a same-quadrant link was authored with the
quadrant name repeated.
