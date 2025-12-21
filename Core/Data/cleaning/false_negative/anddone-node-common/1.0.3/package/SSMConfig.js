//const log = require('./Logger/index').getLogger();

module.exports.ssmConfig = async (ssmParameters) => {
  const log = require('./index').Logger;
  log.info('Input SSM Parameters::');
  log.info(JSON.stringify(ssmParameters.ssmMap));

  const AWS = require('aws-sdk');

  const awsEnv = (process.env.NODE_ENVIRONMENT || ssmParameters.awsEnvt);
  const awsRegion = (process.env.AWS_DEFAULT_REGION || ssmParameters.awsRegion);
  AWS.config.update({ region: awsRegion });

  var ssm = new AWS.SSM();
  var ssmConfiguration = {};
  var namesArray = [];
  var parameterStoreJSON = {};

  for (var param of ssmParameters.ssmMap) {
    namesArray.push('/' + awsEnv + '/' + param.Name);
  }
  const paramater = await ssm.getParameters({
    Names: namesArray,
    WithDecryption: true
  }).promise()

  paramater.Parameters.forEach(record => {
    const key = record.Name.substring(1).split('/').shift();
    const ssnName = record.Name.substring(1).replace(key, '').substring(1);
    for (var param of ssmParameters.ssmMap) {
      if (ssnName === param.Name) {
        parameterStoreJSON[param.Value] = record.Value;
        break;
      }
    }
  });
  log.info('Fetching Output SSM Parameters::');
  //log.info(JSON.stringify(parameterStoreJSON));

  return parameterStoreJSON;
}


//ssmConfig(require('../utils/SSMParameters.js')['ssm']);
