# PDF crop manifest

`crop_pdf_regions.py` renders named rectangular regions directly from a PDF through Poppler's `pdftoppm`.

Coordinates use PDF points measured from the page's top-left corner: 72 points equal one inch. Page numbers are one-based.

```json
{
  "dpi": 240,
  "regions": [
    {
      "page": 3,
      "name": "framework",
      "bbox": [45, 120, 550, 430]
    },
    {
      "page": 7,
      "name": "equation-6",
      "bbox": [80, 210, 510, 285],
      "dpi": 300
    }
  ]
}
```

`bbox` is `[left, top, right, bottom]`. The script converts points to pixels and produces PNG files. Determine regions by inspecting rendered full pages; keep a small margin around rules, legends, equation numbers, and table notes.

Run `python scripts/crop_pdf_regions.py paper.pdf crop-manifest.json figures`.

Set the `PDFTOPPM` environment variable when `pdftoppm` is not on `PATH`.

## Finding the box

When PyMuPDF is available it is the more reliable route: `page.get_pixmap(dpi=300, clip=rect, annots=False)` skips link annotations, which `pdftoppm` renders as coloured frames over reference numbers.

- For a figure, take the caption block from `get_text('blocks')` (it starts with `Fig. N.`). The figure ends where that block begins; the figure starts where the preceding text block ends.
- Row labels such as `Reference`, `View 1 (Source)` and `MOS=8.000` live in text blocks, not in `get_image_info`. A box built only from image rectangles clips them, so move the top edge up to the label block's `y0 - 2`.
- For a table, take the caption block's bottom and the last text or rule below it; horizontal rules come from `get_drawings()` as items with height < 2.5 pt.
- Render each crop once and look at it before accepting the batch. Clipped labels and cut-off last rows are the two usual failures.

