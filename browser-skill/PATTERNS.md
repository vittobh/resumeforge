# Browser Navigation Patterns

Reusable patterns for logged-in websites, portfolio apps, and ResumeForge UI checks.

## Pattern 1: Read-Only Review

Use when user says "check", "review", "see if updated".

```text
open/claim page
observe title + URL
find target section
read exact visible content
report missing/present
do not edit
```

Example output:

```text
Checked. About section shows GitHub short link, but not full URL.
Missing: https://github.com/vittobh/
```

## Pattern 2: Draft Then Save

Use for LinkedIn, Naukri, GitHub profile, job portals.

```text
open profile
open editor
read current value
create improved draft
fill draft
verify field contains draft
show draft to user
wait for `save`
click Save
verify visible page updated
```

## Pattern 3: Single Field Edit

Use for headline, title, URL, summary.

```text
field = unique selector
count(field) == 1
old = read field
new = transform(old)
fill(new)
read back
show diff
save only after confirm
```

## Pattern 4: Multi-Step App Flow

Use for ResumeForge:

```text
paste JD
click Parse JD
verify questions visible
answer 5 questions
select model
click Generate
verify scores visible
verify provenance table visible
```

## Pattern 5: Modal Editor

Use for Naukri and LinkedIn dialogs.

```text
click section edit
verify modal heading
locate textarea/input inside active modal
read value
fill draft
verify character count if present
save only after user says save
verify modal closed
verify profile page text changed
```

## Selector Ladder

Use strongest available selector:

```text
data-testid
id
name
aria-label
label text
role + name
section-scoped CSS
DOM node id
coordinate
```

## Verification Signals

Choose one clear signal:

```text
field value equals draft
button became enabled
modal heading visible
success toast visible
URL changed
saved text visible outside modal
result panel displayed
download button visible
```

## Save Confirmation Template

```text
Ready to save.

Will update:
- Resume headline: ...
- Profile summary: ...
- Key skills: ...

Reply `save` to publish.
```

## ResumeForge Manual Test Script

```text
1. Open https://vittobh.github.io/resumeforge/
2. Paste sample JD into #jd.
3. Click Parse JD.
4. Confirm #questions renders 5 questions.
5. Fill each answer with public-safe dummy data.
6. Select Claude or Gemini.
7. Click Generate Tailored Resume.
8. Confirm #ats-score, #human-score, #bullets, #provenance visible.
9. Do not download unless user asks.
```

## Naukri Premium Profile Pattern

High-value fields:

```text
Resume headline
Key skills
Profile summary
Employment bullets
Projects
Online profile / portfolio links
```

Preferred positioning:

```text
Product Manager / Lead Product Owner
Agentic AI
RAG
Healthcare Data Products
BFSI Platforms
Enterprise SaaS
API Platforms
Product Strategy
PRD / BRD
Roadmaps
Agile Delivery
```

Never overstuff. Use keywords naturally.

## LinkedIn Premium Profile Pattern

High-value fields:

```text
Headline
About
Featured links
Experience bullets
Skills
Open to work titles
```

About ending pattern:

```text
Portfolio: https://vittobh.github.io/vittobh/
GitHub: https://github.com/vittobh/
Open to Product Manager, Lead Product Owner, AI Product Manager, and AI Platform PM roles.
```

