const AWS = require('aws-sdk');

const awsEnv = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
AWS.config.update({ region: awsRegion });
const SSMConfig = require("../../SSMConfig");
const ssmParam = require('../../config/SSMParameters')['ssm']
const keyTypeVal = "API_KEY"; //constant
const gateway = new AWS.APIGateway();
module.exports = {

    /**
     * This Api used to create Usage Plan in Aws
     * @param {object} usagePlanData 
     * {
     * name: 'String Value'
     * description: 'String Value'
     * period: 'String value'
     * env: 'string Value'
     * apiId: 'string Value'
     * offset: Integer
     * limit: Integer
     * rateLimit: Integer
     * burstLimit: Integer
     * }
     * 
     * Example= {
     * "name": "TEstSanal",
     * "description": "check create or not",
     * "period": "DAY",
     * "env": "Test",
     * "apiId": "k5c5nbh1p9",
     * "offset": 0,
     * "rateLimit": 100,
     * "burstLimit": 200 
     * }
     */

    async createUsagePlan(usagePlanData) {
        console.log('AWSUsagePlane : createUsagePlan Start')
        try {
            let params = {
                "name": usagePlanData.name,
                "description": usagePlanData.description,
                "apiStages": [{
                    "stage": usagePlanData.env,
                    "apiId": usagePlanData.apiId
                }],
                "quota": {
                    "period": usagePlanData.period,
                    "offset": usagePlanData.offset,
                    "limit": usagePlanData.limit
                },
                "throttle": {
                    "rateLimit": usagePlanData.rateLimit,
                    "burstLimit": usagePlanData.burstLimit
                }
            }

            let response = await gateway.createUsagePlan(params).promise();

            console.log(`Create Usage  plane ${response}`)
            console.log("AWSUsagePlane : createUsagePlan End ");
            return response
        } catch (error) {
            console.log('error occured while create Usage Plane');
            console.log("AWSUsagePlane: createUsePlane Error : " + error.message);
            throw error;
        }
    },

    /**
     * This Api Used to get ApiKey
     * @param {object} usagePlanData 
     * {
     *  customerId: 'STRING Value',
     *  includeValues: Boolean,
     *  limit: Integer
     *  nameQuery: 'String Value',
     *  position: 'String Value'
     * }
     * 
     * Example:-
     * usagePlanData = {
            customerId: 'b38DNdLj',
            includeValues: false|| true,
            limit: 25,
            nameQuery: 'sanal',
            position: null
        }
     */

    async getApiKey(usagePlanData) {
        try {
            console.log('AWSApiGatewayApiKey : getApiKey Start')
            var params = {
                customerId: usagePlanData.customerId,
                includeValues: usagePlanData.includeValues,
                limit: usagePlanData.limit,
                nameQuery: usagePlanData.nameQuery,
                position: usagePlanData.position
            }
            let apiKeyResult = await gateway.getApiKeys(params).promise();
            console.log('AWSApiGatewayApiKey : getApiKey End')
            return apiKeyResult.items[0];
        } catch (error) {
            console.log('AWSApiGatewayApiKey : getApiKey error occured: ' + error)
            console.log('AWSApiGatewayApiKey : getApiKey error occured:' + error.message);
            throw error
        }
    },
    /**
     * This Api Used to delete ApiKey
     * @param {object} usagePlanData 
     * {
     *  customerId: 'STRING Value',
     *  includeValues: Boolean,
     *  limit: Integer
     *  nameQuery: 'String Value',
     *  position: 'String Value'
     * }
     * 
     * Example:-
     * usagePlanData = {
            customerId: 'b38DNdLj',
            includeValues: false|| true,
            limit: 25,
            nameQuery: 'sanal',
            position: null
        }
     */

    async deleteApiKey(usagePlanData) {
        try {
            console.log('AWSApiGatewayApiKey : deleteApiKey Start')
            let getApiKeyData = await this.getApiKey(usagePlanData);
            var params = {
                apiKey: getApiKeyData.id
            }
            let deleteApiKeyResponse = await gateway.deleteApiKey(params).promise();
            console.log('AWSApiGatewayApiKey : deleteApiKey Start')
            return deleteApiKeyResponse;

        } catch (error) {
            console.log('AWSApiGatewayApiKey : deleteApiKey error occured: ' + error)
            console.log('AWSApiGatewayApiKey : deleteApiKey error occured:' + error.message);
            throw error
        }
    },
    /**
     * This Api used to crate ApiKey
     * @param {object} keyData
     * {
     * customerId: 'String Value',  
     * name: 'String Value',
     * description: 'String Value',
     * stageKeys: [{
     *                  "restApiId": 'String Value',
     *                  "stageName": 'String Value'
     *              }],
     * isAutoGeneratedValue: boolean,
     * value: 'String Value'
     *}
     * 
     * Example-
     *  customerId: '3kW17a2n',
        name: 'sample Name',
        description: 'Sample Description',
                    stageKeys: [{
                        "restApiId": 'wOdLYWGD',
                        "stageName": 'Test'
                    }],
        isAutoGeneratedValue: true,
        value: 'DV66HY8-2GR41PN-MEV6DSE-RV6PRQZ'
     */

    async createApiKey(keyData) {
        try {
            console.log('AWSApiGatewayApiKey : createApiKey Start');
            params = {
                customerId: keyData.customerId,
                name: keyData.name,
                description: keyData.description,
                enabled: true,
                generateDistinctId: true,
                stageKeys: []
            }
            if (!keyData.isAutoGeneratedValue) {
                params.value = keyData.value;
            }

            keyData.stageKeys.forEach(element => {
                params.stageKeys.push({
                    restApiId: element.restApiId,
                    stageName: element.stageName
                });
            });

            const key = await gateway.createApiKey(params).promise();
            console.log('AWSApiGatewayApiKey : createApiKey End');
            return key;
        } catch (error) {
            console.log('AWSApiGatewayApiKey : createApiKey error occured:' + error);
            console.log('AWSApiGatewayApiKey : createApiKey error occured:' + error.message);
            throw error
        }
    },

    /**
     * This Api used add ApiKey in usage plan
     * @param {object} usagePlanData
     * {
     * customerId: 'String Value',
     * includeValues: boolean,
     * limit: Integer,
     * name: 'String Value',
     * position: 'String Value',
     * description: 'String Value',
     * restApiId: 'String Value',
     * isAutoGeneratedValue: Boolean,
     * value: 'String Value'
     * }
     * 
     * Example-
     * const usagePlanData = {
            customerId: 'b38DNdLj',
            includeValues: false,
            limit: 25,
            name: 'sanal',
            position: null,
            description: 'api key',
            restApiId: "k5c5nbh1p9",
            stageName: "Test",
            isAutoGeneratedValue: false,
            value: '5M14FFM-R8JMVZQ-GBS4GMP-J7KHG4F'
        }
     */
    async addApiKey(usagePlanData) {

        try {
            console.log('AWSApiGatewayUsagePlan : addApiKey Start');
            const ssmConfig = await SSMConfig.ssmConfig(ssmParam);
            const usagePlanIdVal = ssmConfig.usagePlanId;
            validate(usagePlanData)

            let deleteApiKeyData = {
                customerId: usagePlanData.customerId,
                includeValues: false,
                limit: usagePlanData.limit,
                nameQuery: usagePlanData.name,
                position: usagePlanData.position
            }
            let keyData = {
                customerId: usagePlanData.customerId,
                name: usagePlanData.name,
                description: usagePlanData.description,
                stageKeys: [{
                    "restApiId": usagePlanData.restApiId,
                    "stageName": usagePlanData.stageName
                }],
                isAutoGeneratedValue: usagePlanData.isAutoGeneratedValue,
                value: usagePlanData.value
            }
            console.log("deleteApiKeyData: ", deleteApiKeyData)
            console.log("keyData: ", keyData)
            let isKeyPresent = await this.getApiKey(deleteApiKeyData);
            if (isKeyPresent) {
                let deleteApiKeyResponse = await this.deleteApiKey(deleteApiKeyData);
            }
            let generateApiKeyResponse = await this.createApiKey(keyData);
            let params = {
                keyId: generateApiKeyResponse.id,
                keyType: keyTypeVal,
                usagePlanId: usagePlanIdVal
            }
            let addUsagePlanApiKeyResponse = await gateway.createUsagePlanKey(params).promise();
            console.log('AWSApiGatewayUsagePlan : addApiKey End');
            return addUsagePlanApiKeyResponse;
        } catch (error) {
            console.log('AWSApiGatewayUsagePlan : addUsagePlanApiKey error occured:' + error);
            console.log('AWSApiGatewayUsagePlan : addUsagePlanApiKey error occured:' + error.message);
            throw error
        }
    }

}

function validate(usagePlanData) {

    if (!usagePlanData) {
        throw new Error('usagePlanData is required');
    }
    if (!usagePlanData.customerId) {
        throw new Error('customerId is required');
    }
    if (!usagePlanData.name) {
        throw new Error('name is required');
    }
    if (!usagePlanData.limit) {
        throw new Error('limit is required');
    }
    if (!usagePlanData.restApiId) {
        throw new Error('restApiId is required');
    }
    if (!usagePlanData.stageName) {
        throw new Error('stageName is required');
    }
}