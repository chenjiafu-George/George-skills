# Coverage Test on 2026-05-09

Test basis:

- OpenAlex source lookup by ISSN
- Crossref journal lookup by ISSN

The following journals came from the user's screenshot.

| Journal | ISSN | OpenAlex | Crossref | Note |
|---|---|---:|---:|---|
| Design Studies | 0142-694X | yes | yes | Covered in both systems |
| The Design Journal | 1460-6925 | yes | yes | Covered in both systems |
| Design Issues | 0747-9360 | yes | yes | Covered in both systems |
| Leonardo | 0024-094X | yes | yes | Covered in both systems |
| 文艺研究 | 0257-5876 | no | no | Not found in either system by ISSN |
| 新美术 | 1674-2249 | no | no | Not found in either system by ISSN |
| 美术研究 | 0461-6855 | no | no | Not found in either system by ISSN |
| 美术与设计 | 1008-9675 | no | no | Not found in either system by ISSN |
| 世界美术 | 1000-8683 | no | no | Not found in either system by ISSN |
| 装饰 | 0412-3662 | no | no | Not found in either system by ISSN |

## Interpretation

- The 4 international design and art journals from the screenshot are retrievable with an `OpenAlex + Crossref` stack.
- The 6 Chinese arts journals from the screenshot were not retrievable in these two systems by ISSN on 2026-05-09.
- For those Chinese journals, you should plan a separate fallback path such as CNKI, CSSCI-oriented search, publisher sites, or a custom MCP built on a Chinese metadata source.

## Example verified OpenAlex match

`Design Studies` with ISSN `0142-694X` returned an OpenAlex source record including:

- `display_name = Design Studies`
- `issn_l = 0142-694X`
- `type = journal`
- `last_publication_year = 2026`

## Practical conclusion

If your skill must support both:

- international design / media journals
- Chinese arts journals

then `OpenAlex + Crossref` is a strong base layer, but not a complete solution for Chinese arts-journal coverage.
