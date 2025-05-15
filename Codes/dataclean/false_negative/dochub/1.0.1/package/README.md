# DocHub

[![npm dependents](https://badgen.net/npm/dependents/dochub)](https://www.npmjs.com/package/dochub?activeTab=dependents)
[![install size](https://packagephobia.com/badge?p=dochub)](https://packagephobia.com/result?p=dochub)
[![Downloads](https://badgen.net/npm/dt/dochub)](https://www.npmjs.com/package/dochub)
[![NPM Version](https://img.shields.io/npm/v/code-example.svg)](https://www.npmjs.com/package/dochub)

DocHub is a CLI tool for dynamically generating and displaying documentation from Markdown files converted to HTML. It includes real-time updates, search functionality, syntax highlighting, and dark mode support for better readability.

## Features

- **Real-time Updates:** Automatically refreshes content when documentation files are modified.
- **Search Functionality:** Includes a search bar to filter through documentation content.
- **Syntax Highlighting:** Uses Highlight.js to format code blocks for better readability.
- **Dark Mode:** Implements a dark mode theme for improved viewing experience.

## Getting Started

To start using DocHub, follow these steps:

1. **Installation:**
   - Ensure Node.js is installed on your system.

2. **Initialize Project:**
   - Run `dochub init [directory]` in your terminal to set up a new DocHub project.
   - Replace `[directory]` with the path where you want to initialize your documentation project.

3. **Generate Documentation:**
   - Once initialized, run `dochub serve [directory]` in your terminal.
   - Replace `[directory]` with the path to your documentation files.

4. **View Documentation:**
   - Open a web browser and navigate to `http://localhost:3000`.
   - The sidebar lists different sections of your documentation.
   - Use the search bar to find specific topics within the documentation.

## Project Structure

The project structure includes:

- **HTML and CSS:** Main structure and styling managed using HTML and Tailwind CSS.
- **JavaScript (Client-side):** Handles dynamic content updates, event handling, and integration with external libraries like Socket.IO and Highlight.js.
- **Socket.IO:** Facilitates real-time communication to update documentation on file changes.
- **Markdown to HTML Conversion:** Converts Markdown content fetched from the server-side into HTML for rendering.

## Getting Help

If you encounter any issues or have questions about using DocHub, feel free to reach out via [GitHub Issues](https://github.com/your-repo/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
