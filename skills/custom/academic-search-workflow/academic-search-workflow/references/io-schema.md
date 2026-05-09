# I/O Schema

This file defines the recommended tool-call order and the data objects the skill should pass between steps.

## Step 1: topic normalization

Input:

```json
{
  "topic_cn": "无人机影像应用与AI媒体视听语言",
  "time_range": {
    "start_year": 2023,
    "end_year": 2026
  },
  "preferred_venues": ["SCI", "SSCI", "A&HCI"],
  "must_include_journals": ["Design Studies", "Leonardo"]
}
```

Output:

```json
{
  "topic_en_core": [
    "drone imagery",
    "UAV imaging",
    "drone cinematography",
    "AI audiovisual language",
    "visual culture",
    "media governance"
  ],
  "query_blocks": [
    "\"drone imagery\" OR \"UAV imaging\"",
    "\"drone cinematography\" OR \"aerial visual storytelling\"",
    "\"AI audiovisual\" OR \"generative media\""
  ],
  "filters": {
    "from_publication_date": "2023-01-01",
    "to_publication_date": "2026-12-31"
  }
}
```

## Step 2: discovery in OpenAlex

Recommended tool order:

1. `openalex_resolve_name`
2. `openalex_search_entities`
3. `openalex_analyze_trends`

Recommended call shape:

```json
{
  "tool": "openalex_search_entities",
  "entity": "works",
  "search": "\"drone cinematography\" OR \"drone imagery\"",
  "filters": {
    "from_publication_date": "2023-01-01",
    "to_publication_date": "2026-12-31",
    "language": ["en"]
  },
  "sort": "cited_by_count:desc",
  "per_page": 20
}
```

Expected normalized output:

```json
{
  "candidate_papers": [
    {
      "title": "Example title",
      "year": 2024,
      "doi": "10.xxxx/xxxxx",
      "openalex_id": "W1234567890",
      "venue": "Journal name",
      "authors": ["Author A", "Author B"],
      "abstract": "Short abstract text",
      "source_issn": ["1234-5678"],
      "citations": 42,
      "landing_page_url": "https://openalex.org/W1234567890"
    }
  ]
}
```

## Step 3: Crossref normalization

Recommended tool order:

1. `get_work_metadata` when DOI is known
2. `search_works_by_query` when DOI is missing
3. `search_journals` when venue or ISSN needs checking

Recommended call shape:

```json
{
  "tool": "get_work_metadata",
  "doi": "10.xxxx/xxxxx"
}
```

Expected normalized output:

```json
{
  "paper": {
    "title": "Example title",
    "doi": "10.xxxx/xxxxx",
    "publisher": "Publisher name",
    "journal": "Journal name",
    "issn": ["1234-5678"],
    "published_year": 2024,
    "authors": [
      {
        "given": "A",
        "family": "Author",
        "orcid": "optional"
      }
    ],
    "type": "journal-article",
    "url": "https://doi.org/10.xxxx/xxxxx"
  }
}
```

## Step 4: coverage test for a named journal

Input:

```json
{
  "journal_title": "Design Studies",
  "issn": "0142-694X"
}
```

OpenAlex success rule:

```json
{
  "display_name": "Design Studies",
  "issn_l": "0142-694X",
  "type": "journal"
}
```

Crossref success rule:

```json
{
  "message": {
    "title": "Design Studies",
    "ISSN": ["0142-694X"]
  }
}
```

Final coverage status object:

```json
{
  "journal_title": "Design Studies",
  "issn": "0142-694X",
  "openalex_found": true,
  "crossref_found": true,
  "coverage_note": "Both systems index this journal."
}
```

## Step 5: review-pack output

Return a single object that the writing stage can consume:

```json
{
  "search_brief": {
    "topic": "drone imagery and AI audiovisual language",
    "time_range": "2023-2026",
    "sources_used": ["OpenAlex", "Crossref"]
  },
  "shortlist": [
    {
      "title": "Example title",
      "year": 2024,
      "venue": "Journal name",
      "doi": "10.xxxx/xxxxx",
      "why_it_matters": "Connects UAV imagery with visual culture analysis."
    }
  ],
  "coverage_notes": [
    "International design journals are mostly covered.",
    "Several Chinese arts journals are not covered in OpenAlex or Crossref."
  ],
  "next_actions": [
    "build comparison table",
    "draft Chinese review",
    "export BibTeX"
  ]
}
```

## Step 6: CNKI journal normalization and local filtering

Use this step when:

- the target journal is Chinese
- OpenAlex and Crossref do not cover the journal
- CNKI or a CNKI-oriented fallback is being used

Recommended normalized input:

```json
{
  "target_journal": "美术与设计",
  "time_range": {
    "start_year": 2021,
    "end_year": 2025
  },
  "journal_alias_map": {
    "文艺研究": ["文艺研究"],
    "新美术": ["新美术"],
    "美术研究": ["美术研究"],
    "美术与设计": ["南京艺术学院学报(美术与设计版)", "南京艺术学院学报"],
    "世界美术": ["世界美术"],
    "装饰": ["装饰", "装饰杂志"]
  },
  "cnki_search_query": "南京艺术学院学报"
}
```

Local filtering rules:

1. Search with the normalized query or alias rather than the raw short title when needed.
2. Keep only records where `source` equals one of the approved aliases for the target journal.
3. Parse the first four characters of `date` as `year`.
4. Keep only records where `start_year <= year <= end_year`.
5. If CNKI web sorting is noisy, treat local year filtering as authoritative.

Expected normalized output:

```json
{
  "journal": "美术与设计",
  "normalized_aliases": ["南京艺术学院学报(美术与设计版)", "南京艺术学院学报"],
  "filtered_records": [
    {
      "title": "数字化场所营造：“场所”认知框架再定义及应用路径研究",
      "source": "南京艺术学院学报(美术与设计版)",
      "date": "2024-11-15",
      "authors": ["罗曼"],
      "url": "https://kns.cnki.net/..."
    }
  ],
  "filter_note": "Source-matched and year-filtered locally after CNKI retrieval."
}
```
