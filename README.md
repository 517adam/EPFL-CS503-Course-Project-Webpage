# SK-Adapter++ Course Project Webpage

This repository contains the GitHub Pages webpage for the CS-503 course project:

**SK-Adapter++: Enhancing Skeleton-Guided Native 3D Generation via Modality Compatible SK-Adapter**

The page uses the structure and styling conventions of the `sk-adapter/sk-adapter.github.io` project page template. Open `index.html` directly or host the folder with any static file server.

## Included materials

- `index.html`: main project webpage
- `static/images/`: rendered figures used by the webpage
- `static/pdf/`: proposal, progress report, progress slides, and final evaluation slides
- `static/css/` and `static/js/`: local template assets copied from the SK-Adapter project page
- `static/models/`: generated 3D results for the interactive skeleton/mesh viewers

The interactive examples load real generated assets. Each result lives in its own
folder under `static/models/<item_id>/` and contains a textured mesh
(`<item_id>_geometry.obj` + `material.mtl` + `material_0.png`), pre-rendered
turntable views (`render/`, `render_gs/`), and the original `<item_id>_data.pt`
(prompt + skeleton joints). In `index.html`, each `.example-pair` points at the
mesh via `data-base`/`data-obj`/`data-mtl`, and renders the skeleton from the
joint coordinates embedded in the `data-skeleton` attribute (joints are shown as
points, since the source data does not include bone connectivity).

To add another result, drop its folder under `static/models/` and add a matching
`.example-pair` block.

The top comparison strip still uses placeholders until synchronized skeleton/result videos are available.

## Local preview

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.
