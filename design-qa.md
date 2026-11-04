# Design QA

## Evidence

- Source visual truth: `/Users/skyfu/Desktop/截圖 2026-11-04 下午3.43.15.png`
- Source pixels: 377 × 168 at 1× density
- Implementation capture: CUA browser capture of `http://127.0.0.1:5174/` (desktop dashboard and login; mobile dashboard and login)
- Desktop viewport: 1280 × 720 at 1× density
- Mobile viewport: 390 × 844 at 1× density
- State: signed-out login screen; signed-in dashboard; incorrect-password error; responsive mobile layout

## Full-view comparison

- The supplied society runner logo is used as a real raster asset in the login screen, application brand area, and lower-left copyright block.
- The lower-left block follows the reference hierarchy: square logo, vertical divider, copyright name, `ALL RIGHTS RESERVED.`, and update date.
- The authenticated interface retains the existing accounting information architecture and data.

## Focused region comparison

- Compared the lower-left sidebar footer against the reference crop because this is the fidelity-critical region.
- Typography is intentionally reduced to fit the existing 252 px sidebar while preserving the source hierarchy and wording.
- The runner mark is cropped from the supplied official wordmark asset; no CSS-drawn or placeholder logo is used.

## Required fidelity surfaces

- Fonts and typography: Traditional Chinese serif/sans hierarchy is consistent; copyright copy remains legible at sidebar size.
- Spacing and layout rhythm: logo, divider, three copyright lines, and storage note remain separated and aligned.
- Colors and visual tokens: dark green background, white primary copy, muted green secondary copy, and gold divider match the existing system palette and reference.
- Image quality and asset fidelity: supplied high-resolution PNG is rendered directly and remains sharp at desktop and mobile sizes.
- Copy and content: association name uses `臺灣`; year, rights statement, and November 2026 update date match the reference.

## Interaction and responsive checks

- Incorrect credentials show a clear error and remain on the login screen.
- `admin` / `0000` opens the dashboard; logout returns to the login screen.
- Session refresh preserves the signed-in state until logout or tab session end.
- Desktop and 390 × 844 mobile layouts were visually inspected.
- A mobile toolbar overflow found in the first pass was fixed by stacking the filter and update timestamp; the second capture showed no overlap.

## Findings

- P0: none
- P1: none
- P2: none after the mobile toolbar fix
- P3: the narrow sidebar requires smaller copyright typography than the wider reference crop; accepted as a responsive constraint.

## Comparison history

1. First mobile dashboard capture: update timestamp overlapped the right edge (P2).
2. Fix: mobile toolbar now stacks vertically and the project filter fills the available width.
3. Post-fix capture: timestamp and filter are fully visible without overlap.

final result: passed
