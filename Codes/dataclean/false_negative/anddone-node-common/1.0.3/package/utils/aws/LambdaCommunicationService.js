const AWS = require('aws-sdk');
const {v1 : uuidv1} = require('uuid');
const jwt = require('jsonwebtoken');
const ms = require('ms');

const SSMConfig = require("../../SSMConfig");
const ssmParam = require('../../config/SSMParameters')['ssm']

const environment = (process.env.NODE_ENVIRONMENT || 'dev');
const region = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
AWS.config.region = region;
const lambdaClient = new AWS.Lambda();

module.exports = {
/**
 * This api is used for lambda inter communication.
 * @param {string} moduleName 
 * @param {string} method 
 * @param {string} path 
 * @param {object} jsonData 
 * @param {string} userType 
 * @param {string} rawToken 
 */
    async invokeAPI(communicationRequest) {
        console.log("LambdaCommunicationService : invokeAPI : Start : " );

        validate(communicationRequest);
        if (!communicationRequest.rawToken) {
            console.log('raw token is required.');
            throw new Error('raw token is required.');
        }
        try {
            let invokePayLoad = await generatePayload(communicationRequest.method, communicationRequest.path, communicationRequest.jsonData, communicationRequest.userType, communicationRequest.rawToken);
            let params = {
                FunctionName: environment.concat('-', communicationRequest.moduleName, '-', 'API'),
                InvocationType: 'RequestResponse',
                Payload: invokePayLoad
            }
            let response = await lambdaClient.invoke(params).promise();
            console.log("LambdaCommunicationService : invokeAPI : End : " );

            return response.Payload;

        } catch (error) {
            console.log("error occured while invoking api ", error);
            console.log("LambdaCommunicationService : invokeAPI : Error : " + JSON.stringify(error.name));
            
            throw error;
        }
    },async  invokeLambdaAPI(communicationRequest) {
        console.log("LambdaCommunicationService : invokeLambdaAPI : Start : " );
        validate(communicationRequest);
    
        try {
            let invokePayLoad = await generatePayload(communicationRequest.method, communicationRequest.path, communicationRequest.jsonData, communicationRequest.userType, '', communicationRequest.id, communicationRequest.parentId, communicationRequest.resellerId,communicationRequest.merchantId);
            let params = {
                FunctionName: environment.concat('-', communicationRequest.moduleName, '-', 'API'),
                InvocationType: 'RequestResponse',
                Payload: invokePayLoad
            }
            let response = await lambdaClient.invoke(params).promise();
            console.log("LambdaCommunicationService : invokeLambdaAPI : End : " );

            return response.Payload;
        } catch (error) {
            console.log("error occured while invoking api ", error);
            console.log("LambdaCommunicationService : invokeLambdaAPI : Error : " + JSON.stringify(error.name));
            throw error;
        }
    
    },async generateJWTToken(userType, id, parentId, resellerId,merchantId){
        return await generateJWTToken(userType, id, parentId, resellerId,merchantId);
    }
}

function validate(communicationRequest) {
    if (!communicationRequest) {
        console.log('communication request is required.');
        throw new Error('communication request is required.');
    }
    else if (!communicationRequest.moduleName) {
        console.log('module name is required.');
        throw new Error('module name is required.');
    }
    else if (!communicationRequest.method) {
        console.log('method is required.');
        throw new Error('method is required.');
    }
    else if (!communicationRequest.path) {
        console.log('path is required.');
        throw new Error('path is required.');
    }
    else if (!communicationRequest.userType) {
        console.log('user type is required.');
        throw new Error('user type is required.');
    }
}

/*function getUserTypeString(userType) {
    switch (userType) {
        case 0:
            return "Reseller"
        case 1:
            return "Merchant"
        case 2:
            return "Global"
    }
}*/

