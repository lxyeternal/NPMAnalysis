
module.exports.secretManagerConfig = async (secretNames) => {
    const AWS = require('aws-sdk');
    const log = require('./index').Logger;

    log.info('Input Secret Names::');
    log.info(JSON.stringify(secretNames));

    const awsEnv = process.env.NODE_ENVIRONMENT || secretNames.awsEnvt;
    const awsRegion = process.env.AWS_DEFAULT_REGION || secretNames.awsRegion;
    AWS.config.update({ region: awsRegion });

    const secretsManager = new AWS.SecretsManager();
    const secretValues = {};

    for (const secretName of secretNames.sspMap) {
        try {
            const secretResponse = await secretsManager.getSecretValue({
                SecretId: awsEnv + '/' + secretName.SecretName,
            }).promise();

            if (secretResponse.SecretString) {
                const secretData = JSON.parse(secretResponse.SecretString);
                if (secretName.SecretKey in secretData)
                    secretValues[secretName.Value] = secretData[secretName.SecretKey];
            } else {
                log.warn(`Secret ${secretName} has no SecretString.`);
            }
        } catch (error) {
            log.error(`Error fetching secret ${secretName}: ${error}`);
        }
    }
    log.info('Fetching Output Secrets::');
    return secretValues;
};
