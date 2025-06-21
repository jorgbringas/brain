from flask import Flask, render_template, send_from_directory, abort
import os
from pathlib import Path
import markdown

app = Flask(__name__)

# Set the path to the brain directory
BRAIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain')

def get_markdown_files(directory):
    """Recursively get all markdown files in the given directory."""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                rel_path = os.path.relpath(os.path.join(root, file), directory)
                md_files.append({
                    'path': rel_path,
                    'name': os.path.splitext(rel_path)[0].replace('_', ' ').title()
                })
    return sorted(md_files, key=lambda x: x['name'])

@app.route('/')
def index():
    """Render the main page with a list of markdown files."""
    md_files = get_markdown_files(BRAIN_DIR)
    return render_template('index.html', files=md_files)

@app.route('/view/<path:filename>')
def view_file(filename):
    """Render a markdown file as HTML."""
    filepath = os.path.join(BRAIN_DIR, filename)
    
    # Security check to prevent directory traversal
    if not os.path.abspath(filepath).startswith(os.path.abspath(BRAIN_DIR)):
        abort(403)
    
    if not os.path.exists(filepath):
        abort(404)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
    
    return render_template('view.html', 
                         content=html_content, 
                         title=os.path.splitext(os.path.basename(filename))[0].replace('_', ' ').title())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
