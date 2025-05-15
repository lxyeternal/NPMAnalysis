const AWS = require('aws-sdk');
const crypto = require('crypto');

const environment = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
AWS.config.update({ region: awsRegion });

const kms = new AWS.KMS();
const algorithm = 'AES-256-CBC';

module.exports = {

async encrypt(initVector,plainText,keyInfo){
    try{
        const masterKey = extractMasterKey(keyInfo,'keyid');
    const params = {
        KeyId: masterKey,
        KeySpec: 'AES_256'// Specifies the type of data key to return.
    };

    const dataKey = await kms.generateDataKey(params).promise();
    
    // Copy the length of the CiphertextBlob as first byte and concatenate the CiphertextBlob to it
    var length = Buffer.from(['0x' + dataKey.CiphertextBlob.length.toString(16)]);
    var str = Buffer.concat([length, dataKey.CiphertextBlob]);

    // Get a random IV
    const iv = await crypto.randomBytes(16);

    // Concatenate the iv to the buffer
    str = Buffer.concat([str, iv]);
             
    // Create aes encryptor with KMS plain key
    var encryptor = await crypto.createCipheriv(algorithm, dataKey.Plaintext, iv);

    // Encrypt the data
    encryptor.write(plainText);
    encryptor.end();

    // Concatenate the encrypted to the buffer and return the base64 string
    str = Buffer.concat([str, encryptor.read()]);

    return str.toString('base64');
}catch(error){
    console.log(`error occured while encrypting ${plainText}`);
    console.log(error);
}

},

async  decrypt(text) {
        try {
            // Convert the base64 string to buffer
            var buf = Buffer.from(text, 'base64');

            // Get the CiphertextBlob length stored in the firsty byte
            var length = parseInt(buf[0].toString());

            // Extract the CiphertextBlob, IV and 
            var cipherBlob = buf.slice(1, length+1);
            var iv = buf.slice(length + 1, length + 1 + 16);
            var encText = buf.slice(length + 1 + 16, buf.length);

            // Decrypt the CiphertextBlob and get the plaintext key
           const dataKey =  await kms.decrypt({ 'CiphertextBlob':cipherBlob }).promise();
                
           // Create aes decryptor and decrypt the text
            var decryptor = await crypto.createDecipheriv(algorithm, dataKey.Plaintext, iv)
            decryptor.write(encText);
            decryptor.end();
            return decryptor.read().toString();
    }catch (error) {
        console.log(`error occured while decrypting ${text}`);
        console.log(error);        }
}

}

function extractMasterKey(keyInfo, fieldName){
    let keyArn;
    var keyWithValues = keyInfo.split(';');
    for(var keyWithValue of keyWithValues){
        var parts = keyWithValue.split('=');
        if(parts[0].toLowerCase() === fieldName.toLowerCase()){
            keyArn = parts[1];
            break;
        }
    }
    return keyArn;
 }

 /*const ssm = arn value;

    encrypt('','4124932222222223',ssm).then(async value=>{
        console.log(value);
        data = await decrypt(value)
        console.log(data);
    }).catch(error=>{
        console.log(error)
    })*/
    





