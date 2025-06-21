# Brain Dump Website

A simple, self-contained website to view markdown files in the brain directory.

## Features

- View markdown files in a clean, readable format
- No server setup required (runs on Python's built-in HTTP server)
- Mobile-responsive design
- Syntax highlighting for code blocks

## How to Run

1. Make sure you have Python 3.6 or higher installed
2. Navigate to this directory in your terminal
3. Run the following command:

```bash
python3 serve.py
```

4. The website will automatically open in your default web browser
5. To stop the server, press `Ctrl+C` in the terminal

## Adding Content

Simply add markdown (`.md`) files to this directory, and they will be automatically included in the file list. The files will be displayed in alphabetical order.

## Keyboard Shortcuts

- `Esc` - Clear the current file view
- `←` (Back button) - Go back to the file list

## Notes

- The website is completely client-side and runs entirely in your browser
- No data is sent to any external servers
- All content is loaded directly from local files
