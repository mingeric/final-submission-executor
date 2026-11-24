# 4. Visual QA and print specification

A successful plotting script is not evidence of a good figure. Inspect the actual rendered image at final physical size.

## Print gates

- Use the project's explicit width contract. A common two-column target is 183 mm at 600 dpi, height at or below the journal limit (for example 247 mm).
- Export RGB PNG unless the user explicitly requests another format.
- Verify decoded image dimensions, embedded DPI metadata, colour mode and SHA256 after every replacement.
- Typography must be readable at final print size, not at screen zoom. Increase font size, reduce annotation count, or move detail to supplements when needed.

## Geometry gates

Use the renderer's real text bounding boxes (`get_window_extent`) for collisions; grayscale heuristics fail on heatmaps and dense forests.

- Check text-vs-text overlap with a small tolerance.
- Check text crossing into a neighbouring panel using both x and y coordinates.
- Check out-of-page text.
- Exclude panel-letter gutters and page-level text from per-panel ownership checks, or they produce false positives.
- Assert row-height and label-space constraints programmatically where possible.

## Two visual passes

**Pass A — scientific composition.** Reject uniform dashboard layouts, weak hero panels, repeated evidence, unreadable small multiples, empty text-only panels, large blank regions, inappropriate geometry and disconnected narratives.

**Pass B — publication readability.** Reject clipped labels, broken colourbars, inconsistent units, wrong ranges, missing/zero ambiguity, overlapping annotations, inconsistent module colours, invalid significance marks and disconnected legends.

Procedure: render → inspect a whole-figure thumbnail → inspect 2x crops of dense regions → repair → rerender → inspect again. Geometry gates alone never replace this step.

## Colour

- Use a single light design system across a release: near-white ground, dark ink, low-saturation module colours, perceptual sequential scales, zero-centred diverging scales for signed effects.
- Avoid red-green pairs and rainbow palettes. Check colour-vision accessibility.
- Keep legend and colourbar meaning adjacent to the panel they describe; do not let a colourbar steal width from a neighbour.
- Use Arial/Helvetica-compatible fonts available on the rendering machine; confirm resolution in the actual environment.
