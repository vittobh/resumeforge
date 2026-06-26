# Browser Skill

Use this skill when an AI agent must navigate a website, test a browser UI, fill forms, or verify a user-facing flow.

This skill is designed for Codex with Chrome plugin, but the pattern also works for Claude Code, Gemini CLI, Cursor, or any AI agent with browser automation.

## Goal

Make browser work reliable:

1. Observe current page state.
2. Pick one unique target.
3. Act once.
4. Verify result.
5. Ask before saving, submitting, deleting, uploading, or publishing.

## Core Rule

Never click from memory. Always click from fresh page state.

Good:

```text
Snapshot shows one button named "Save". Count = 1. Click. Verify modal closed and text visible.
```

Bad:

```text
Clicked likely Save button because it was there earlier.
```

## Safe Browser Workflow

### 1. Open Or Claim Tab

Use existing logged-in tab when user asks for LinkedIn, Naukri, GitHub, Gmail, Drive, or other account pages.

Do not inspect cookies, passwords, local storage, browser profiles, or secret stores.

### 2. Observe

Prefer DOM/accessibility snapshot before screenshots.

Collect:

- URL
- title
- visible headings
- buttons
- links
- form labels
- current field values where relevant

### 3. Locate Target

Preferred locator order:

1. `data-testid`
2. stable `id`
3. stable `name`
4. label text
5. role + accessible name
6. scoped CSS inside known section
7. DOM node id from visible DOM
8. coordinates only as last resort

### 4. Count Before Action

Before click, fill, check, or press:

- locator count must be `1`
- if count is `0`, re-observe
- if count is `>1`, scope tighter

### 5. Act

One action at a time.

Examples:

- fill headline
- click edit icon
- select radio
- press Enter
- click parse JD

### 6. Verify

After action, verify one specific signal:

- field value changed
- modal opened
- modal closed
- URL changed
- success toast appeared
- generated result visible
- uploaded file name visible

### 7. Save Gate

Always ask before final action if it creates external side effect:

- Save LinkedIn profile
- Save Naukri profile
- Submit application
- Send message
- Upload resume
- Delete data
- Publish public page

Use exact confirmation:

```text
Ready to save. Will publish:
- field 1
- field 2

Reply `save`.
```

## Form Fill Pattern

```text
observe page
find field by label/id
count field = 1
read current value
fill draft
read filled value
show user draft
wait for save confirmation
click save
verify saved text visible
```

## ResumeForge UI Pattern

ResumeForge prototype flow:

1. Upload master resume
2. Paste target JD
3. Click `Parse JD`
4. Answer 5 discovery questions
5. Select model
6. Click `Generate Tailored Resume`
7. Verify ATS score, Human score, bullets, provenance map
8. Download mock docx only after user asks

Important selectors:

```text
#resume-file
#jd
button text: Parse JD
#questions
input[name="model"]
button text: Generate Tailored Resume
#results
#ats-score
#human-score
#bullets
#provenance
```

## ResumeForge Test Data

Use dummy public-safe text only.

Sample JD:

```text
Product Manager, AI Platforms. Own roadmap, PRDs, RAG evaluation, agentic workflows, stakeholder alignment, API integrations, and KPI reporting for enterprise SaaS.
```

Sample discovery answers:

```text
Q1: Improved workflow turnaround by 40% and reduced manual effort by 60%.
Q2: Led 8-member cross-functional team across product, design, data, and engineering.
Q3: Chose RAG with human-in-the-loop validation over fully autonomous generation due compliance risk.
Q4: Validated requirements through stakeholder interviews, wireframes, and UAT feedback.
Q5: Launched 0-to-1 AI workflow from POC to production-ready pilot.
```

## Agent Prompt

Use this prompt with Codex, Gemini, Claude, or Cursor:

```text
You are browser automation agent. Use observe-click-verify discipline.

Rules:
- Do not click from memory.
- Use fresh DOM/snapshot before every meaningful action.
- Count target before click or fill.
- Use unique selectors only.
- Fill draft changes first.
- Stop before Save/Submit/Publish/Delete/Upload and show exact change summary.
- After user says save, click Save once and verify saved state.

Current task:
[describe website, page, and fields to update]
```

## Anti-Patterns

Avoid:

- repeated blind clicks
- using stale node ids
- using `.first()` without count
- broad body text scraping as first move
- coordinate click before trying DOM
- saving public profile without user confirmation
- typing sensitive data into wrong field
- editing unrelated fields

## Recovery

If click fails:

1. Take fresh snapshot.
2. Check if modal/page changed.
3. Rebuild locator.
4. Try one stronger selector.
5. If still blocked, ask user to take over exact step.

If tab disappears:

1. list open tabs
2. claim matching URL/title
3. continue only after verifying URL and page title

If form reloads:

1. do not assume draft persisted
2. reopen editor
3. re-read current value
4. fill again
5. verify

