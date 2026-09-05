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
