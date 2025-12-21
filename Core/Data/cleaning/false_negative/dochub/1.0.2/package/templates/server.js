const http = require('http');
const fs = require('fs');
const path = require('path');
const hljs = require('highlight.js');
const socketio = require('socket.io');

let htmlContent = ''; // Variable to store HTML content

// Function to convert Markdown to HTML
function convertMarkdownToHtml(markdownContent, filePath) {
  // Regular expression to match Markdown code blocks
  const codeBlockRegex = /```(\w+)\n([\s\S]*?)```/g;

  // Basic conversion: Replace Markdown syntax with HTML equivalents
  let htmlContent = markdownContent
    // Code blocks
    .replace(codeBlockRegex, (match, language, code) => {
      const validLanguage = language || 'plaintext'; // Default to plaintext if no language specified
      const highlightedCode = hljs.highlight(code, { language: validLanguage }).value;
      // Count the number of lines in the code content
      const lines = code.split('\n').length;
      return `<pre class="bg-gray-800 text-white p-4 rounded-md mb-4 code-block" style="height: ${lines * 1.5}rem;"><code class="language-${validLanguage}" data-lines="${lines}">${highlightedCode}</code></pre>`;
    })
    // Inline code
    .replace(/`([^`]*)`/g, '<code class="bg-gray-800 text-white rounded px-1">$1</code>')
    // Headers, emphasis, lists, links
    .replace(/^# (.*)$/gm, '<h1 class="text-4xl font-bold mt-8 mb-4">$1</h1>')
    .replace(/^## (.*)$/gm, '<h2 class="text-3xl font-bold mt-6 mb-3">$1</h2>')
    .replace(/^### (.*)$/gm, '<h3 class="text-2xl font-bold mt-4 mb-2">$1</h3>')
    .replace(/^#### (.*)$/gm, '<h4 class="text-xl font-bold mt-3 mb-2">$1</h4>')
    .replace(/^##### (.*)$/gm, '<h5 class="text-lg font-bold mt-3 mb-2">$1</h5>')
    .replace(/^###### (.*)$/gm, '<h6 class="text-base font-bold mt-2 mb-2">$1</h6>')
    .replace(/\*\*(.*)\*\*/g, '<strong class="font-bold">$1</strong>')
    .replace(/\*(.*)\*/g, '<em class="italic">$1</em>')
    .replace(/^\s*-\s(.*)$/gm, '<li class="list-disc ml-4">$1</li>')
    .replace(/^\s*\d\.\s(.*)$/gm, '<li class="list-decimal ml-4">$1</li>')
    .replace(/<li>(.*)<\/li>/g, '<ul class="list-inside list-disc mb-4">$1</ul>')
    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="text-blue-500 hover:underline">$1</a>')
    // Paragraphs and Line breaks
    .replace(/\n\n/gm, '</p><p class="mb-6">')  // Replace double newline with closing and opening paragraph tags
    .replace(/^\s*$/gm, '<p class="mb-6">')      // Replace empty lines with opening paragraph tag
    .replace(/^/gm, '')                         // Remove the beginning of each line
    .replace(/$/gm, '');                        // Remove the end of each line

  // Generate sidebar based on file structure
  const sidebar = generateSidebar(path.join(__dirname, 'markdown'));

  // Return the entire HTML structure
  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Markdown to HTML</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/highlight.js/styles/vs2015.css" rel="stylesheet">
  <style>
    /* Dark mode theme */
    body {
      background-color: #1a202c;
      color: #e2e8f0;
    }
    .bg-gray-200 {
      background-color: #2d3748;
    }
    .text-blue-500 {
      color: #90cdf4;
    }
    .hover\:underline:hover {
      text-decoration: underline;
    }
    /* Adjust sidebar height */
    .sidebar {
      min-height: 100vh; /* Ensure sidebar stretches to full viewport height */
      display: flex;
      flex-direction: column;
      align-items: flex-start; /* Align items to the start (left) */
      justify-content: flex-start; /* Start content from the top */
      padding: 20px;
    }
    .code-block {
      color: #e2e8f0; /* Match the body text color */
      padding: 1rem;
      margin-bottom: 1rem;
      border-radius: 0.5rem;
      overflow: hidden; /* Prevents scroll bars */
      white-space: pre-wrap; /* Preserves white space */
    }
    .search-bar {
      width: 100%;
      padding: 0.5rem;
      margin-bottom: 1rem;
      background-color: #4a5568;
      color: #e2e8f0;
      border: none;
      border-radius: 0.25rem;
      outline: none;
    }
    .search-bar:focus {
      background-color: #2d3748;
    }
  </style>
</head>
<body class="flex bg-gray-100">
  <aside class="w-1/5 bg-gray-800 p-4 sidebar">
    <h1 class="text-xl font-bold mb-4">Sidebar</h1>
    <input type="text" id="search-input" class="search-bar" placeholder="Search...">
    <ul id="sidebar-list" class="space-y-2">
      ${sidebar}
    </ul>
  </aside>
  <main id="main-content" class="w-4/5 p-4 bg-gray-200">
    ${htmlContent}
  </main>
  <script src="https://cdn.socket.io/4.3.1/socket.io.min.js"></script>
 <script>
  document.addEventListener('DOMContentLoaded', function() {
    const socket = io(); // Declare socket variable here

    socket.on('fileChange', function() {
      fetchCurrentPageContent();
    });

    const codeBlocks = document.querySelectorAll('.code-block');
    codeBlocks.forEach(block => {
      const code = block.querySelector('code');
      const lines = parseInt(code.getAttribute('data-lines'));
      const lineHeight = parseInt(getComputedStyle(code).lineHeight);
      block.style.height = (lines * lineHeight) + 'px'; // Set height using proper concatenation
    });

    // Fetch the sidebar list and handle search input
    const sidebarList = document.getElementById('sidebar-list');
    if (sidebarList) {
      const sidebarItems = sidebarList.getElementsByTagName('li');

      document.getElementById('search-input').addEventListener('input', function() {
        const searchValue = this.value.trim().toLowerCase();

        Array.from(sidebarItems).forEach(item => {
          const link = item.querySelector('a');
          if (link) {
            const textContent = link.textContent.trim().toLowerCase();

            if (textContent.includes(searchValue)) {
              item.style.display = 'block';
            } else {
              item.style.display = 'none';
            }
          }
        });
      });
    } else {
      console.error('Sidebar list element not found.');
    }
  });

  function fetchCurrentPageContent() {
    // Fetch the current page's HTML content
    fetch(window.location.href)
      .then(response => response.text())
      .then(html => {
        // Replace the entire HTML document with the fetched content
        document.open();
        document.write(html);
        document.close();
      })
      .catch(error => {
        console.error('Error fetching current page content:', error);
      });
  }
</script>

</body>
</html>
  `;
}

