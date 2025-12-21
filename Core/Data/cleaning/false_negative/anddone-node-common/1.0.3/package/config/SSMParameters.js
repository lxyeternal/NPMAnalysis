const environment = (process.env.NODE_ENVIRONMENT || 'dev');
const region = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
module.exports = {

    ssm: {
        awsEnvt: `${environment}`,
        awsRegion: `${region}`,
        ssmMap: [
            { "Name": "Token/SigningKey", "Value": "SigningKey" },
            { "Name": "Token/Issuer", "Value": "Issuer" },
            { "Name": "UsagePlanId", "Value": "usagePlanId" }
        ]
    }



}