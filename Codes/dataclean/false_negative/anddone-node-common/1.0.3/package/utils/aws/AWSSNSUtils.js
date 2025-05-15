const log = require('../../Logger').getLogger();
const AWS = require('aws-sdk');

const environment = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
AWS.config.update({ region: awsRegion });
AuditLogger = require("../../auditlog/AuditLogger");
var sns = new AWS.SNS({apiVersion: '2010-03-31'});

module.exports = {

    async publish(topic, subject, message,messageAttributes) {
        var arn = '';
        try{
            const topicName = `${environment}-${topic}`;

            var response = await sns.createTopic({ Name: topicName }).promise();
                arn = response.TopicArn;
                const snsParameters = {
                    Message: message,
                    MessageAttributes:messageAttributes,
                    Subject: subject,
                    TopicArn: arn
                };
                log.info("Topic ARN is " + arn);
                var data = await sns.publish(snsParameters).promise();

                log.info("MessageID is " + data.MessageId);
                let auditLogger = new AuditLogger();
                await auditLogger.audit(message, subject,messageAttributes);
            }catch(error){
                log.error(`error occured while publishing event ${subject} to SNS `)
                log.error(error, error.stack);
            
            }       
    }
}

