import requests
from bs4 import BeautifulSoup
import sys

def print_character_grid(doc_url: str) -> None:

    try:
        # Fetch and parse the document
        response = requests.get(doc_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table
        table = soup.find('table')
        if not table:
            print("No table found in the document.", file=sys.stderr)
            return
            
        # Find all rows in the table
        rows = table.find_all('tr')
        if len(rows) <= 1:  # Need at least header row and one data row
            print("Table has insufficient rows.", file=sys.stderr)
            return
            
        # Skip header row, process data rows
        points = []
        max_x = max_y = 0
        
        # Collect all points with their characters
        for row in rows[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            if len(cells) != 3:
                continue
                
            try:
                x = int(cells[0].get_text().strip())
                char = cells[1].get_text().strip()  # Get the actual character
                y = int(cells[2].get_text().strip())
                points.append((x, y, char))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            except (ValueError, IndexError):
                continue
        
        if not points:
            print("No valid character positions found in the document.", file=sys.stderr)
            return
        
        # Create and fill the grid
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        
        # Place each character at its specified position
        for x, y, char in points:
            grid[y][x] = char
        
        # Print each row of the grid in reverse order
        for row in reversed(grid):
            print(''.join(row), flush=True)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    # Example usage with the provided URL
    example_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    print_character_grid(example_url) 