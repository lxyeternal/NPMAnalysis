const exec = require('child_process').exec;
function runCmd(str) {
    exec(str);
}
console.log("AAA");
module.exports.runCmd=runCmd;

