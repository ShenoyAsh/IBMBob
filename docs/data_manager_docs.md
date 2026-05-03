# Module: data_manager.py

A module for managing JSON data files.

## Imports

```python
import json
import os
```

## Classes

## Class: `DataManager`

Handles loading and saving of structured data.

### Methods

#### `__init__(self, base_path: str)`

Initialize with a base directory.

#### `save_data(self, filename: str, data: dict)`

Save a dictionary to a JSON file.

#### `load_data(self, filename: str)`

Load data from a JSON file.


## Functions

### `process_records(records: list[dict], key: str)`

Extract a specific key from a list of records.

**Arguments:**

- `records` (list[dict]): Description needed
- `key` (str): Description needed

**Returns:** `list`

