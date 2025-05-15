
let Validator = require("fastest-validator");
let v = new Validator({
    messages: {
        // Register our new error message text
        errorMessage: "The '{field}' field must be an even number! Actual: {actual}"
    }   
    });

validateRequest =  (schema,dto)=> {
    const log = require('../index').Logger;
    var check = v.compile(schema);
    let validationResponse = check(dto)
    log.info('dto validated ' + JSON.stringify(validationResponse));
    if (validationResponse.length>0 ) {
        log.error('data validation failed33333');
        let response=createErrorResponse(validationResponse);
        log.error('data validation failed111' + response);
        return response
    } else {
        return null;
    }
}

function createErrorResponse (validationResponse)  {
    var errors = [];
    var error;
    const log = require('../index').Logger;
    validationResponse.forEach(function (errorRow) {
        error = {
            "message": errorRow.message,
            "field": errorRow.field,
            "description": ""
        }
        errors.push(error);
    });
    log.info('errors::: ' + JSON.stringify(errors));
    return errors;

}

module.exports = {
    generateErrorResponse : createErrorResponse,
    validateRequest : validateRequest
  };
//exports.generateErrorResponse=createErrorResponse