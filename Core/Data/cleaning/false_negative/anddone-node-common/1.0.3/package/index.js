'use strict'

// This module is one way of exposing subdependencies to dependent modules
// Modules are still `require`d on demand
const fs = require('fs');
const path = require('path');
//const Logger = require('./Logger/index');
const Logger = require('./Logger').getLogger();
const validation = require('./validation/CoreValidations');
const sendResponse = require('./exception/SendResponse');
const CustomException = require('./exception/CustomException');
const SSMConfig = require('./SSMConfig');
const ApplicationContextService = require('./ApplicationContextService');
const schemaValidation = require('./validation/SchemaValidation');
const AWSS3Utils = require('./utils/aws/AWSS3Utils');
const CoreUtils = require('./CoreUtils');
const FrequencyValidator = require('./validation/FrequencyValidator');
const ScheduleCalculationService = require('./ScheduleCalculationService');
const AWSSNSBasedEmailDispatcher = require('./utils/aws/AWSSNSBasedEmailDispatcher');
const AWSSNSBasedSMSDispatcher = require('./utils/aws/AWSSNSBasedSMSDispatcher')
const LambdaCommunicationService = require('./utils/aws/LambdaCommunicationService');
const AWSSNSUtils = require('./utils/aws/AWSSNSUtils');
const AWSAPIKeyGenerator = require('./utils/aws/AWSAPIKeyGenerator');
const AESEncryptionUsingKMS = require('./utils/aws/AESEncryptionUsingKMS');
const AccessInterceptor = require('./utils/AccessInterceptor');
const AWSSMSUtils = require('./utils/aws/AWSSMSUtils');
const HashIds = require('./utils/HashIds');
const modulePath = path.resolve(__dirname, 'node_modules');
const TimeZoneConverter = require('./utils/TimeZoneConverter');
const Internationalization = require('./utils/Internationalization');
const NumberFormatter = require('./utils/NumberFormatter');
const URLShorteningService = require('./utils/thirdparty/URLShorteningService');
const SecretManagerConfig = require('./SecretManagerConfig');



try {
    console.log('common library initialized*******');
    fs.readdirSync(modulePath)
        .map(subDir => path.resolve(modulePath, subDir))
        .filter(file => fs.statSync(file).isDirectory() && fs.existsSync(path.resolve(file, 'package.json')))
        .forEach(moduleDir => {
            const moduleName = path.basename(moduleDir)
            Object.defineProperty(
                module.exports,
                moduleName, {
                    get: () => require(moduleName)
                })
        })
} catch (error) {
    console.error('************index called modulePath error ***********' + error);
}

module.exports.Logger = Logger
module.exports.CustomException = CustomException;
module.exports.SSMConfig = {
    ssmConfig: SSMConfig.ssmConfig
};
module.exports.SecretManagerConfig = {
    secretManagerConfig: SecretManagerConfig.secretManagerConfig
};

module.exports.ApplicationContextService = {
    setContextAttributes: ApplicationContextService.setContextAttributes
};

module.exports.SendResponse = {

    generateErrorResponse: sendResponse.sendErrorMessage,
    databaseConnectionError: sendResponse.databaseConnectionError,
    dataNotFound: sendResponse.dataNotFound,
    errorMessage: sendResponse.errorMessage,
    sendData: sendResponse.sendData,
    successMessageForPost: sendResponse.successMessageForPost,
    successMessage: sendResponse.successMessage,
    getAllSuccessMessage: sendResponse.getAllSuccessMessage,
    unAuthorizedAccess: sendResponse.unAuthorizedAccess,
    validationException: sendResponse.validationException,
    merchantInActive: sendResponse.merchantInActive,
    invalidMerchant: sendResponse.invalidMerchant,
    successOnlyMessage: sendResponse.successOnlyMessage,
    internalServerError: sendResponse.internalServerError

};

module.exports.Validations = {
    generateErrorResponse: validation.generateErrorResponse,
    validateRequest: validation.validateRequest
};
module.exports.SchemaValidation = {
    validateRequest: schemaValidation.validateRequest
};


module.exports.FrequencyValidator = {
    isValidFrequency: FrequencyValidator.isValidFrequency
};

module.exports.ScheduleCalculationService = {
    getNextDate: ScheduleCalculationService.getNextDate,
    getLastDayOfMonth: ScheduleCalculationService.getLastDayOfMonth

};

module.exports.CoreUtils = {
    convertUCfirst: CoreUtils.convertUCfirst,
    prefixPad: CoreUtils.prefixPad,
    getUTCDate: CoreUtils.getUTCDate,
    getUTC: CoreUtils.getUTC,
    isInputDateTime: CoreUtils.isInputDateTime,
    formatSearchToDate: CoreUtils.formatSearchToDate,
    isInputDate: CoreUtils.isInputDate
};


module.exports.AWSS3Utils = {
    getS3File: AWSS3Utils.getS3File,
    putS3File: AWSS3Utils.putS3File,
    getS3FileStream: AWSS3Utils.getS3FileStream,
    deleteS3File: AWSS3Utils.deleteS3File

};
module.exports.AWSSNSBasedEmailDispatcher = {
    dispatchNotification: AWSSNSBasedEmailDispatcher.dispatchNotification
}

module.exports.AWSSNSBasedSMSDispatcher = {
    dispatchNotification: AWSSNSBasedSMSDispatcher.dispatchNotification
}

module.exports.LambdaCommunicationService = {
    invokeAPI: LambdaCommunicationService.invokeAPI,
    invokeLambdaAPI: LambdaCommunicationService.invokeLambdaAPI,
    generateJWTToken: LambdaCommunicationService.generateJWTToken
}

module.exports.AWSSNSUtils = {
    publish: AWSSNSUtils.publish,
}

module.exports.AWSAPIKeyGenerator = {
    addApiKey: AWSAPIKeyGenerator.addApiKey,
    createUsagePlan: AWSAPIKeyGenerator.createUsagePlan,
    getApiKey: AWSAPIKeyGenerator.getApiKey,
    deleteApiKey: AWSAPIKeyGenerator.deleteApiKey,
    createApiKey: AWSAPIKeyGenerator.createApiKey
}

module.exports.AESEncryptionUsingKMS = {
    encrypt: AESEncryptionUsingKMS.encrypt,
    decrypt: AESEncryptionUsingKMS.decrypt,

}

module.exports.AWSUsagePlanAndApiKey = {
    encrypt: AESEncryptionUsingKMS.encrypt,
    decrypt: AESEncryptionUsingKMS.decrypt,

}

module.exports.AccessInterceptor = {
    authorize: AccessInterceptor.authorize
}

module.exports.HashIds = {
    hashResponse: HashIds.hashResponse,
    unHashRequest: HashIds.unHashRequest
}


module.exports.TimeZoneConverter = {
    timeZoneConvert: TimeZoneConverter.timeZoneConvert
}
module.exports.NumberFormatter = {
    format: NumberFormatter.format
}


module.exports.AWSSMSUtils = {
    sendSMS: AWSSMSUtils.sendSMS
}


module.exports.Internationalization = {
    FormatCurrency: Internationalization.FormatCurrency,
    FormatDate: Internationalization.FormatDate,
    FormatDateTime: Internationalization.FormatDateTime

}

module.exports.URLShorteningService = {
    shortenURL: URLShorteningService.shortenURL
};