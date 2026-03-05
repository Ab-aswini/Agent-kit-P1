# Marketing & Growth Workflow

> Optimize marketing pages, implement technical SEO schemas, and run CRO audits using the 25 Advanced Marketing Skills.

## Trigger

- Marketing integration request
- SEO / AEO optimization demand
- Conversion rate drop detected

## Agent Sequence

### Step 1: SEO & CRO Audit

**Agent:** MKT-001 (SEO/AEO Specialist)

- Run `seo-audit` skill on the target domain/page.
- Run `page-cro` skill to identify conversion bottlenecks.
- Check `schema-markup` for missing JSON-LD.

### Step 2: Content & Copy Strategy

**Agent:** MKT-001 (or delegated content specialist)

- Implement `copywriting` and `marketing-psychology` skills to draft high-converting hero sections.
- Define `pricing-strategy` if upgrading pricing pages.

### Step 3: Implementation

**Agent:** FE-001 or suitable Frontend Dev

- Add the `schema-markup` structured data to the Next.js/React `head`.
- Adjust the layout per `page-cro` recommendations.

### Step 4: Verification

**Agent:** QA-001 → CTS-001

- Ensure performance metric compliance (Lighthouse).
- Verify standard anti-hallucination validation before closing workflow.
