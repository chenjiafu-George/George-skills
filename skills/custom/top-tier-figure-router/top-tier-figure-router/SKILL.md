---
name: top-tier-figure-router
description: >-
  Trigger this skill whenever the user asks in Chinese or English to draw, revise,
  audit, or polish figures in a top-tier journal or conference style, including
  requests such as 顶刊顶会风格画图、Nature风格画图、顶会论文图、按 NeurIPS/ICML/ICLR 风格作图、
  高水平投稿图、多面板顶刊图、top-tier paper figure, high-impact figure, or Nature-style plot.
  Route the task to the installed global skill `nature-figure` and follow that workflow.
---

# Top-Tier Figure Router

This is a lightweight trigger bridge for top-tier paper-figure requests.

When this skill is activated:

1. Immediately open and follow the installed global skill `nature-figure`.
2. Treat `nature-figure` as the authoritative workflow for top-tier journal and conference
   plotting, layout, export, and QA.
3. Preserve its backend gate: if the user has not chosen Python or R, ask `Python or R?`
   and stop.
4. Prefer this route for requests framed as Nature style, top-tier journal style,
   top-tier conference style, or publication figures aimed at elite venues.
