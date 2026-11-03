# Editorial workflow

## 1. Establish the evidence base

Read the title page, abstract, method, experiments, conclusion, captions, tables, references, and publication metadata. Do not rely on the abstract alone. Record each numerical statement together with its table/figure/page source.

Resolve these fields before publication:

- paper title and preferred public-facing Chinese title;
- author order, affiliations, correspondence marks, and contact details;
- venue, publication status, year, DOI, and full citation;
- publication timeline exactly as printed on the paper front page (Received / Revised / Accepted / Available online, or IEEE's "Date of publication" and "date of current version"), with no stage inferred or back-calculated;
- problem definition, method novelty, training/inference design;
- datasets, baselines, metrics, best/second-best conventions;
- limitations or conditions that narrow a claim — recorded on the fact sheet only, never turned into a section of the article.

If a Chinese author name is not printed in an authoritative source supplied by the user, keep the Romanized name or ask the user. Never transliterate and present it as verified, and do not add a note apologising for the English spelling.

If the PDF is an author version with no journal header, DOI, or dates, take the venue metadata from the publisher record (IEEE Xplore shows "Date of Publication" for early-access items) and say in the delivery note where it came from. Never infer a received/accepted date from the PDF's creation timestamp.

## 2. Study the reference article

Separate content structure from visual styling. Typical research-group article order:

1. public-facing headline outside the copied body;
2. centered English paper title;
3. authors, affiliations, email, venue, citation, publication note;
4. numbered paper introduction;
5. method overview and component explanations;
6. experiments, quantitative tables, and visual comparisons;
7. conclusion and optional paper/code links.

Match only conventions visible in the supplied reference. Do not assume that every account uses the same colors, font sizes, or section numbering.

## 3. Draft for a technical public audience

### 3.1 Stance

The account belongs to the group being written about. Treat the article as promotion and keep every judgement inside that frame.

- Never add a limitations, evidence-boundary, or open-questions section, and never close with a list of criticisms.
- Numbers stay exact; the framing stays neutral or positive. A setting the method does not win becomes 与基线各有高低 in one clause, not a paragraph on why the baseline leads.
- Limitations the authors state themselves may be carried over as future work (轻量化、后续引入渲染先验), without comment.
- Keep reviewer vocabulary out of the body: 证据边界、论文未解释、要打折扣、覆盖不足、没有做到全覆盖. A genuine mismatch between text and table belongs in the delivery note, for the user to raise with the authors privately.
- Do not explain that author names are Romanised or that Chinese names are unavailable; keep them exactly as printed.

### 3.2 Prose

The reader is a researcher, not someone skimming a landing page. Write dense.

- Delete lead-ins that announce the next sentence instead of making a claim: 值得注意、需要说明、不难看出、我们先来看、这里有两个设计选择.
- Delete tautologies. After a clause has already implied the conclusion ("点越贴近对角线，线性相关就越高"), the sentence adds nothing.
- Do not restate in the body what the caption already says.
- Prefer the number to the adverb. 非常、极其、相当、明显地 usually marks a place where a value was available and unused.
- Three to five sentences per paragraph, one claim each. Vary sentence length instead of scaffolding with 首先/其次/最后.
- Analogies and rhetorical questions only when they shorten the explanation; no decorative metaphors.

### 3.3 Content and house wording

- State the research problem before module names.
- Explain what each component changes and why it matters.
- Keep equations only when they clarify the mechanism; add a plain-language explanation.
- Tie claims to named datasets and metrics. Avoid “全面领先” unless the complete relevant comparison supports it.
- Explain arrows such as ↑ and ↓ the first time metrics appear.
- Keep technical names and casing consistent with the paper.
- House wording for this account: label the corresponding author as 通讯作者, never 通信作者, in the `作者` metadata line and anywhere else in the Chinese copy.
- House wording for the publication-timeline note: place one note directly under the metadata block (作者／单位／邮箱／发表期刊／DOI／引用) and state the dates in the journal's own English labels, in this form:

  ```
  卷期页码与在线发表日期请以期刊正式出版信息为准（Received 25 February 2026；Revised 7 July 2026；Accepted 21 July 2026；Available online 29 July 2026）。
  ```

  - Keep the English labels as printed (Received / Revised / Accepted / Available online; for IEEE letters the front page uses "Date of publication" and "date of current version", so map the publication date to Available online and, if useful, add the current-version date the same way).
  - Limit the entries to the stages the paper actually prints. Do not invent an Accepted date when only Received and Available online are given, and do not translate the labels into Chinese (收稿／修回／录用／上线).
  - Separate entries with a full-width semicolon `；` and wrap the whole list in full-width parentheses `（）`.
  - Drop the 卷期页码 caveat only when the user says the paper needs no such caveat; by default keep the sentence as written above even for articles whose volume and pages are already fixed.

When `humanizer-zh` is available and requested, use it only after the factual draft is stable. Recheck every number and technical relationship afterward.

## 4. Choose visual assets

Use a compact visual sequence that tells the paper's story: motivation, overall architecture, core components, main quantitative result, qualitative result, and ablation if useful. Preserve figure/table identifiers from the paper in captions, even if the article assigns a separate display sequence.

Prefer, in order:

1. original author-provided figure or LaTeX asset;
2. vector extraction from the PDF;
3. a high-resolution page crop at 200–300 DPI.

Do not crop away legends, axis labels, footnotes, ↑/↓ markers, bold/underline result markers, or subfigure labels. Do not resize a table so aggressively that mobile text becomes unreadable.

## 5. Headline candidates

The WeChat headline is entered in the editor's own title field, so it sits outside the copied body and has to be delivered separately. Produce two or three candidates and write each one into the markdown front matter as its own `title-candidate:` line; the builder lists them above the article with a character count and a copy button.

House format for this account:

```
<journal abbreviation> | <model name>：<Chinese rendering of the English subtitle>
```

- Use an ASCII pipe `|` (U+007C). Never the character 丨 (U+4E28) and never the full-width ｜ (U+FF5C).
- Put exactly one ASCII space on each side of the pipe: `JOE | WaterDiff：…`, not `JOE|WaterDiff：…`.
- The colon is the full-width `：`.
- The Chinese rendering compresses the English subtitle into "modifier + task name". Do not append a generic 方法/模型 tail.
- Journal abbreviation: take the JCR (Web of Science) abbreviation in capitals, for example `INFORM FUSION` or `IEEE J OCEANIC ENG`. IEEE journals are a known conflict — the account's earlier articles shipped community short codes such as `TMM` and `TCSVT`, which do not match the JCR style. When both readings are defensible, give one candidate per route instead of silently choosing.
- Keep each candidate within 64 characters. The subscription feed shows only about the first 20, so the abbreviation plus model name must not consume all of them.
- Vary the candidates rather than rewording one: one strictly following the rule, one matching the look of already-published articles, one shorter and mechanism-forward.

Also draft a share summary of at most 120 characters for the delivery note. Neither the headline nor the summary belongs in the article body.
