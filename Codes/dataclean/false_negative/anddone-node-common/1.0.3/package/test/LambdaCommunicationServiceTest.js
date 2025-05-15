const LambdaCommunicationService = require('../utils/aws/LambdaCommunicationService');
const assert = require('chai');
var expect = require('chai').expect;


describe('LambdaCommunicationServiceTestCase',async function() {

    it('return 200 Status code', async function() {
        //Arrange 
        this.enableTimeouts(false)

        let path = "/countries";
        let jsonData = {};

        let communicationRequest = {
            moduleName: "Fraud",
            method: "GET",
            path: path,
            userType: "1",
        //    parentId: "67",
            jsonData:jsonData
        }
        //Act
        const resultString = await LambdaCommunicationService.invokeLambdaAPI(communicationRequest);
            var resultJson = JSON.parse(resultString);

            //Assert
            expect(resultJson.statusCode).to.equal(200);
            expect(resultJson.body).to.not.equal(null);
        
    });

    it('return 200 status with successful login',async function() {
        //Arrange 
        this.enableTimeouts(false)

        let path = "/users/sessions";
        let jsonData = {
            userName: "SanalMerchant",
            password: "SanalMerchant"
        };

        let communicationRequest = {
            moduleName: "Infrastructure",
            method: "POST",
            path: path,
            userType: "1",
            parentId: "67",
            jsonData:jsonData
        }

        //Act
       const resultString = await LambdaCommunicationService.invokeLambdaAPI(communicationRequest);
            var resultJson = JSON.parse(resultString);
            //Assert
            expect(resultJson.statusCode).to.equal(200);
            expect(resultJson.body).to.not.equal(null);
        
    });

    it('return the Merchant Data', async function() {
        //Arrange   
        this.enableTimeouts(false)

        let path = "/merchants/n7de378M/customers";
        let communicationRequest = {
            moduleName: "Domain",
            method: "Get",
            path: path,
            userType: "1",
            parentId: "67"
        }

        //Act
       const resultString = await LambdaCommunicationService.invokeLambdaAPI(communicationRequest);
       var resultJson = JSON.parse(resultString);
            console.log(resultJson.statusCode);

            //Assert
            expect(resultJson.statusCode).to.equal(200);
       
    })

})