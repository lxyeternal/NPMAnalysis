'use strict'

const winstonAwsCloudWatch = require('winston-aws-cloudwatch');
const winston = require('winston');
const config = require('./loggerTransports');

class Logger {

    getLogger(module) {
        const logType = process.env.LOG_TYPE || 'console';
        const level = process.env.LOG_LEVEL || "info";
        let logger;
        console.log(logType);
        switch (logType) {
            case 'off':
                console.log('Logging is off');
                logger = winston.createLogger(config.offTransport());
                logger.cli();
                break;

            case 'console':
                console.log('***********Logging to console***********');
                logger = winston.createLogger(config.consoleTransport());
                logger.format = winston.format.combine(winston.format.colorize(), winston.format.simple())
                break;


            case 'aws':
                console.log('***********Logging to aws****************');
                logger = winston.createLogger(config.awsTransport(module));
                break;

            case 'file':
                console.log('***********Logging to file****************');
                logger = winston.createLogger(config.fileTransport());
                break;

            default:
                console.log('***********Default chosen:Logging to console***********');
                logger = (config.consoleTransport());
                logger.cli();
                break;

        }
        logger.level = level;
        logger.format = this.getRequestLogFormatter();
        // Call exceptions.handle with a transport to handle exceptions
        // logger.exceptions.handle(
        //     new winston.transports.File({ filename: 'exceptions.log' })
        // );

      /*  const DailyRotateFile = require('winston-daily-rotate-file');
        logger.configure({
            level: 'verbose',
            transports: [
             new DailyRotateFile(opts)
            ]
        });*/
        logger.exitOnError = false; //winston will not exit after logging an uncaughtException
        return logger;
    }

    getRequestLogFormatter() {
        const { combine, timestamp, printf } = winston.format;

        return combine(
            timestamp({
                format: 'YYYY-MM-DD HH:mm:ss'
            }),
            // [${info.label}] winston.format.label({ label: path.basename(process.mainModule.filename) }),  
            winston.format.printf(info => `${info.timestamp} ${info.level}  : ${info.message}`)

        );
    }


    logError(err, req, res, next) {
        logger.error(err)
        next();
    }

    logRequest(req, res, next, log) {
        log.info('hello');
        next();
    }

    getLog() {
        return this.logger;
    }



}
module.exports = new Logger;