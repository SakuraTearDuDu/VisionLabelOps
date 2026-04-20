# GitHub Showcase Checklist

This checklist captures the remaining GitHub web actions for a polished `v0.1.1` release. It separates what is already prepared inside the repository from what still requires GitHub settings or release-page work.

## Already prepared in the repository

- `README.md` has a showcase-oriented front page with:
  - tagline
  - bilingual language switch
  - badges
  - hero banner
  - highlights
  - support tables
  - results preview
- `README.zh-CN.md` provides a full Simplified Chinese entry.
- `docs/quickstart.zh-CN.md` exists and mirrors the English quickstart scope.
- Release and showcase assets are ready under `docs/assets/`:
  - `readme-hero.svg`
  - `readme-preview.jpg`
  - `readme-cli-preview.png`
  - `social-preview.png`
- `docs/release_notes_v0.1.1.md` is ready to use as the GitHub Release draft source.

## P0 - Do now

### Confirm repository description

Recommended description:

> A lightweight toolkit for computer vision dataset auditing, conversion, statistics, splitting, preview, and report generation.

Current repository description already matches this wording. Reconfirm it after publishing `v0.1.1`.

### Set repository topics

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

### Upload the social preview image

Recommended asset:

- `docs/assets/social-preview.png`

This is the highest-value GitHub web setting still missing from the repository itself.

### Create the `v0.1.1` release

Recommended title:

- `VisionLabelOps v0.1.1`

Recommended release subtitle:

- `repository hardening, showcase polish, and Chinese documentation`

Use `docs/release_notes_v0.1.1.md` as the base text for the GitHub release draft.

## P1 - This week

### Re-check the default branch homepage

After the release is published, manually verify on GitHub that:

- `README.md` renders the hero banner correctly
- `README.zh-CN.md` renders correctly
- language switch links work both ways
- all image paths render correctly from relative links
- `docs/quickstart.zh-CN.md` is reachable from the Chinese README

### Release page media choice

Recommended release-page image strategy:

- use `social-preview.png` as the share card
- include `readme-preview.jpg` or `readme-cli-preview.png` inside the release body only if you want one inline visual example

### Pinning strategy

If VisionLabelOps is one of your first public repositories, pin it on your GitHub profile after publishing `v0.1.1`.

## P2 - Later

### Homepage / website link

If you later publish standalone documentation or a project site, add it as the repository homepage link. For now, leaving the repository without a separate website link is acceptable.

### Release-page iteration

After `v0.1.1`, keep future release pages short and consistent with the README front page instead of rewriting the project positioning every time.

## Connector limitation note

In the current session, the available GitHub connector flow can read repository and PR state, but it does not expose a direct write path for topics, social preview settings, or GitHub Release draft creation. Those remaining actions must be completed manually in the GitHub web UI.
