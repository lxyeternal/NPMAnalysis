#!/usr/bin/env node

const yargs = require('yargs');
const initProject = require('./src/init');
const serveDocs = require('./src/serve');

yargs
  .command({
    command: 'init <directory>',
    describe: 'Initialize a new documentation project',
    builder: (yargs) => {
      yargs.positional('directory', {
        describe: 'Directory name for the documentation project',
        type: 'string',
      });
    },
    handler: initProject,
  })
  .command({
    command: 'serve <directory>',
    describe: 'Serve the documentation site',
    builder: (yargs) => {
      yargs.positional('directory', {
        describe: 'Directory name where documentation files are located',
        type: 'string',
      });
    },
    handler: serveDocs,
  })
  .demandCommand()
  .help()
  .argv;
