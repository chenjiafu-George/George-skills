# CNKI Journal Normalization

Use this note when a Chinese journal must be searched through CNKI or a CNKI-oriented fallback.

## Why it matters

Chinese journal short names are not always the best CNKI search strings.
Some journals are indexed under:

- a short title
- a university-journal title plus section suffix
- a broader source family name

That means batch search should normalize the target journal name before retrieval and then filter locally after retrieval.

## Recommended query aliases

```json
{
  "文艺研究": "文艺研究",
  "新美术": "新美术",
  "美术研究": "美术研究",
  "美术与设计": "南京艺术学院学报",
  "世界美术": "世界美术",
  "装饰": "装饰杂志"
}
```

## Recommended accepted source names

```json
{
  "文艺研究": ["文艺研究"],
  "新美术": ["新美术"],
  "美术研究": ["美术研究"],
  "美术与设计": ["南京艺术学院学报(美术与设计版)", "南京艺术学院学报"],
  "世界美术": ["世界美术"],
  "装饰": ["装饰"]
}
```

## Recommended local filter

```python
def keep_record(record, target_journal, accepted_sources, start_year, end_year):
    source_ok = record.get("source") in accepted_sources[target_journal]
    try:
        year = int((record.get("date") or "")[:4])
    except Exception:
        return False
    year_ok = start_year <= year <= end_year
    return source_ok and year_ok
```

## Practical rule

- Normalize first.
- Retrieve second.
- Filter by source and year locally.
- Only then write the records into the review.
