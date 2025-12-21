const AWS = require('aws-sdk');

const awsEnv = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
AWS.config.update({ region: awsRegion });
const camelcaseKeys = require('camelcase-keys');
const CoreUtils = require('../CoreUtils');
const httpContext = require('express-http-context');
const TimeZoneConvertor = require('./TimeZoneConverter')
const moment = require('moment');
const log = require('../Logger').getLogger();


let hashids;


module.exports = {

    hashResponse(hashConfig, response, properties,dateproperties) {
        if (properties === undefined || response === undefined) {
            log.error('No properties to unhash');
        }
        hashids = hashConfig;

        response = hash(response, properties,dateproperties);
        return response;

    },

    unHashRequest(hashConfig, request, properties) {
        hashids = hashConfig;
        if (properties === undefined || request === undefined) {
            log.error('No properties to unhash');
        }

        request = unHash(request, properties);
        return request;

    }

}

function unHash(request, properties) {
    if (typeof request !== 'object' || request === null) {
        return request
    }
    if (Array.isArray(request)) {
        return deepUnHashedArray(request, properties);
    }

    return deepUnHashedObject(request, properties);
}

function deepUnHashedObject(request, properties) {
    const result = {}

    Object.keys(request).forEach((key) => {
        let requestKey = request[key]
        let timeZone = httpContext.get("TimeZone");
        if (properties.includes(key) && (typeof requestKey === "string")) {
            const hashedValue = requestKey;

            result[key] = parseInt(hashids.decode(hashedValue));

        } else if (CoreUtils.isInputDateTime(requestKey)) {
            result[key] = CoreUtils.getUTCDate(requestKey, timeZone);
        } else if (CoreUtils.isInputDate(requestKey)) {
            let dateProperty = `${requestKey} 00:00:00`
            result[key] = CoreUtils.getUTCDate(dateProperty, timeZone);
        }
        else {
            const value = requestKey;
            result[key] = unHash(requestKey, properties);
        }

    }, {})
    return result;
}

function deepUnHashedArray(collection, properties) {
    return collection.map((value) => {
        return unHash(value, properties)
    })
}

function hash(response, properties,dateproperties) {
    if (typeof response !== 'object' || response === null) {
        return response;
    }
    if (Array.isArray(response)) {
        return deepHashedArray(response, properties,dateproperties);
    }

    return deepHashedObject(response, properties,dateproperties);
}

function deepHashedObject(response, properties,dateproperties) {
    const result = {}
    Object.keys(response).forEach((key) => {
        if (properties.includes(key)) {
            const unHashedValue = response[key];
            if (unHashedValue !== null && unHashedValue !== "" && unHashedValue != 0 && (typeof(unHashedValue) === 'number')) {
                result[key] = hashids.encode(unHashedValue);
            } else {
                result[key] = unHashedValue;
            }

        } else {
            const value = response[key];
            if (value instanceof Date && value != null) {
                let timezone = 0;
                if (httpContext.get("TimeZone")) {
                    timezone = parseInt(httpContext.get("TimeZone"))
                }
                let toMerchantTimeZone = TimeZoneConvertor.timeZoneConvert(timezone, moment(value).utc(true));

                if (!toMerchantTimeZone) {
                    toMerchantTimeZone = moment(value).utc(true).format('MM-DD-YYYY HH:mm:ss')
                }

                if(dateproperties!= undefined && Array.isArray(dateproperties) && dateproperties.includes(key)){
                    toMerchantTimeZone = toMerchantTimeZone.substring(0,10);
                }

                result[key] = toMerchantTimeZone;
            } else
            //  if (value != null) {
                result[key] = hash(response[key], properties,dateproperties);
            // }
        }

    }, {})
    return camelcaseKeys(result);
}

function deepHashedArray(collection, properties,dateproperties) {
    return collection.map((value) => {
        return hash(value, properties,dateproperties)
    })
}