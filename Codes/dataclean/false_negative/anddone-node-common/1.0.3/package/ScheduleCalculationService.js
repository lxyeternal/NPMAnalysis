const moment = require('moment');
const Frequency = require('./constants/Frequency').Frequency;
const log = require('./Logger').getLogger();

module.exports = {

    getNextDate(startDate, currentDate, frequency, frequencyParam, includeCurrentDate) {
        log.info('frequencyParam -', frequencyParam);
        log.info('frequency -', frequency);

        switch (frequency) {
            case Frequency.DAILY:
                {
                    if (moment(currentDate).isBefore(startDate)) {
                        return startDate
                    }
                    if (includeCurrentDate) {
                        var new_date = moment(currentDate).add(1, 'day');
                        return new_date.format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                    }
                    const returnDate = moment(currentDate).format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                    log.info("Date : " + returnDate);
                    return returnDate;
                }
            case Frequency.WEEKLY:
                {
                    let dayOfFrequencyParam = moment().day(frequencyParam);
                    let dayOfWeek = moment(dayOfFrequencyParam).day();
                    let currentDayOfWeek = moment(currentDate).day();
                    let daysToAdd;

                    if (currentDayOfWeek == dayOfWeek && includeCurrentDate)
                        daysToAdd = 0;
                    else if (currentDayOfWeek < dayOfWeek)
                        daysToAdd = dayOfWeek - currentDayOfWeek;
                    else
                        daysToAdd = 7 - (currentDayOfWeek - dayOfWeek);

                    let date = moment(currentDate).add(daysToAdd, 'days');
                    while (date.isBefore(startDate)) {
                        date = moment(date).add(7, 'days')
                    }
                    const returnDate = date.format("YYYY-MM-DDTHH:mm:ss.SSS[Z]")
                    log.info("Date : " + returnDate);
                    return returnDate;
                }
            case Frequency.BIWEEKLY:
                {
                    let date = moment(this.getNextDate(startDate, currentDate, Frequency.WEEKLY, frequencyParam, includeCurrentDate));
                    let diffDay = date.diff(startDate, 'days');
                    let weeks = diffDay / 7;
                    if (weeks % 2 == 0) {
                        const returnDate = moment(date).format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                        log.info("Date : " + returnDate);
                        return returnDate;

                    }
                    const returnDate = date.add(7, 'days').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                    log.info("Date : " + returnDate);
                    return returnDate;
                }
            case Frequency.MONTHLY:
                {

                    frequencyParam = currentDate > startDate ? this.getLastDayOfMonth(currentDate, frequencyParam) : this.getLastDayOfMonth(startDate, frequencyParam);
                    let dayOfMonth = frequencyParam;
                    let date = moment.utc("0001-01-01");
                    if (dayOfMonth != null) {
                        let currentDayOfMonth = moment(currentDate).date();
                        if (currentDayOfMonth == dayOfMonth && includeCurrentDate) {
                            date = currentDate;
                        } else if (currentDayOfMonth < dayOfMonth) {
                            try {
                                date = currentDate > startDate ?
                                    date = moment(new Date(moment(currentDate).year(), moment(currentDate).month(), dayOfMonth)) :
                                    date = moment(new Date(moment(startDate).year(), moment(startDate).month(), dayOfMonth));
                            } catch (excep) {
                                date = moment(new Date(moment(currentDate).year(), moment(currentDate).month(), 1)).add(1, 'month').subtract(1, 'days').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                            }
                        } else {
                            date = moment(new Date(moment(currentDate).year(), moment(currentDate).month(), dayOfMonth)).add(1, 'month').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                        }
                        while (moment(date).isBefore(startDate)) {
                            date = moment(date).add(1, 'month');
                        }
                    } else {
                        console.log("Else Monthly");
                        let startMoreThanCurrent = false;
                        let nextMonth = moment(currentDate).add(1, 'month');
                        if (currentDate < startDate) {
                            nextMonth = moment(startDate).add(1, 'month');
                            startMoreThanCurrent = true;
                        }
                        let lastDateOfCurrentMonth = moment(new Date(moment(nextMonth).year(), moment(nextMonth).month(), 1)).add(-1, 'day');
                        if (includeCurrentDate || startMoreThanCurrent)
                            date = lastDateOfCurrentMonth;
                        else {
                            if (moment(currentDate).date() == moment(lastDateOfCurrentMonth).date()) {
                                let nextMonthDate = moment(lastDateOfCurrentMonth).add(2, 'month');
                                date = moment(new Date(moment(nextMonthDate).year(), moment(nextMonthDate).month(), 1)).add(-1, 'days')
                            } else
                                date = lastDateOfCurrentMonth;
                        }
                    }
                    console.log("Date : ", moment(date).format("YYYY-MM-DDTHH:mm:ss.SSS[Z]"));
                    return moment(date).format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                }

            case Frequency.QUARTERLY:
                {
                    frequencyParam = moment(startDate).date();
                    let date1 = moment(this.getNextDate(startDate, currentDate, Frequency.MONTHLY, frequencyParam, includeCurrentDate));
                    let monthDiff = date1.diff(startDate, 'month');
                    if (frequencyParam != null) {
                        if (moment(startDate).date() <= frequencyParam) {
                            let calmonth = (3 - monthDiff) % 3;
                            return date1.add(calmonth, 'month').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                        }
                    }
                    let calmonths = (3 - monthDiff) % 3;
                    let addCalmonth = date1.add(calmonths, 'month');
                    console.log("Date : ", addCalmonth.add(1, 'month').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]"));
                    return addCalmonth.add(1, 'month').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                }
            case Frequency.HALFYEARLY:
                {

                    frequencyParam = moment(startDate).date();
                    let date = moment(this.getNextDate(startDate, currentDate, Frequency.MONTHLY, frequencyParam, includeCurrentDate));
                    let monthDiff = date.diff(startDate, 'month');
                    if (frequencyParam != null) {
                        if (moment(startDate).date() <= frequencyParam) {
                            let calmonth = (6 - monthDiff) % 6;
                            const returnDate = date.add(calmonth, 'month').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                            log.info("Date : " + returnDate);
                            return returnDate;
                        }

                    }
                    let calmonth = (6 - monthDiff) % 6;
                    let addCalmonth = date.add(calmonths, 'month');

                    const returnDate = addCalmonth.add(1, 'month').format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                    log.info("Date : " + returnDate);
                    return returnDate;
                }
            case Frequency.ANNUALLY:
                let dateToReturn = moment(startDate);
                while (dateToReturn.isBefore(currentDate) || (includeCurrentDate && dateToReturn == currentDate)) {
                    dateToReturn = moment(dateToReturn).add(1, 'year')
                }
                const returnDate = dateToReturn.format("YYYY-MM-DDTHH:mm:ss.SSS[Z]");
                log.info("Date : " + returnDate);
                return returnDate;

        }
    },


    getLastDayOfMonth(date, frequencyParam) {
        if (frequencyParam !== null) {

            if (frequencyParam === "Last") {
                frequencyParam = moment(date).endOf('month').date();
            }
        }
        return frequencyParam
    }
}

/*var a = new ScheduleCalculationService();
console.log(a.GetNextDate(moment("2019-01-02"), moment().toISOString(), Frequency.DAILY, "Sunday", false));
console.log(a.GetNextDate(moment("2019-01-02"), moment("2019-09-30").toISOString(), Frequency.WEEKLY, "Sunday", true));
console.log(a.GetNextDate(moment("2019-01-02").toISOString(), moment().toISOString(), Frequency.MONTHLY, "last", true));
console.log(a.GetNextDate(moment("2019-01-02").toISOString(), moment().toISOString(), Frequency.BIWEEKLY, "Sunday", false));
console.log(a.GetNextDate(moment("2020-01-02").toISOString(), moment().toISOString(), Frequency.QUARTERLY, null, false));
console.log(a.GetNextDate(moment("2020-01-02").toISOString(), moment().toISOString(), Frequency.HALFYEARLY, null, false));
console.log(a.GetNextDate(moment("2020-01-02").toISOString(), moment().toISOString(), Frequency.ANNUALLY, null, false));
*/