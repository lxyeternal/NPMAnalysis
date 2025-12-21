
const messages = require('../constants/CommonMessages');

exports.merchantInActive = () => {
    const results = {
        statuscode: 400,
        response: {
            message: messages.MerchantInactive
        }
    }
    return results
};

exports.invalidMerchant = () => {
    const results = {
        statuscode: 401,
        response: {
            message: messages.InvalidMerchant
        }
    }
    return results
};


exports.dataNotFound = (message) => {
    return {
        statuscode: 404,
        response: {
            message: message
        }
    }
};

exports.errorMessage = (message) => {
    return {
        statuscode: 400,
        response: {
            message: message
        }
    }
};

exports.unAuthorizedAccess = () => {
    const results = {
        statuscode: 403,
        response: {
            message: messages.UnAuthorizedAccess
        }
    }
    return results
};

exports.internalServerError = () => {
    const results = {
        statuscode: 503,
        response: {
            message: messages.InternalServerError
        }
    }
    return results
};
exports.databaseConnectionError = () => {
    return {
        statuscode: 503,
        response: {
            message: messages.DatabaseConnectionError
        }
    }

};

exports.successMessage = (requestData) => {
    return {
        statuscode: 200,
        response: requestData
    }
};

exports.getAllSuccessMessage = (requestData, count) => {
    let result = {
        totalRowCount: count,
        data: requestData
    }
    return {
        statuscode: 200,
        response: result
    }
};
exports.errorMessage = (message,code) => {
    let statusCode=400;
    if (code) {
        statusCode=code
    }
    return {
        statuscode: statusCode,
        response: {
            message: message
        }
    }
};

exports.errorMessageResponse = (message,code) => {
    let statusCode=400;
    if (code) {
        statusCode=code
    }
    return {
        statuscode: statusCode,
        response:message
    }
};

exports.successMessageForPost = (requestData) => {
    return {
        statuscode: 201,
        response: requestData
    }
};
exports.successOnlyMessage = (message) => {
    return {
        statuscode: 200,
        response: {
            message: message
        }
    }
};
exports.validationException = (errorList) => {
    return {
        statuscode: 400,
        response: {
            message: messages.InvalidFields,
            description: '',
            errors: errorList
        }
    }
};



