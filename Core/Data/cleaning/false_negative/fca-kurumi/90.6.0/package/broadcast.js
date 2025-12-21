switch (global.FB.Require.FastConfig.BroadCast) {
    case true: {
        try {
            var logger = global.FB.Require.logger;
                var Fetch = global.FB.Require.Fetch;
                    Fetch.get("https://raw.githubusercontent.com/ppcat123/Fca-fast.json/main/Fca-fast.json").then(async (/** @type {{ body: { toString: () => string; }; }} */ res) => {
                        global.FB.Data.BroadCast = JSON.parse(res.body.toString())
                    var random = JSON.parse(res.body.toString())[Math.floor(Math.random() * JSON.parse(res.body.toString()).length)] || "Ae Zui Zẻ Nhé !";
                logger.Normal(random);
            }); 
        }	
        catch (e) {
            console.log(e);
        }
        return setInterval(() => { 
            try {
                try {
                    var logger = global.Fca.Require.logger;
                        var random = global.FB.Data.BroadCast[Math.floor(Math.random() * global.Fca.Data.BroadCast.length)] || "Ae Zui Zẻ Nhé !";
                    logger.Normal(random);
                }	
                catch (e) {
                    console.log(e);
                    return;
                }
            }
            catch (e) {
                console.log(e);
            }
        },1800 * 1000);
    }
    case false: {
        break;
    }
    default: {
        break;
    }
}