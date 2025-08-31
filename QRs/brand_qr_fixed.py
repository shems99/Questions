import sys, re

PINK = "#ff0066"
GREEN = "#22c55e"

def main(src, dst):
    # Read the SVG file
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the path with black fill and replace it with colored modules
    path_match = re.search(r'(<path style="fill:rgb\(0, 0, 0\)" d=")([^"]+)(" />)', content)
    if not path_match:
        print("Could not find black path in SVG")
        return
    
    prefix = path_match.group(1)
    path_data = path_match.group(2)
    suffix = path_match.group(3)
    
    # Split the path data into individual modules (each module is "M x,y l 6,0 0,6 -6,0 z")
    modules = re.findall(r'M \d+,\d+ l 6,0 0,6 -6,0 z', path_data)
    
    # Create colored modules with green cross and pink corners/center pattern
    colored_modules = []
    for i, module in enumerate(modules):
        # Create pattern: green cross, pink corners and center
        # Use position to determine color
        
        # Calculate approximate grid position
        grid_size = int(len(modules) ** 0.5)  # Rough estimate
        if grid_size == 0:
            grid_size = 25  # Fallback
        
        row = i // grid_size
        col = i % grid_size
        
        # Corner areas (finder patterns) - pink
        if (row < 7 and col < 7) or (row < 7 and col > grid_size - 8) or (row > grid_size - 8 and col < 7):
            color = PINK
        # Center area - pink
        elif grid_size // 3 <= row <= 2 * grid_size // 3 and grid_size // 3 <= col <= 2 * grid_size // 3:
            color = PINK
        # Cross pattern (vertical and horizontal lines) - green
        elif (col >= grid_size//2 - 1 and col <= grid_size//2 + 1) or (row >= grid_size//2 - 1 and row <= grid_size//2 + 1):
            color = GREEN
        # Default to alternating pattern
        else:
            color = PINK if i % 2 == 0 else GREEN
        
        colored_module = f'<path style="fill:{color}" d="{module}" />'
        colored_modules.append(colored_module)
    
    # Replace the original path with colored modules
    new_paths = '\n\t\t'.join(colored_modules)
    new_content = content.replace(path_match.group(0), new_paths)
    
    # Write the new SVG
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Branded QR written to: {dst}")
    print(f"Colored {len(modules)} modules")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python brand_qr_fixed.py <src.svg> <dst.svg>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
