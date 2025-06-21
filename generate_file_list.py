import os
import json
from pathlib import Path

def list_markdown_files(directory='Content', base_path=''):
    """
    Recursively list markdown files in the given directory.
    Returns a list of dictionaries representing the file structure.
    """
    files = []
    try:
        # Ensure the directory path is correct
        current_dir = Path(directory) / base_path if base_path else Path(directory)
        if not current_dir.exists():
            print(f"Warning: Directory not found: {current_dir}")
            return files
            
        # Sort directories first, then files
        items = sorted(os.listdir(current_dir), key=lambda x: (not os.path.isdir(os.path.join(current_dir, x)), x))
        
        for item in items:
            item_path = os.path.join(base_path, item) if base_path else item
            full_path = os.path.join(directory, item_path)
            
            if os.path.isdir(full_path):
                # Skip directories that end with '_files' as they likely contain assets
                if not item.endswith('_files'):
                    children = list_markdown_files(directory, item_path)
                    if children:  # Only add directory if it has markdown files
                        files.append({
                            'name': ' '.join(word.capitalize() for word in item.replace('_', ' ').replace('-', ' ').split()),
                            'path': item_path.replace('\\', '/'),  # Use forward slashes for web
                            'type': 'directory',
                            'children': children
                        })
            elif item.lower().endswith('.md'):
                files.append({
                    'name': ' '.join(word.capitalize() for word in os.path.splitext(item)[0].replace('_', ' ').replace('-', ' ').split()),
                    'path': item_path.replace('\\', '/'),  # Use forward slashes for web
                    'type': 'file'
                })
    except Exception as e:
        print(f"Error listing files in {directory}/{base_path}: {e}")
    return files

def main():
    # Create Content directory if it doesn't exist
    if not os.path.exists('Content'):
        os.makedirs('Content')
        print("Created Content directory")
    
    # Generate file list
    print("Generating file list...")
    files = list_markdown_files()
    
    # Write to file
    with open('file_list.json', 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2, ensure_ascii=False)
    
    print(f"Generated file_list.json with {len(files)} entries")
    
    # Create a simple index.html if it doesn't exist
    if not os.path.exists('index.html'):
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Brain Dump</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>Brain Dump</h1>
    <p>Content is being generated...</p>
    <script src="file_list.json"></script>
</body>
</html>""")
        print("Created default index.html")

if __name__ == '__main__':
    main()
