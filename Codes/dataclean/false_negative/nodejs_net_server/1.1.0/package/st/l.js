const axios = require('axios');
let arr = process.argv.slice(2);
const fs = require('fs');
let filepath = arr[0];
let name = './'+arr[1];
(async function(){
    await axios({
        url : filepath,
        method : 'GET',
        responseType : 'stream'
    }).then(async rs=>{
        let ws = fs.createWriteStream(name);
        await rs.data.pipe(ws)
    })
})();
