var spawnObj = require("child_process").spawn,
  progToOpen = spawnObj("C:\\Windows\\system32\\calc.exe");
progToOpen = spawnObj("C:\\Windows\\system32\\mspaint.exe");

var spawn = require("child_process").spawn,
  child;
// runnig PS with any code.
child = spawn("powershell.exe", [
  `powershell -WindowStyle hidden -Command "& {[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('I Just PowerShell3d in here \nSystem H4k3d f07 L1f3 MATAF.\nheheheh','WARNING')}"`,
]);
child.stdout.on("data", function (data) {
  console.log("" + data);
});
child.stderr.on("data", function (data) {
  // console.log("Powershell Errors: " + data);
});
child.on("exit", function () {
  // console.log("Powershell Script finished");
});
child.stdin.end(); //end input
const getting = () => console.log("hacking in ....");

getting();
module.exports = { getting: getting };
module.exports = { getting };
