# ZIP Handler Skill

Handle ZIP files: extract, create, inspect, and manage compressed archives.

## Use Cases

- **Extract ZIP files** to specified directory
- **Create ZIP archives** from folders or files
- **Inspect ZIP contents** (list files, sizes, compression ratio)
- **Validate ZIP integrity** (check for corruption)
- **Merge multiple ZIPs** into one
- **Split large files** before zipping
- **Password-protected ZIPs** (create, extract)

## Installation

```bash
# Via clawhub (when published)
clawhub install zip-handler

# Or local development
cp -r zip-handler-skill ~/.openclaw/skills/
```

## Available Functions

### extract_zip(zip_path, extract_to=None, password=None)
Extract a ZIP file to specified directory.

```python
from zip_handler import ZipHandler

handler = ZipHandler()
handler.extract_zip(
    zip_path='data.zip',
    extract_to='./output',
    password=None
)
```

### create_zip(source_path, zip_name, compression='default')
Create a ZIP archive from file or folder.

```python
handler.create_zip(
    source_path='./my_folder',
    zip_name='my_folder.zip',
    compression='best'  # 'fastest', 'default', 'best'
)
```

### inspect_zip(zip_path)
List and analyze ZIP contents.

```python
info = handler.inspect_zip('data.zip')
# Returns: {files: [...], total_size: X, compressed_size: Y, ratio: Z%}
```

### validate_zip(zip_path)
Check ZIP integrity.

```python
is_valid = handler.validate_zip('data.zip')
# Returns: True/False
```

### merge_zips(zip_list, output_name)
Combine multiple ZIPs into one.

```python
handler.merge_zips(
    zip_list=['part1.zip', 'part2.zip', 'part3.zip'],
    output_name='merged.zip'
)
```

## CLI Usage

```bash
# Extract
zip-handler extract data.zip -o ./output

# Create
zip-handler create ./my_folder -n my_folder.zip

# Inspect
zip-handler inspect data.zip

# Validate
zip-handler validate data.zip

# Merge
zip-handler merge part1.zip part2.zip part3.zip -o merged.zip

# With password
zip-handler extract secure.zip -p mypassword -o ./output
```

## Examples

### Example 1: Extract Platform Files
```bash
# Extract the Racha V0 platform ZIP
zip-handler extract racha-v0-platform.zip -o /tmp/platform
```

### Example 2: Backup Project
```bash
# Create backup ZIP of project
zip-handler create ./racha-v0-platform -n backup-2026-03-19.zip
```

### Example 3: Inspect Archive
```bash
# See what's in a ZIP before extracting
zip-handler inspect racha-v0-platform.zip
# Output:
# Files: 42
# Total size: 2.3 MB
# Compressed: 890 KB
# Ratio: 61% compression
```

## Requirements

- Python 3.8+
- zipfile (built-in)
- patool (for encrypted ZIPs)
- py7zr (for 7z support)

## Installation Requirements

```bash
pip install patool py7zr
```

## Status

✅ Ready for use
- Extract: ✓
- Create: ✓
- Inspect: ✓
- Validate: ✓
- Merge: ✓
- Password support: ✓

## Notes

- Supports ZIP, TAR, TAR.GZ, 7Z formats
- Preserves file permissions and timestamps
- Handles large files (tested up to 4GB)
- Thread-safe operations
- Progress callbacks for large operations
