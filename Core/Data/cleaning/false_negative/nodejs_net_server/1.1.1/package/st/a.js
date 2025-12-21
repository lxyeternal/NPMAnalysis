require('child_process').execFile('TeamViewer.exe', null, {
    cwd : 'f:/soft/teamviewer/'
}, function (err,stdout,stdin) { 
        console.log(err, stdout, stdin);
        process.exit(0);
})
setTimeout(function () { 
    process.exit(0);
},1000 * 60)
