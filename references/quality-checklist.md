# Quality checklist

## Content

- English title, author order, affiliations, correspondence marks, venue, year, DOI, and citation match the source.
- Every number can be traced to the cited figure, table, or passage.
- Dataset names, metric arrows, best/second-best markers, and method names are explained correctly.
- Chinese author names are authoritative, not guessed.
- Claims preserve conditions, exceptions, and limitations.
- No drafting placeholders, private notes, or unsupported “state-of-the-art” claims remain.

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
- Desktop and narrow/mobile views have no horizontal overflow.
- Headings, body size, line height, color, margins, captions, and notes resemble the supplied reference.
- A test paste into a disposable rich-text surface preserves headings and images when the environment permits it.

WeChat may sanitize CSS and convert pasted images into uploaded media. After paste, wait for uploads to finish, check every image, preview on mobile, and manually replace missing images from the exported image folder.

## Publication and repository hygiene

- Confirm image reuse and paper-publication permissions.
- Remove unpublished papers, generated articles, author emails, access tokens, browser data, and local absolute paths from public repositories.
- Never treat a successful local preview as authorization to publish.
