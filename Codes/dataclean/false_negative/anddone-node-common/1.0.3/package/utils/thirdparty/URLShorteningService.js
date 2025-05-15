const httpClient = require( "axios" );
module.exports = {

    async shortenURL(longURL,apiUrl,accessToken ){
        let shortURL = "";
        var reqHeaders = {
            'Content-Type': 'application/json'
                  }
        try{
            let url = encodeURIComponent( longURL )
            let requestBody = {
            };
            let postURL = apiUrl+"?access_token="+accessToken+`&longUrl=${url}`;
            let response = await httpClient.post( postURL ,requestBody,{ "headers": reqHeaders });
            if( response && response.status === 200 ){
                shortURL = response.data.data.url;
            }
        }catch(error){
            console.log(`error occured while shortening url -  ${longURL}`);
            console.log(error);
        }
        return shortURL;
    
    }
    
    }