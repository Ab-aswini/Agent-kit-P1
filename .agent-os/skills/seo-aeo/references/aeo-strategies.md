# AEO — Answer Engine Optimization Strategies

AEO = getting cited by ChatGPT, Perplexity, Gemini, Claude, Copilot when users ask questions.
SEO gets you ranked. AEO gets you cited. Both are required now.

---

## Core AEO Principles

### 1. Inverted Pyramid Structure
Answer FIRST. Context second. Detail third.
AI models extract the first direct answer they find. Put yours at the top.

```
[DIRECT ANSWER — first paragraph]
[SUPPORTING CONTEXT — why/how]
[DETAILED EXPLANATION — depth]
[RELATED INFORMATION — surrounding entities]
```

### 2. Direct Answer Blocks
Every major topic needs a boxed/highlighted definition block:

```html
<div class="answer-block" itemscope itemtype="https://schema.org/Answer">
  <h3>What is [TOPIC]?</h3>
  <p itemprop="text">
    [TOPIC] is [direct 1-sentence definition]. It works by [mechanism]. 
    Primary benefit: [value]. Used for: [use cases].
  </p>
</div>
```

### 3. Question-Based Headers (H2/H3)
Mirror exact user queries — including how they'd phrase it to an AI:

| ❌ Don't | ✅ Do |
|----------|-------|
| Our Services | What Services Does [Brand] Offer? |
| About Pricing | How Much Does [Service] Cost in India? |
| Features | What Are the Key Features of [Product]? |
| Contact Us | How Can I Contact [Brand]? |
| Why Choose Us | Why Do [City] Businesses Choose [Brand]? |

### 4. Cited Statistics
AI engines trust and cite pages that cite authoritative sources.

Required citations per page:
- 1-2 government sources (data.gov.in, mospi.gov.in, mca.gov.in)
- 1-2 industry reports (NASSCOM, IBEF, CII, industry associations)
- Published research with DOI or source URL

Format: `"According to [Source Name] ([Year]), [statistic]."` — match exactly how AI engines cite.

### 5. Entity Coverage Map
Every page must mention related named entities. Build an entity map per page:

```
Page topic: [X]
People entities: [experts, founders, thought leaders in field]
Place entities: [cities, regions, countries where relevant]
Organization entities: [companies, institutions, bodies related to topic]
Product/Service entities: [specific named products, tools, platforms]
Concept entities: [related technical terms, methodologies, frameworks]
```

Use these entities naturally in the content. LLMs use entity co-occurrence to assess topical authority.

### 6. Passage Indexing Optimization
Google and AI models extract individual passages. Every paragraph must be:
- Self-contained (makes sense without surrounding context)
- Independently understandable
- Max 3-4 sentences
- Contains at least one semantic keyword

### 7. Structured Content per Page

```
H1: [Primary Keyword — matches user search intent exactly]

INTRO (2 sentences):
  → WHO THIS IS FOR + WHAT THIS PAGE COVERS

H2: What is [Topic]?
  → Direct definition paragraph (AEO anchor)

H2: How Does [Topic] Work?
  → Step-by-step or mechanism explanation

H2: [Primary Use Case / Benefit]
  → Evidence-backed, entity-rich section

H2: [Comparison / vs. Alternative]
  → Commercial intent coverage

H2: Frequently Asked Questions About [Topic]
  → 5-8 Q&As with FAQPage schema

H2: [CTA Section]
  → Conversion section
```

### 8. FAQ Requirements per Page
- Minimum 5 questions, maximum 10
- Questions must match actual user queries (use Google's "People Also Ask" and AnswerThePublic)
- Each answer must be 40-300 words
- First sentence of each answer must stand alone as a complete answer
- Deploy FAQPage schema on every page with FAQs

### 9. E-E-A-T Signals for AEO

AI engines weight E-E-A-T when deciding what to cite:

```
Experience  → "Based on our work with X clients..." / Case studies / Real examples
Expertise   → Author credentials / Technical depth / Accurate terminology
Authority   → Cited by others / Backlinks / Schema-verified authorship
Trust       → HTTPS / Contact info / Privacy policy / Verifiable facts
```

Required trust elements per page:
- Author name + bio + author schema markup
- Date published + date modified
- At least 2 external citation links to authoritative sources
- Clear organization affiliation

### 10. AI-Readable Content Patterns

Write content in patterns AI engines extract well:

**Definition pattern:**
```
[Term] is defined as [definition]. [Term] differs from [related term] in that [distinction].
```

**Process pattern:**
```
[Task] involves [N] steps: First, [step 1]. Then, [step 2]. Finally, [step 3].
```

**Comparison pattern:**
```
[Option A] and [Option B] differ primarily in [dimension]. [A] is better for [use case A]. [B] is preferable when [use case B].
```

**Statistic pattern:**
```
According to [Source] ([Year]), [statistic]. This means [implication for reader].
```

---

## AEO Audit Checklist per Page

```
□ Direct answer in first 100 words?
□ All H2/H3 headers phrased as questions?
□ 5+ FAQ items with FAQPage schema?
□ 2+ authoritative external citations?
□ Entity map covered (people, places, organizations)?
□ Every paragraph self-contained?
□ Author bio with schema markup?
□ HowTo schema if page is instructional?
□ Answer blocks for key definitions?
□ Word count matches top 3 competitors?
□ Reading level Grade 8-10?
□ Date published/modified visible?
```
