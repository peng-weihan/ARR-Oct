# Construct Validity Brief Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a concise two-page Chinese memo and matching PDF that explain HEART-Bench's construct-validity concern and practical remedies for discussion with an academic advisor.

**Architecture:** The Markdown file is the canonical content source. A temporary ReportLab conversion script will render the same content into an A4 PDF with embedded Chinese fonts, after which every page will be rasterized and visually inspected.

**Tech Stack:** Markdown, Python 3, ReportLab, PyMuPDF, Arial Unicode font.

## Global Constraints

The brief must use formal, concise prose and should avoid dense itemized exposition. It must distinguish the benchmark's direct measurement from broader human-psychology claims, separate immediate manuscript changes from stronger empirical additions, and remain approximately two A4 pages. Do not commit files unless the user explicitly requests a commit.

---

### Task 1: Write the concise advisor memo

**Files:**
- Create: `CONSTRUCT_VALIDITY_BRIEF.md`
- Reference: `CONSTRUCT_VALIDITY_MEMO.md`
- Reference: `CONSTRUCT_VALIDITY_REVISION_GUIDE.md`

**Interfaces:**
- Consumes: Evidence and recommendations from the two existing construct-validity documents.
- Produces: The canonical Markdown source used by the PDF renderer.

- [ ] **Step 1: Draft the central issue**

Write a title and opening section that states that HEART-Bench directly measures expert-reference agreement for memory-grounded, persona-consistent action selection in controlled synthetic scenarios. Clarify that this operationalization does not directly measure observed human psychology or behavior.

- [ ] **Step 2: Select the minimum supporting evidence**

Write concise paragraphs covering four points: all personas and memories are synthetic; experts adjudicate consistency with predefined persona specifications rather than real-person outcomes; model-family involvement and input cues may create shortcut signals; and a single-turn MCQ does not by itself validate broad agent-psychology claims.

- [ ] **Step 3: Explain the submission risk**

State that retaining “human-like psychology” as the direct measured construct may invite a construct-validity objection because low or high benchmark accuracy has multiple alternative explanations.

- [ ] **Step 4: Present staged solutions**

Describe immediate manuscript revisions in one subsection: narrow the title and claims, define reference-label accuracy, replace ground-truth terminology, and add an explicit scope limitation. Describe stronger empirical additions in a second subsection: strict anonymization and shortcut ablations, source-independent evaluation, and a same-information human comparison or open-ended convergent-validity study.

- [ ] **Step 5: Conclude with the recommended positioning**

End with the recommended framing of HEART-Bench as a controlled benchmark for psychology-informed, memory-grounded persona consistency. Include one reusable English operational-definition paragraph.

- [ ] **Step 6: Verify scope and terminology**

Run:

```bash
wc -w CONSTRUCT_VALIDITY_BRIEF.md
rg -n "human-like psychology|ground truth|real human behavior|persona-consistent|reference-label" CONSTRUCT_VALIDITY_BRIEF.md
```

Expected: the memo is concise enough to render in approximately two A4 pages; every occurrence of broad human-psychology terminology is explicitly qualified; the recommended terminology appears consistently.

### Task 2: Render and validate the PDF

**Files:**
- Create: `output/pdf/CONSTRUCT_VALIDITY_BRIEF.pdf`
- Create temporarily, then delete: `tmp/pdfs/render_construct_validity_brief.py`
- Create temporarily, then delete: `tmp/pdfs/rendered/CONSTRUCT_VALIDITY_BRIEF/*.png`

**Interfaces:**
- Consumes: `CONSTRUCT_VALIDITY_BRIEF.md`.
- Produces: A polished, visually verified A4 PDF.

- [ ] **Step 1: Build the PDF renderer**

Create a temporary ReportLab script that supports the Markdown structures used in the brief, embeds `/Library/Fonts/Arial Unicode.ttf`, uses A4 margins of approximately 18–20 mm, and adds restrained headers, footers, and page numbers.

- [ ] **Step 2: Generate the PDF**

Run:

```bash
python3 tmp/pdfs/render_construct_validity_brief.py \
  CONSTRUCT_VALIDITY_BRIEF.md \
  output/pdf/CONSTRUCT_VALIDITY_BRIEF.pdf
```

Expected: the command exits successfully and produces a nonempty PDF.

- [ ] **Step 3: Perform structural validation**

Open the PDF with PyMuPDF and verify that it has two nonempty pages and contains no Unicode replacement glyphs.

Expected: `pages=2`, `empty_pages=none`, and `replacement_glyphs=0`.

- [ ] **Step 4: Perform visual validation**

Rasterize both pages to PNG and inspect typography, paragraph spacing, page transitions, English-Chinese wrapping, and footer placement.

Expected: no clipped text, broken glyphs, excessive word spacing, raw Markdown syntax, or overflow.

- [ ] **Step 5: Clean temporary artifacts**

Delete the temporary renderer and page images after the final PDF passes validation. Preserve only `CONSTRUCT_VALIDITY_BRIEF.md` and `output/pdf/CONSTRUCT_VALIDITY_BRIEF.pdf`.
