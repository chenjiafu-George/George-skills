---
name: journal-figure-router
description: >-
  Trigger this skill whenever the user asks in Chinese or English to draw, revise,
  audit, or polish figures according to journal formatting or manuscript submission
  conventions, including requests such as 按照期刊的格式画图、按投稿格式作图、按论文格式出图、
  期刊格式润色图表、论文图排版、投稿图导出、publication-format figure, journal-format plot,
  or manuscript-format chart. Route the task to the installed global skill
  `scientific-figure-making` and follow that workflow.
---

# Journal Figure Router

This is a lightweight trigger bridge for journal-figure requests.

When this skill is activated:

1. Immediately open and follow the installed global skill `scientific-figure-making`.
2. Treat `scientific-figure-making` as the authoritative workflow for matplotlib-based
   plotting, layout, export, and style parity with figures4papers.
3. Prefer this route for requests centered on journal formatting, manuscript formatting,
   print/vector export, or repo-style publication plots.
4. If the user instead asks for top-tier journal or conference style such as Nature,
   Science, Cell, NeurIPS, ICML, ICLR, or "顶刊顶会风格", route to `nature-figure`.
