# GitHub Showcase Checklist

This checklist records which repository showcase items are already prepared in-repo and which ones still need GitHub web settings or post-merge actions.

## Already prepared in the repository

- `README.md` has a showcase-oriented front page with:
  - tagline
  - language switch
  - badges
  - hero banner
  - highlights
  - support table
  - results preview
- `README.zh-CN.md` provides a full Simplified Chinese counterpart with the same core information.
- `docs/quickstart.zh-CN.md` exists and is linked from the Chinese README.
- Showcase assets are ready under `docs/assets/`:
  - `readme-hero.svg`
  - `readme-preview.jpg`
  - `readme-cli-preview.png`
  - `social-preview.png`

## Repository metadata status

### Description

Current repository description is already aligned with the project:

> A lightweight toolkit for computer vision dataset auditing, conversion, statistics, splitting, preview, and report generation.

No immediate change is required unless you want a shorter homepage description after the next release.

### Topics

Recommended topics:

- `computer-vision`
- `dataset`
- `yolo`
- `coco`
- `labelme`
- `data-quality`
- `annotation`
- `python`
- `cli`

These still need to be applied in the GitHub repository settings or on the repo homepage edit panel if they are not already present.

## Social preview

Recommended asset:

- `docs/assets/social-preview.png`

Suggested usage:

- Upload it as the GitHub repository social preview image after the README showcase PR is merged.
- Reuse the same image in release notes or social cards if needed.

## README rendering checks

After the PR is pushed, confirm on the GitHub branch page that:

- `README.md` renders the hero banner correctly
- `README.zh-CN.md` renders correctly
- the language switch links work both ways
- all image paths render from relative links
- `docs/quickstart.zh-CN.md` is reachable from the Chinese README

## Release page presentation suggestions

For the next release page:

- use the same tagline as the README opening
- include one screenshot from `readme-preview.jpg`
- keep the first release paragraph focused on:
  - detection-first scope
  - YOLO / COCO / Labelme support
  - unified CLI + API
  - audit / convert / stats / split / preview / report

## Manual GitHub tasks

The current available connector workflow can create PRs, but it does not expose a direct write path for repository description, topics, or social preview settings in this session. After merge, complete these manually in the GitHub web UI:

1. Confirm repository topics
2. Upload `docs/assets/social-preview.png` as the social preview image
3. Re-check the default branch README rendering once the showcase branch is merged
4. Use the improved README structure as the reference for the next release notes page
