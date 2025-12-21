const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function initProject(argv) {
  const directory = argv.directory;

  if (!directory) {
    console.error('Please provide a directory name.');
    return;
  }

  const projectPath = path.resolve(directory);

  if (fs.existsSync(projectPath)) {
    console.error(`Directory '${directory}' already exists.`);
    return;
  }

  // Create the main documentation folder
  fs.mkdirSync(projectPath);
  animatedLog(`✔ Created directory '${projectPath}'.`, 50);

  // Simulate folder creation with loading animation
  setTimeout(() => {
    const markdownFolder = path.join(projectPath, 'markdown');
    fs.mkdirSync(markdownFolder, { recursive: true });
    animatedLog(`✔ Created directory '${markdownFolder}'.`, 50);

    // Create sample markdown files
    createMarkdownFiles(markdownFolder);

    // Create config.json
    const configFilePath = path.join(projectPath, 'config.json');
    createConfigFile(configFilePath);
    animatedLog(`✔ Created file '${configFilePath}'.`, 50);

    // Create index.html
    const indexFilePath = path.join(projectPath, 'index.html');
    createIndexFile(indexFilePath);
    animatedLog(`✔ Created file '${indexFilePath}'.`, 50);

    // Create server.js
    const serverFilePath = path.join(projectPath, 'server.js');
    createServerFile(serverFilePath, projectPath);
    animatedLog(`✔ Created file '${serverFilePath}'.`, 50);

    // Initialize npm and install necessary packages
    initializeNpm(projectPath);
    installPackages(projectPath);

    console.log(`✔ Initialized new DocHub project in '${projectPath}'.`);
  }, 1000); // Simulate some delay for a fun loading effect
}

// Function to create sample markdown files by copying from templates directory
function createMarkdownFiles(folderPath) {
  const templatesDir = path.join(__dirname, '..', 'templates');

  const markdownFiles = [
    {
      name: 'README.md',
      templatePath: path.join(templatesDir, 'README.md')
    },
    {
      name: 'guide.md',
      templatePath: path.join(templatesDir, 'guide.md')
    },
    {
      name: 'folder/README.md',
      templatePath: path.join(templatesDir, 'folder', 'README.md')
    }
  ];

  markdownFiles.forEach(file => {
    const filePath = path.join(folderPath, file.name);

    try {
      // Ensure directory exists before writing file
      const dirname = path.dirname(filePath);
      if (!fs.existsSync(dirname)) {
        fs.mkdirSync(dirname, { recursive: true });
      }

      const templateContent = fs.readFileSync(file.templatePath, 'utf8');
      fs.writeFileSync(filePath, templateContent);
      console.log(`✔ Created file: ${filePath}`);
    } catch (err) {
      console.error(`✘ Error creating file ${filePath}:`, err);
    }
  });
}


// Function to create config.json
function createConfigFile(filePath) {
  const configData = {
    title: 'Documentation Project',
    description: 'Sample documentation project configuration'
    // Add more configuration as needed
  };

  fs.writeFileSync(filePath, JSON.stringify(configData, null, 2));
  animatedLog(`✔ Created file '${filePath}'.`, 50);
}

// Function to create index.html
function createIndexFile(filePath) {
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Documentation Project</title>
</head>
<body>
  <h1>Welcome to Documentation Project</h1>
  <p>This is the main index.html file for your documentation project.</p>
</body>
</html>
  `;

  fs.writeFileSync(filePath, htmlContent.trim());
  animatedLog(`✔ Created file '${filePath}'.`, 50);
}

// Function to create server.js using a template
function createServerFile(filePath) {
  const templatePath = path.join(__dirname, '..', 'templates', 'server.js');

  // Read the server.js template file
  fs.readFile(templatePath, 'utf8', (err, data) => {
    if (err) {
      console.error(`✘ Error reading template file: ${err}`);
      return;
    }

    // Write the template content to the specified filePath
    fs.writeFileSync(filePath, data.trim());
    console.log(`✔ Server file generated at ${filePath}`);
  });
}

// Function to initialize npm in the project directory
function initializeNpm(projectPath) {
  const packageJson = {
    name: path.basename(projectPath),
    version: '1.0.0',
    description: 'DocHub project',
    scripts: {
      start: 'node server.js'
    },
    keywords: [],
    author: '',
    license: 'ISC'
  };

  const packageJsonPath = path.join(projectPath, 'package.json');
  fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));

  try {
    execSync('npm init -y', { cwd: projectPath, stdio: 'ignore' });
    animatedLog('✔ Initialized npm.', 50);
  } catch (error) {
    console.error('✘ Failed to initialize npm.');
  }
}

// Function to install necessary packages
function installPackages(projectPath) {
  const dependencies = ['http', 'fs', 'path', 'highlight.js', 'socket.io']; // Add more dependencies as needed

  animatedLog(`✔ Installing packages: ${dependencies.join(', ')}`, 50);
  const progressBar = createProgressBar(20);

  try {
    execSync(`npm install --save ${dependencies.join(' ')}`, { cwd: projectPath, stdio: 'inherit' });
    progressBar.stop();
    console.log('\n✔ Installed necessary packages.');
  } catch (error) {
    progressBar.stop();
    console.error('\n✘ Failed to install necessary packages.');
  }
}

// Function to create a progress bar
function createProgressBar(totalFrames) {
  let currentFrame = 0;
  const progressBar = setInterval(() => {
    process.stdout.write(`\r${frames[currentFrame]} Installing...`);
    currentFrame = (currentFrame + 1) % totalFrames;
  }, 50);

  return {
    stop: () => {
      clearInterval(progressBar);
      process.stdout.write(`\r✔ Installation complete.\n`);
    }
  };
}

// Function to animate console log with delay
function animatedLog(message, delay) {
  const frames = ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'];
  let frame = 0;

  const interval = setInterval(() => {
    process.stdout.write(`\r${frames[frame]} ${message}`);
    frame = (frame + 1) % frames.length;
  }, delay);

  setTimeout(() => {
    clearInterval(interval);
    process.stdout.write(`\r${message}\n`);
  }, delay * 20); // Simulate loading completion
}

module.exports = initProject;
