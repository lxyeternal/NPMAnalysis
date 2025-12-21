const assert = require('chai');
const FrequncyValidationHelper = require('../validation/FrequencyValidator');

describe("FrequncyValidationHelper Testing", function() {
    it('return true if Daily and frequencyParam is undefined', function() {
        //Arrage 
        let frequency = 0;
        let frequencyParam;

        //Act
        let isTrue = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isTrue, "return True").to.equal(true);
    });

    it("return true if Daily and frequencyParam is '' ", function() {
        //Arrage 
        let frequency = 0;
        let frequencyParam = '';

        //Act
        let isTrue = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isTrue, "return True").to.equal(true);
    });
    it("return false if Daily and frequencyParam is 'mon' ", function() {
        //Arrage 
        let frequency = 0;
        let frequencyParam = "sas";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });
    it('return true if Weekly and frequencyParam is mon|tue|wed|thu|fri|sat|sun', function() {
        //Arrage 
        let frequency = 1;
        let frequencyParam = "tue";

        //Act
        let isTrue = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isTrue, "return True").to.equal(true);
    });

    it('return false if Weekly and frequencyParam is ""', function() {
        //Arrage 
        let frequency = 1;
        let frequencyParam = "";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });


    it('return false if Weekly and frequencyParam is Monday', function() {
        //Arrage 
        let frequency = 1;
        let frequencyParam = "Monday";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });
    //Biweekly

    it('return true if Biweekly and frequencyParam is mon|tue|wed|thu|fri|sat|sun', function() {
        //Arrage 
        let frequency = 2;
        let frequencyParam = "tue";

        //Act
        let isTrue = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isTrue, "return True").to.equal(true);
    });

    it('return false if Biweekly and frequencyParam is ""', function() {
        //Arrage 
        let frequency = 2;
        let frequencyParam = "";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });


    it('return false if Biweekly and frequencyParam is Monday', function() {
        //Arrage 
        let frequency = 2;
        let frequencyParam = "Monday";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });



    it('return true if Monthly and frequencyParam is number string', function() {
        //Arrage 
        let frequency = 3;
        let frequencyParam = "01";

        //Act
        let isTrue = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isTrue, "return true").to.equal(true);
    });
    it('return false if Monthly and frequencyParam is ""', function() {
        //Arrage 
        let frequency = 3;
        let frequencyParam = "";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });
    it('return false if Monthly and frequencyParam is string', function() {
        //Arrage 
        let frequency = 3;
        let frequencyParam = "mon";

        //Act
        let isFalse = FrequncyValidationHelper.isValidFrequency(frequency, frequencyParam);

        //Assert
        assert.expect(isFalse, "return false").to.equal(false);
    });
})