// Function to generate sidebar links based on directory structure
function generateSidebar(rootDir) {
  const generateLinks = (dir, baseUrl, depth = 0) => {
    let links = '';
    const items = fs.readdirSync(dir);

    items.forEach(item => {
      const itemPath = path.join(dir, item);
      const relativePath = path.relative(rootDir, itemPath);
      const urlPath = baseUrl + '/' + relativePath.replace(/\\/g, '/').replace('.md', '');

      if (fs.statSync(itemPath).isDirectory()) {
        // If directory, recursively generate nested list with increased depth
        links += `<li class="font-bold ml-${depth * 2}">${item}</li>\n`;
        links += `<ul class="ml-4 space-y-2">${generateLinks(itemPath, baseUrl, depth + 1)}</ul>\n`;
      } else if (item.endsWith('.md')) {
        // If Markdown file, generate list item with link
        links += `<li class="ml-${depth * 2}"><a href="${urlPath}" class="text-blue-500 hover:underline">${item.replace('.md', '')}</a></li>\n`;
      }
    });

    return links;
  };

  // Start generating sidebar from root directory
  return generateLinks(rootDir, '');
}

// Create HTTP server
const server = http.createServer((req, res) => {
  let filePath = '.' + req.url;

  if (filePath === './' || filePath === './index.html') {
    filePath = './README.md'; // Default to README.md for root URL
  } else if (!path.extname(filePath)) {
    // Append '.md' for paths that do not have an extension
    filePath += '.md';
  }

  filePath = path.join(__dirname, 'markdown', filePath.replace(/^\//, ''));

  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 Not Found</h1><p>The requested URL was not found on this server.</p>');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/html' });
        res.end('<h1>500 Internal Server Error</h1><p>Sorry, something went wrong.</p>');
      }
    } else {
      let contentType = 'text/html';

      if (filePath.endsWith('.md')) {
        // Convert Markdown to HTML
        const markdownContent = data.toString();
        htmlContent = convertMarkdownToHtml(markdownContent, filePath);

        // Serve HTML with proper Tailwind CSS and sidebar
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(htmlContent);
      } else {
        // Serve other file types directly (e.g., CSS files)
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(data);
      }
    }
  });
});

// Attach Socket.IO to the HTTP server
const io = socketio(server);

// Watch changes in the Markdown directory
const markdownDir = path.join(__dirname, 'markdown');
if (fs.existsSync(markdownDir)) {
  fs.watch(markdownDir, { recursive: true }, (eventType, filename) => {
    console.log(`File ${filename} ${eventType}`);
    io.emit('fileChange'); // Emit event to clients when file changes
  });
} else {
  console.error('Markdown directory does not exist.');
}

const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});