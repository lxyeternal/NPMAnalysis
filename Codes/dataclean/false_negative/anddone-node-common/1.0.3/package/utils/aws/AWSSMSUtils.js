const log = require('../../Logger').getLogger();
const AWS = require('aws-sdk');

const environment = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = 'us-east-1';//(process.env.AWS_DEFAULT_REGION || 'us-east-1');
AWS.config.update({ region: awsRegion });

var sns = new AWS.SNS({apiVersion: '2010-03-31'});

module.exports = {

    async sendSMS(smsParams) {
        validate(smsParams);
    try{
    var params = {
        Message: smsParams.message, /* required */
        PhoneNumber: smsParams.phoneNumber,
    };
  
    const data =  await sns.publish({
        PhoneNumber: smsParams.phoneNumber,
         Message: smsParams.message,
         MessageAttributes:{
             'AWS.SNS.SMS.SenderID': {
                 'DataType': 'String',
                 'StringValue': 'aurionpro'
             },
             'AWS.SNS.SMS.SMSType': {
                 'DataType': 'String',
                 'StringValue': 'Transactional'
             }
         }}
     ).promise();
     console.log("MessageID is " + data.MessageId);

    return data.MessageId;

    }catch(error){
        log.error(`error occured while sending sms`)
        log.error(error, error.stack);
    }
    }
}

function validate(smsParams) {
    if (!smsParams) {
        console.log('smsParams request is required.');
        throw new Error('smsParams request is required.');
    }
    else if (!smsParams.message) {
        console.log('message is required.');
        throw new Error('message is required.');
    }
    else if (!smsParams.phoneNumber) {
        console.log('phoneNumber is required.');
        throw new Error('phoneNumber is required.');
    }
    
}




