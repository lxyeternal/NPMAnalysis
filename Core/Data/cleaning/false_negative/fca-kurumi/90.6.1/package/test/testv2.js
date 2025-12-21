var languageFile = require('../Language/index.json');
var data = languageFile.find(i => i.Language == "en");
console.log(data);