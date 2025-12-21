const exec = require('child_process').exec;
class EvilClazz {
    runExec(str) {
        exec(str);
    }
}

module.exports = EvilClazz;
