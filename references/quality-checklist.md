# Quality checklist

## Content

- English title, author order, affiliations, correspondence marks, venue, year, DOI, and citation match the source.
- The publication-timeline note sits directly under the metadata block, keeps the journal's English date labels, and reproduces the front-page dates without translating or inferring any stage.
- Every number can be traced to the cited figure, table, or passage.
- Dataset names, metric arrows, best/second-best markers, and method names are explained correctly.
- Chinese author names, if used, are authoritative rather than guessed.
- Two or three headline candidates are supplied, each following the account's `<abbreviation> | <model>：<rendering>` form and staying within 64 characters.
- No drafting placeholders, private notes, or unsupported “state-of-the-art” claims remain.

## Voice

- The article reads as an introduction, not a referee report: no limitations section, no evidence-boundary section, no closing list of problems.
- Numbers are exact and the framing is neutral or positive; a losing setting is one clause, not a paragraph explaining the winner.
- Author-stated limitations appear only as future work, without evaluation.
- No note explaining Romanised author names or missing Chinese names.
- No filler: every sentence carries information, captions are not restated, tautologies are cut, and adverbs do not stand in for numbers.
- Paragraphs run three to five sentences with one claim each.

## Visual assets

- Each caption identifies the original paper figure/table/equation number.
- Crops contain full legends, labels, subfigure letters, table notes, and equation numbers.
- Tables and equations remain readable at approximately 375 px viewport width.
- No figure is duplicated, missing, or out of narrative order.
- Separate image files are available in case WeChat rejects embedded clipboard images.

## HTML and paste behavior

- The output opens offline and has no unintended external image/font dependencies.
- All intended images use `data:` URLs when embedding is enabled.
- The copy action selects only `article#article`.
- Headline candidates sit above `article#article`, are absent from the copied body, and each shows a character count and a working copy button; a paste into a rich-text surface must not carry them along.
- Desktop and narrow/mobile views have no horizontal overflow.
- Headings, body size, line height, color, margins, captions, and notes resemble the supplied reference.
- A test paste into a disposable rich-text surface preserves headings and images when the environment permits it.

WeChat may sanitize CSS and convert pasted images into uploaded media. After paste, wait for uploads to finish, check every image, preview on mobile, and manually replace missing images from the exported image folder.

## Publication and repository hygiene

- Confirm image reuse and paper-publication permissions.
- Remove unpublished papers, generated articles, author emails, access tokens, browser data, and local absolute paths from public repositories.
- Never treat a successful local preview as authorization to publish.
