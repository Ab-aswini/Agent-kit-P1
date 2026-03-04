---
name: seo-aeo
description: >
  Full-stack SEO + AEO (Answer Engine Optimization) agent skill. Triggers when
  user mentions SEO, AEO, meta tags, schema markup, sitemap, robots.txt, Open
  Graph, structured data, keyword research, Google Search Console, Bing
  Webmaster, Google Business Profile, site indexing, search ranking, Core Web
  Vitals, or wants their website to appear in AI engine answers (ChatGPT,
  Perplexity, Gemini, Claude web search). Also triggers for: "optimize this
  page", "add schema", "create robots.txt", "generate sitemap", "what's my SEO
  score", "help me rank", "make this AI-readable", or any mention of
  crawlability, indexability, or discoverability.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# SEO + AEO Agent Skill — SERAPH

> **Philosophy:** Research first. Deploy second. Validate always.
> **Core Principle:** Human-first content, machine-optimized structure.

---

## 🎯 Selective Reading Rule (MANDATORY)

**Read REQUIRED files always, OPTIONAL only when needed:**

| File                                                          | Status          | When to Read                         |
| ------------------------------------------------------------- | --------------- | ------------------------------------ |
| [aeo-strategies.md](references/aeo-strategies.md)             | 🔴 **REQUIRED** | Always read first!                   |
| [technical-seo.md](references/technical-seo.md)               | ⚪ Optional     | robots.txt, sitemaps, meta, IndexNow |
| [schema-library.md](references/schema-library.md)             | ⚪ Optional     | Any JSON-LD schema needed            |
| [submission-checklist.md](references/submission-checklist.md) | ⚪ Optional     | GSC, Bing, GBP submissions           |

> 🔴 **aeo-strategies.md = ALWAYS READ. Others = only if relevant to the task.**

---

## Memory System

### Load Memory (Start of Every Task)

```bash
cat memory/project-memory.json
```

If file doesn't exist, run the intake flow and create it:

```bash
cp .agent-os/skills/seo-aeo/memory/project-memory.template.json memory/project-memory.json
```

### Save Memory (End of Every Task)

Update `memory/project-memory.json` with:

- Keywords researched and their intent classification
- Pages optimized and what schema was applied
- Submission status (GSC, Bing, GBP)
- Pending tasks
- Competitor insights discovered
- Core Web Vitals scores if measured

---

## Phase Flow — Follow This Order Every Time

### PHASE 0: Intake (if project-memory.json is empty or new)

Ask for or extract from existing files:

- Business name, URL, industry, geo, language, primary goal
- Top 3 competitor URLs
- Target audience (ICP)
- Any existing GSC/Analytics data

Then research:

1. Keyword universe (seed → LSI → long-tail → question-based → entity)
2. Search intent per keyword (Info / Nav / Commercial / Transactional)
3. Competitor schema audit — what types are they using?
4. AEO question mapping — what AI engines should cite this site for?

### PHASE 1: Technical Files

Generate in this order:

1. `robots.txt` → see `references/technical-seo.md` §robots
2. `sitemap_index.xml` → see `references/technical-seo.md` §sitemap
3. Full `<head>` meta block → see `references/technical-seo.md` §meta
4. Schema markup (JSON-LD) → see `references/schema-library.md`

### PHASE 2: AEO Content

Apply AEO rules from `references/aeo-strategies.md` to every page:

- Inverted pyramid structure
- Question-based H2/H3 headers
- FAQ schema on every page
- Entity coverage map
- Direct answer blocks

### PHASE 3: Submission & Verification

Follow checklist in `references/submission-checklist.md`:

- GSC property setup + sitemap submission
- Bing Webmaster + IndexNow API
- Google Business Profile
- Structured data validation commands

### PHASE 4: Monitoring Plan

Output weekly + monthly automation tasks.
For n8n workflows, generate the JSON trigger configs.

---

## Output Format

Always structure output as:

```text
## [ANALYST BRIEF]
## [KEYWORD STRATEGY]
## [TECHNICAL FILES] (ready to deploy)
## [CONTENT BLUEPRINT]
## [SUBMISSION CHECKLIST]
## [MONITORING PLAN]
## [MEMORY UPDATE] — show what was written to project-memory.json
```

---

## Absolute Rules

```text
✗ Never leave YOURDOMAIN.com unfilled in output code
✗ Never generate schema without validating it against schema.org spec
✗ Never create thin content pages (<300 words if indexed)
✗ Never block CSS/JS in robots.txt
✗ Never skip canonical tags on paginated or filtered pages
✗ Never output duplicate meta descriptions across pages
✗ Never skip the memory read at session start
✗ Never skip the memory write at session end
```

---

## Reference Files

| File                                  | Use When                                                |
| ------------------------------------- | ------------------------------------------------------- |
| `references/technical-seo.md`         | Generating robots.txt, sitemaps, meta tags, head blocks |
| `references/schema-library.md`        | Any JSON-LD schema markup needed                        |
| `references/aeo-strategies.md`        | Optimizing content for AI engine citation               |
| `references/submission-checklist.md`  | GSC, Bing, GBP, IndexNow setup steps                    |
| `memory/project-memory.template.json` | Creating new project memory files                       |

---

## Activation

To start a new project:

```text
SERAPH INIT — [Project Name] — [URL or "new"] — [Industry] — [Goal]
```

To continue existing project:

```text
SERAPH CONTINUE — [what needs to be done]
```

To audit an existing page:

```text
SERAPH AUDIT — [URL or file path]
```

---

## Related Skills

| Skill                                                          | When to Use                                      |
| -------------------------------------------------------------- | ------------------------------------------------ |
| **seo-aeo** (this)                                             | SEO strategy, schema, AEO content, submissions   |
| **[frontend-design](../frontend-design/SKILL.md)**             | Visual design decisions before coding            |
| **[web-design-guidelines](../web-design-guidelines/SKILL.md)** | Accessibility, performance, best practices audit |

---

> **Remember:** SEO gets you ranked. AEO gets you cited. Both are required now. Research first, deploy second, validate always.
