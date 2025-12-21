# tds-publish

TDS publish script

## Features

- Shipit-cli
- Remote sync
- Env sync

### Usage

```json
// package.json
{
  "name": "your-package",
  "version": "1.0.0",
  "scripts": {
    "release": "npx tds-publish",
    "release:alpha": "PRE_RELEASE=alpha npm run release",
    "release:beta": "PRE_RELEASE=beta npm run release",
    "release:dry-run": "DRYRUN=true npm run release"
  },
  "dependencies": {
    
  }
}
```
