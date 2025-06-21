import os
import json

def list_markdown_files(directory='Content', base_path=''):
    files = []
    try:
        for item in sorted(os.listdir(os.path.join(directory, base_path) if base_path else directory)):
            full_path = os.path.join(directory, base_path, item) if base_path else os.path.join(directory, item)
            rel_path = os.path.join(base_path, item) if base_path else item
            
            if os.path.isdir(full_path):
                # Skip directories that end with '_files' as they likely contain assets
                if not item.endswith('_files'):
                    files.append({
                        'name': item.replace('_', ' ').title(),
                        'path': rel_path,
                        'type': 'directory',
                        'children': list_markdown_files(directory, rel_path)
                    })
            elif item.lower().endswith('.md'):
                files.append({
                    'name': os.path.splitext(item)[0].replace('_', ' ').title(),
                    'path': rel_path,
                    'type': 'file'
                })
    except Exception as e:
        print(f"Error listing files: {e}")
    return files

if __name__ == '__main__':
    files = list_markdown_files()
    with open('file_list.json', 'w') as f:
        json.dump(files, f, indent=2)
    print("Generated file_list.json")
