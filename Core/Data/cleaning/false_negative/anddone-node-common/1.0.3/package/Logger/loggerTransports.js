'use strict'

//const elasticsearch = require('elasticsearch');
const AWS = require('aws-sdk');
const winstonAwsCloudWatch = require('winston-aws-cloudwatch');
const winston = require('winston');
//const awses = require('http-aws-es');
//const WinstonElasticsearch = require('winston-elasticsearch');
const fs = require('fs');
const path = require('path');

const logDir = 'log';
// Create the log directory if it does not exist
// if (!fs.existsSync(logDir)) {
//   fs.mkdirSync(logDir);
// }
// const filename = path.join(logDir, 'results.log');

//const region = 'us-east-1';
//const hosts = ['https://search-aws-es-v-n67kab4wame7fzgneuw7qzehia.us-east-1.es.amazonaws.com'];
//rachna
const awsEnv = (process.env.NODE_ENVIRONMENT || "dev");
const awsRegion = (process.env.AWS_DEFAULT_REGION || "us-east-2");
AWS.config.update({ region: awsRegion });
//const logGroup = process.env.AWS_LAMBDA_LOG_GROUP_NAME;
//const functionName = process.env.AWS_LAMBDA_FUNCTION_NAME;
module.exports.offTransport = () => {
    return {
        transports: []
    };
}

module.exports.consoleTransport = () => {
    return {
        transports: [
            new (winston.transports.Console)({ level: 'info' })
            /*,
            new (winstonAwsCloudWatch)({
                level: 'info',
                timestamp: () => {
                    return new Date().toString()
                },
                json: true,
                //logGroupName: 'apfTest', // REQUIRED
                logGroupName: logGroup,//rachna
                logStreamName: functionName,//rachna
               // logStreamName: module, // REQUIRED
                //logStreamName: 'invoicing', // REQUIRED

                createLogGroup: true,
                createLogStream: true,
                awsRegion: awsRegion,
                formatLog: function (item) {
                    return item.level + ': ' + item.message + ' ' + JSON.stringify(item.meta)
                }
            })*/
         /*  new (winston.transports.Console)({ level: 'info' ,format: winston.format.combine(
            winston.format.timestamp(),
            winston.format.colorize(),
            winston.format.simple(),
            winston.format.printf(info => `${info.timestamp}  ${info.level}: ${info.message}`)
          )}),*/
        ]
    };
}



// Replaces the previous transports with those in the
// new configuration wholesale.
//
// const DailyRotateFile = require('winston-daily-rotate-file');
// logger.configure({
//   level: 'verbose',
//   transports: [
//     new DailyRotateFile(opts)
//   ]
// });

module.exports.fileTransport = () => {
    return {
        transports: [
    // - Write to all logs with level `info` and below to `combined.log` 
    // - Write all logs error (and below) to `error.log`.
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'invoicing.log' }),
        ]
    };
}

module.exports.awsTransport = (module) => {
    const awsConfig = {
        region: region
    }

    // const client = elasticsearch.Client({
    //     hosts: hosts,
    //     connectionClass: awses,
    //     log: 'trace'
    // });

    //Configuring AWS Credentials once
    AWS.config.update({
        region: region
    });

    return {
        transports: [
            new (winstonAwsCloudWatch)({
                level: 'info',
                timestamp: () => {
                    return new Date().toString()
                },
                json: true,
                logGroupName: 'apfTest', // REQUIRED
                
                
                logStreamName: module, // REQUIRED
                //logStreamName: 'invoicing', // REQUIRED

                createLogGroup: true,
                createLogStream: true,
                awsRegion: awsRegion,
                formatLog: function (item) {
                    return item.level + ': ' + item.message + ' ' + JSON.stringify(item.meta)
                }
            }),
            // new (WinstonElasticsearch)({
            //     level: 'info',
            //     client: client,
            //     formatLog: function (item) {
            //         return item.level + ': ' + item.message + ' ' + JSON.stringify(item.meta)
            //     }
            // })
        ]
    };
}
