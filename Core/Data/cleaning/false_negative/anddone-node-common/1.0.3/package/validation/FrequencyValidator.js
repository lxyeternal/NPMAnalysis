const Frequency = require('../constants/Frequency').Frequency;

module.exports = {

    isValidFrequency: function(frequency, frequencyParam) {

        console.log(frequency);
        console.log(frequencyParam)
        console.log(Frequency.DAILY)
        console.log(JSON.stringify(Frequency))
        if (frequency === Frequency.DAILY) { //Daily
            return frequencyParam == undefined || frequencyParam === "" ? true : false;
        }
        if (frequency === Frequency.WEEKLY || frequency === Frequency.BIWEEKLY) { //Weekly Or BiWeekly
            var regEx = new RegExp("^(?:mon|tue|wed|thu|fri|sat|sun)(?:, )*$");
            return frequencyParam.match(regEx) ? true : false;
        } else if (frequency === Frequency.MONTHLY) { //Monthly
            var regEx = new RegExp("^(0?[1-9]|[12][0-9]|3[01])$");
            return frequencyParam.match(regEx) ? true : false;
        } else if (frequency !== 0) { //  
            return true;
        }
        return false;
    }

}

//let obj = new FrequncyValidationHelper();
//Daily
//console.log(obj.isFrequencyValid(0, "mon"));
//Weekly
//console.log(obj.isFrequencyValid(1, 'mon'));
//console.log(obj.isFrequencyValid(1, 'mon'));
//console.log(obj.isFrequencyValid(3, "mon"));