async function generatePayload(method, path, jsonData, userType, rawToken, id, parentId, resellerId = '0',merchantId) {
    console.log("inside generatePayload start")

    if (!rawToken || rawToken === ''){
        rawToken = await generateJWTToken(userType, id, parentId, resellerId,merchantId);
    }
    let queryStringParameters;

    let queryString = path.indexOf('?', 0) > 0 ? path.substring(path.indexOf('?', 0)) : '';

    if (queryString || queryString !== ''){
        queryStringParameters = parseQueryString(queryString);
    }

    let apiEvent = {
        "httpMethod": method,
        "path": path.indexOf("?", 0) > 0 ? path.substring(0, path.indexOf("?", 0)) : path,
        "pathParameters": { "proxy": path },
        "body": (jsonData!= undefined&&jsonData!="") ? JSON.stringify(jsonData):"",
        "requestContext": {
            "requestId": uuidv1().toString(),
            "identity": {
                "caller": "",
                "userAgent": "HPG-LambdaCommunicator"
            }
        },
        "headers": {
            "via": "",
            "X-Forwarded-For": "",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "HPG-LambdaCommunicator",
            "Authorization": "Bearer ".concat(rawToken),
            "Accept-Encoding": "gzip, deflate, br",

        },
        "stageVariables": {"env":`${environment}`},
        "queryStringParameters": queryStringParameters
    }

   /* let apiEvent = {
        HttpMethod: method,
        Path: path.indexOf('?', 0) > 0 ? path.substring(0, path.indexOf('?', 0)) : path,
        PathParameters: { "proxy": path },
        Body: jsonData!= undefined ? JSON.stringify(jsonData):'',
        RequestContext: {
            RequestId: uuidv1().toString(),
            Identity: {
                Caller: "",
                UserAgent: "HPG-LambdaCommunicator"
            }
        },
        Headers: {
            "Via": "",
            "X-Forwarded-For": "",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "HPG-LambdaCommunicator",
            "Authorization": "Bearer ".concat(rawToken),
            'Accept-Encoding': 'gzip, deflate, br',

        },
        StageVariables: {},
        QueryStringParameters: queryStringParameters
    }*/
    console.log("inside generatePayload end")

    return JSON.stringify(apiEvent);
}

function parseQueryString(query) {
    let queryDict = new Object();
    let queryArray = query.replace(/^\?*/, '').split('&');

    queryArray.forEach(element => {
        //let parts = element.replace(/^\=*/, '');
        let parts = element.split('=');
        console.log(parts)
        if (parts.length == 2)
            queryDict[parts[0].trim()] = decodeURI(parts[1]).trim();
        else
            queryDict[parts[0].trim()] = "";
    });

    return queryDict;
}

async function generateJWTToken(userType, id, parentId, resellerId,merchantId) {
    console.log("inside generateJWTToken start")
    const ssmConfig = await SSMConfig.ssmConfig(ssmParam);
    console.log(parentId)

    let payload = {
        Id: id,
        sub: "System",
        Admin: "1",
        UserType: userType,
        jit: "0",
        Role: "0",
        ParentId: (parentId === undefined || parentId === "0")? "0":parentId.toString(),
        ResellerId: resellerId,
        MerchantId: (merchantId === undefined || merchantId === "0")? "0":merchantId.toString(),
        Service: "Service"
    };
    let secretSigningKey = ssmConfig.SigningKey;
    let tokenIssuer = ssmConfig.Issuer;
    let signOptions = {
        issuer: tokenIssuer,
        audience: "HPGServer",
        expiresIn: "2h",
        notBefore: ms('0s')
    };

    let token = jwt.sign(payload, secretSigningKey, signOptions);
    console.log(token);
    console.log("inside generateJWTToken end");

    return token;
}



// var obj = new LambdaCommunicationService();
// obj.invokeAPI("Infrastructure", "POST", "users/sessions", { userName: "SKIndiaMerchant", password: "Admin@1234" }, userType = 1)