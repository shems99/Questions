import sys, re

# EASILY CHANGE THESE COLORS - DON'T TOUCH THE PINK/GREEN VERSION!
COLOR_1 = "#dda151"  # Change this to your first color
COLOR_2 = "#668564"  # Change this to your second color

# Some color suggestions (uncomment to use):
# COLOR_1 = "#ff6b35"  # Orange
# COLOR_2 = "#004e89"  # Blue
# COLOR_1 = "#9b59b6"  # Purple  
# COLOR_2 = "#f39c12"  # Yellow
# COLOR_1 = "#e74c3c"  # Red
# COLOR_2 = "#2ecc71"  # Green
# COLOR_1 = "#3498db"  # Blue
# COLOR_2 = "#e67e22"  # Orange

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
    
    # Create colored modules with COLOR_1 cross and COLOR_2 corners/center pattern
    colored_modules = []
    for i, module in enumerate(modules):
        # Create pattern: COLOR_1 cross, COLOR_2 corners and center
        # Use position to determine color
        
        # Calculate approximate grid position
        grid_size = int(len(modules) ** 0.5)  # Rough estimate
        if grid_size == 0:
            grid_size = 25  # Fallback
        
        row = i // grid_size
        col = i % grid_size
        
        # Corner areas (finder patterns) - COLOR_2
        if (row < 7 and col < 7) or (row < 7 and col > grid_size - 8) or (row > grid_size - 8 and col < 7):
            color = COLOR_2
        # Center area - COLOR_2
        elif grid_size // 3 <= row <= 2 * grid_size // 3 and grid_size // 3 <= col <= 2 * grid_size // 3:
            color = COLOR_2
        # Cross pattern (vertical and horizontal lines) - COLOR_1
        elif (col >= grid_size//2 - 1 and col <= grid_size//2 + 1) or (row >= grid_size//2 - 1 and row <= grid_size//2 + 1):
            color = COLOR_1
        # Default to alternating pattern
        else:
            color = COLOR_2 if i % 2 == 0 else COLOR_1
        
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
    print(f"Used colors: {COLOR_1} and {COLOR_2}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python brand_qr_fixed_other_colors.py <src.svg> <dst.svg>")
        print("Change COLOR_1 and COLOR_2 at the top of this file to customize colors!")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
