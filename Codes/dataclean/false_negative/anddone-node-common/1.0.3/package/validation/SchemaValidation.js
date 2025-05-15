var Ajv = require('ajv');
var ajv = new Ajv({ v5: true, $data: true, allErrors: true, jsonPointers: true });
// Ajv options allErrors and jsonPointers are required
require('ajv-keywords')(ajv /*, {singleError: true} */ );
require('ajv-errors')(ajv);
const moment = require('moment');
const coreUtils = require('../CoreUtils');
const sendResponse = require('../exception/SendResponse');
const dateTimeRegex = /^\d\d\d\d-([0]{0,1}[1-9]|1[012])-([1-9]|([012][0-9])|(3[01])) (20|21|22|23|[0-1]?\d):[0-5]?\d:[0-5]?\d$/;

validateRequest = (schema, dto) => {
    const log = require('../index').Logger;

    ajv.addFormat('date-time', {
        validate: (dateTimeString) => dateTimeRegex.test(dateTimeString),
        compare: (first,second)=> {
            if(moment(first).isBefore(moment(second))){
                return -1;
            }else if(moment(first).isAfter(moment(second))){
            return 1;
        }else if(moment(first).isSame(moment(second))){
            return 0
        }
    }});
    if(!ajv.getKeyword('isNotEmpty')){
        ajv.addKeyword('isNotEmpty', {
            type: 'string',
            validate: function (schema, data) {
              return typeof data === 'string' && data.trim() !== ''
            },
            errors: false
          });
    }
    
    var validate = ajv.compile(schema);
    var valid = validate(dto);

    if (!valid) {
        log.error('dto validation failed');
        let validationResponse = validate.errors; // processed errors
        log.info('raw dto errors:: ' + JSON.stringify(validationResponse));
        let customErrorResponse = createErrorResponse(validationResponse);
        return sendResponse.validationException(customErrorResponse);
    } else {
        log.info('dto validation passed');
        return null;
    }
}

createErrorResponse = (validationResponse) => {
    var errors = [];

    //console.info('createErrorResponse:' + JSON.stringify(validationResponse));
    validationResponse.forEach(function(errorRow) {
        var error;
        if (errorRow.dataPath) {
            if (errorRow.keyword === 'required') {
                let property = errorRow.params.missingProperty
                error = {
                    "message": "Key_" + coreUtils.convertUCfirst(property) + "CannotBeBlank",
                    "field": errorRow.dataPath + "/" + property
                }
                errors.push(error);
            } else if(errorRow.keyword != 'if'){ // to ignore if error message provided by ajv.
                error = {
                    "message": errorRow.message,
                    "field": errorRow.dataPath.slice(1)
                }
                errors.push(error);
            } 
        } else {
            let internalErrorRow = errorRow;
            if (internalErrorRow.keyword === 'dependencies') {
                let firstProperty = internalErrorRow.params.property
                let secondProperty = internalErrorRow.params.missingProperty
                error = {
                    "message": "Key_" + coreUtils.convertUCfirst(firstProperty) +
                        "And" + coreUtils.convertUCfirst(secondProperty) + "NotToBeEmpty",
                    "field": firstProperty + "," + secondProperty
                }

            }
            if (internalErrorRow.keyword === 'required') {
                let property = internalErrorRow.params.missingProperty
                error = {
                    "message": "Key_" + coreUtils.convertUCfirst(property) + "CannotBeBlank",
                    "field": property
                }
            }
            if (internalErrorRow.keyword === 'additionalProperties') {
                let property = internalErrorRow.params.additionalProperty
                error = {
                    "message": "Key_" + coreUtils.convertUCfirst(property) + "isNotRequired",
                    "field": property
                }
            }
            if (error) {
                errors.push(error);
            }

        }
    });
    return errors;
}
module.exports = {
    validateRequest
}