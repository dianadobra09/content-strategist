# Visuals

A visual must help the reader see the point, understand the work or connect with the author's experience.
Choose it with the post, not as decoration after the text is finished.
Photos are one option. Technical diagrams, charts and code excerpts can be created from actual source material.

## Choose the form

- **Personal moment:** the author's own photo from the event, workday or routine. Keep the context true to the story.
- **Something happened:** a real screenshot, test output, diff or before-and-after artifact. Crop and annotate the relevant detail.
- **How it works:** a simple flow, sequence or architecture diagram based on code, notes or verified documentation (`examples/outputs/visuals/content-workflow/`).
- **A choice or comparison:** actual inputs, common criteria and outputs shown together. Include the limitation or failed case.
- **A measured result:** a chart from real data, with units, sample size, period and source. Do not invent missing values.
- **A primary source:** excerpts cropped unchanged from the document, with the quoted lines highlighted (`examples/outputs/visuals/character-ai-bankruptcy/`).
- **A useful process:** a short PDF or carousel with one step per page, combining artifacts and explanations. Use only as many pages as needed.
- **A change in motion:** a short looping animation of a flow or diagram when motion shows the change better than a still: input becoming output, steps completing, a before and after. Use `motion-graphics-builder`; `examples/outputs/visuals/design-team-figma-to-react/` shows a finished one.
- **An interaction:** a short recording of a real run, with readable captions and the relevant result. Do not hide failures with misleading edits.
- **No visual:** use text alone when an attachment adds no evidence, explanation or meaningful context.

A relevant checklist or resource can accompany the post. Avoid generic quote cards, stock photos and decorative AI imagery.
Do not manufacture screenshots, analytics, customer messages or scenes. A screenshot is evidence of what it shows, not proof of every claim.
Product visuals follow `strategy/product.md`.

## What the author can supply

Any one of these can start a technical visual:

- A screenshot or the file, code diff, test output or trace that contains the relevant detail.
- A few notes describing the actual steps, including where a person intervenes.
- A CSV or small results table with the test conditions and dates.
- A recording of one real task, from input to output.
- A primary-source document, diagram or explanation they want to discuss, with its link.

Ask only for missing facts or files. Do not require a photo of the author for a technical post.
A sketch can explain the work before a finished screenshot exists. Label proposals as proposed and teaching examples as illustrative.
Never present a teaching example as the author's observed output or benchmark.

## Create the visual

1. Read the post and source material. State the single point the visual will show.
2. Choose the simplest fitting form. For a diagram, name the components, connections and any important boundary or human review step.
3. Create an editable source. Use SVG or HTML for diagrams and code, plotting code for charts, a build script for document excerpts, or HTML slides for carousels.
4. Use the available matching tools. Use document or presentation workflows for PDFs or slides; use plotting tools for measured data.
5. Export PNG for static visuals, PDF for document posts and carousels, video for recordings, or MP4 and GIF for animated diagrams (`motion-graphics-builder`).
6. Render and inspect the export at phone size. Check text, clipping, arrows, labels, contrast, factual meaning and privacy.
7. Save source and export in `outputs/visuals/<post-slug>/`. Link both in the post's Visual section and write alt text.

For original screenshots and photos, keep the source intact. Make a separate cropped or redacted copy.
Annotations can clarify a real artifact but must not alter its result. Retain important error messages and qualifications.
If creation tools or source material are unavailable, save a precise capture brief. Do not claim the asset is finished.
When the author asks for a finished visual and the inputs are present, create it rather than returning only a suggestion.

## Keep the design consistent

Carousels: 1080 x 1350 pages styled by `outputs/visuals/carousel-kit/kit.css`, saved in `outputs/visuals/<post-slug>/carousel/`. `sh outputs/visuals/carousel-kit/render.sh <folder> <name>` renders the `slide-N.html` pages and the PDF (macOS with Google Chrome); `carousel-kit/example/` shows the pattern. Two pages is a good default: a big question as the title with the key words highlighted, the answer or number, and a short source line.

Carousels and animations share one set of brand tokens: by default BlinkWrite's brand guidelines (Onest, Geist Mono, ink and a lime accent), in `carousel-kit/kit.css` and the `motion-graphics-builder` template. Replace them with the author's brand.

Use a plain background, readable type, generous spacing and a restrained accent color.
Use the same treatment across diagrams while keeping the content specific. The author's preferences can refine that treatment over time.
A square or 4:5 portrait is a practical starting canvas, not a reach promise. Use landscape when the diagram needs it.
For a 1080-pixel-wide image, start near 32 pixels for body labels and inspect the reduced result on a phone-sized preview.
Split a crowded diagram or show fewer code lines instead of shrinking the text.
Use plain labels and direct connections. Do not add logos, icons, 3D effects or a headline that merely repeats the hook. Other companies' logos need their permission.
Diagram labels and step numbers can be structured even when the post body uses connected prose.

## Before delivery

Check every claim against the source. Identify simplified or omitted steps when they affect the explanation.
For charts, label axes and units, give the date or period, and distinguish measured values from estimates.
Hide personal data, keys, tokens, internal URLs and unreleased product details. Check titles, filenames and browser tabs too.
Use others' photos, messages or artwork only when permission or reuse terms allow it. Preserve source attribution.
Write alt text that explains the important relationship or result, not every decorative detail.
Keep the opening, visual and body consistent. Never claim a diagram, PDF or photo guarantees engagement.
