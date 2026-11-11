# Paginated read

## State

One session variable, `listings`: tool name, then one record per distinct set of filters.

```python
"listings": {
    "find_employee": {
        "c77c8dbd587a": {"filters": {"name": "garcia"},
                         "next_page": 2, "total": 14},
        "d24ff8089849": {"filters": {"name": "smith"},
                         "next_page": "this is the final page", "total": 3},
    },
    "list_leave_requests": {
        "6cd528438bfc": {"filters": {"status": "pending"},
                         "next_page": 3, "total": 23},
        "888ebfde1d0d": {"filters": {"emp_id": 26, "status": "approved"},
                         "next_page": "this is the final page", "total": 4},
    },
}
```

- A record is the tool's return value minus the entries.
- `next_page` is a page number, or the sentence when no page is left.
- The key is for code. The model reads the records, never the key.
- Each tool keeps only its most recent few records.

## Key

```python
import hashlib, json

def listing_key(filters: dict, page_size: int) -> str:
    applied = {name: value for name, value in filters.items() if value is not None}
    text = json.dumps({"filters": applied, "page_size": page_size},
                      sort_keys=True, separators=(",", ":"))
    return hashlib.blake2b(text.encode(), digest_size=6).hexdigest()
```

- **Input:** filters as the tool applied them. Ids converted to numbers, text trimmed and lower-cased.
- **Unset filters are dropped,** so a new optional argument does not change old keys.
- **Names are sorted,** so argument order does not matter.
- **Page size is included,** so a changed page size starts a fresh listing.
- **`hashlib`, not `hash()`.** The built-in changes on every run, and state outlives the run.

## Lookup

Find the record by key, then compare its `filters` with the incoming ones.
A mismatch is a miss. This covers a collision of the short key.

## Parked: page size getter

- One function returns the read page size. It is the only code that knows the key `read_page_size`.
- The tool and the decorator both call it, so they cannot disagree.
- It applies the cap of 100.
- Open: raise when the key is missing, or fall back to the config value.
