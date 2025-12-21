const log = require('../../Logger').getLogger();
const AWS = require('aws-sdk');

const AWSSNSUtils = require('./AWSSNSUtils');
const environment = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');

AWS.config.update({ region: awsRegion });
const topicName = "Infrastructure-EmailHandler";
const subject = 'Infrastructure-EmailHandler';

var sns = new AWS.SNS();

    module.exports = {

    async  dispatchNotification(tagData, context) {
        const messageAttributes =  getAttributs(context);
        await AWSSNSUtils.publish(topicName, subject, JSON.stringify(tagData),messageAttributes);
        log.info('email notification published!!')

    }
}

function getAttributs(context) {
    let messageAttributes = {};
    context.forEach((contextValue) =>{
             var value =  {
                      DataType : "String",
                      StringValue : contextValue.Value
                    }   
                    messageAttributes[contextValue.Key] = value;                          
    });

    return messageAttributes;
}


