const assert = require('chai');
const ScheduleCalculationService = require('../ScheduleCalculationService');
const moment = require('moment');
const Frequency = {
    DAILY: 0,
    WEEKLY: 1,
    BIWEEKLY: 2,
    MONTHLY: 3,
    QUARTERLY: 4,
    HALFYEARLY: 5,
    ANNUALLY: 6
}
describe('scheduleCalculationServiceTest', function() {
    it('should return next day of current date', function() {
        //Arrage 

        let startDate = moment("2019-01-02");
        let currentDate = moment("2019-09-30").toISOString();
        let includeCurrentDate = true;
        let frequencyParam = "Sun";
        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.DAILY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", nextDate)

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-10-01");
    });
    it('should return current date if ', function() {
        //Arrage
        let startDate = moment("2019-01-02");
        let currentDate = moment().toISOString();
        let includeCurrentDate = false;
        let frequencyParam = "Sunday";
        //Act
        let nextDate = ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.DAILY, frequencyParam, includeCurrentDate);
        console.log(nextDate)

        //Assert
        assert.expect(moment(nextDate).date(), "date are equal").to.equal(moment().date());
        assert.expect(moment(nextDate).month(), "month are equal").to.equal(moment().month());
        assert.expect(moment(nextDate).year(), "year are equal").to.equal(moment().year());
    });

    it('should return current date if ', function() {
        //Arrage
        let startDate = moment("2019-01-02");
        let currentDate = moment().toISOString();
        let includeCurrentDate = false;
        let frequencyParam = "Sunday";
        //Act
        let nextDate = ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.DAILY, frequencyParam, includeCurrentDate);
        console.log(nextDate)

        //Assert
        assert.expect(moment(nextDate).date(), "date are equal").to.equal(moment().date());
        assert.expect(moment(nextDate).month(), "month are equal").to.equal(moment().month());
        assert.expect(moment(nextDate).year(), "year are equal").to.equal(moment().year());
    });

    it('should return current week next sunday date', function() {
        //Arrage
        let startDate = moment("2019-01-02").toISOString();
        let currentDate = moment("2019-09-26").toISOString();
        let includeCurrentDate = true;
        let frequencyParam = "Sunday";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.WEEKLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-09-29");
    })

    it('should return current week next sunday date', function() {
        //Arrage
        let startDate = moment("2019-01-02").toISOString();
        let currentDate = moment("2019-09-20").toISOString();
        let includeCurrentDate = true;
        let frequencyParam = "Sunday";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.WEEKLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-09-22");
    })


    it('should return next date month 5', function() {
        //Arrage
        let startDate = moment("2019-01-01").toISOString();
        let currentDate = moment("2019-10-05").toISOString();
        let includeCurrentDate = true;
        let frequencyParam = 5;

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.MONTHLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-10-05");
    })

    it('should return next date month last', function() {
        //Arrage
        let startDate = moment("2019-01-01").toISOString();
        let currentDate = moment("2019-10-05").toISOString();
        let includeCurrentDate = true;
        let frequencyParam = "Last";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.MONTHLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-10-31");
    })


    it('should return next date BiWeekly week after week date on sunday', function() {
        //Arrage
        let startDate = moment("2019-01-02").toISOString();
        let currentDate = moment("2019-09-18").toISOString()
        let includeCurrentDate = false;
        let frequencyParam = "Sunday";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.BIWEEKLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-09-29");
    })

    it('should return next date QUARTERLY month', function() {
        //Arrage
        let startDate = moment("2019-01-01").toISOString();
        let currentDate = moment("2019-01-18").toISOString()
        let includeCurrentDate = false;
        let frequencyParam = "Sunday";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.QUARTERLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-04-01");
    })
    it('should return next date HALFYEARLY', function() {
        //Arrage
        let startDate = moment("2019-01-01").toISOString();
        let currentDate = moment("2019-01-18").toISOString()
        let includeCurrentDate = false;
        let frequencyParam = "Sunday";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.HALFYEARLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2019-07-01");
    })

    it('should return next date ANNUALLY', function() {
        //Arrage
        let startDate = moment("2019-01-01").toISOString();
        let currentDate = moment("2020-01-18").toISOString()
        let includeCurrentDate = false;
        let frequencyParam = "Sunday";

        //Act
        let nextDate = moment(ScheduleCalculationService.getNextDate(startDate, currentDate, Frequency.ANNUALLY, frequencyParam, includeCurrentDate)).format("YYYY-MM-DD").toString();
        console.log("nextDate", moment(nextDate).format("YYYY-MM-DD"))

        //Assert
        assert.expect(nextDate, "date are equal").to.equal("2021-01-01");
    })
})