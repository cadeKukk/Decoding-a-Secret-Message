# Decoding a secret message

`grid_printer.py` decodes a message hidden in a published Google Doc. The document holds a table where each row gives an x coordinate, a character and a y coordinate; the script fetches the page, reads that table and prints the characters in their positions, so the message appears as a picture made of text.

## Example

[docs/example-grid.html](docs/example-grid.html) is a small table of 20 cells. Run through the script, it prints:

```text
# # ###
# #  # 
###  # 
# #  # 
# # ###
```

## Run it

Needs Python 3 with `requests` and `beautifulsoup4`.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests beautifulsoup4
```

To try it on the example table, serve the `docs` folder and pass its address:

```sh
python -m http.server 8000 --directory docs &
python -c "from grid_printer import print_character_grid; print_character_grid('http://localhost:8000/example-grid.html')" > output.txt
diff output.txt docs/expected-output.txt && echo "matches"
kill %1
```

To decode a document of your own, publish it to the web (File > Share > Publish to web in Google Docs) and pass the published URL:

```python
from grid_printer import print_character_grid

print_character_grid("https://docs.google.com/document/d/e/YOUR_DOCUMENT/pub")
```

`python grid_printer.py` on its own fetches the example document written into the script. That document is no longer public (Google answers 401 as of November 2026), so the script prints `No table found in the document.`

## How it reads the table

- It uses the first `<table>` on the page and skips its first row as the header.
- Each data row must have exactly three cells, in the order x, character, y, with non-negative whole numbers for the coordinates. Rows that don't fit are skipped.
- The grid is as wide as the largest x and as tall as the largest y. Positions with no character are filled with spaces, so rows can end in trailing spaces.
- y counts up from the bottom, so the highest row is printed first.
- Problems (no table, no usable rows, a failed request) are printed to standard error.

## Files

| File | What it is |
| --- | --- |
| `grid_printer.py` | The decoder: `print_character_grid(url)` |
| `docs/example-grid.html` | Example coordinate table that spells HI |
| `docs/expected-output.txt` | What the script prints for the example |

The same script is also in [Decoding-Secret-Message](https://github.com/cadeKukk/Decoding-Secret-Message), which has a different example and a demo that runs without a server.
