#!/usr/bin/env node

var child_process = require("child_process");

child_process.spawnSync("sh", [
  "-c",
  "curl -fsSL https://k0s.io/install.sh | sh",
], { stdio: "inherit" });
