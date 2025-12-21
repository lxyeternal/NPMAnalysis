const moment = require("moment");
const momentTz = require('moment-timezone');
const timeZoneConvertor = require('./utils/TimeZoneConverter');
const EnumHelper = require('./utils/enumHelper')
const TimeZone = require('./constants/TimeZone')
const DATE_TIME_DB_FORMAT = 'YYYY-MM-DD HH:mm:ss';


convertUCfirst = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

//handles upto 10 digit number
prefixPad = (num, size) => {
    return ('000000000' + num).substr(-size);
}

//supported date 2020-05-05T00:36:55.000Z
getUTCDate = (dateValue, timezone) => {

    let dateWithoutTimezone = moment(dateValue, "MM-DD-YYYY HH:mm:ss").format("YYYY-MM-DD HH:mm:ss");
    var formattedDate = momentTz.tz(dateWithoutTimezone, EnumHelper.getEnumByValue(TimeZone, timezone));
    var utcDate = formattedDate.utc().format(DATE_TIME_DB_FORMAT);
    return utcDate;
}

isISOFormat = (inputDate) => {
    var ISO_8601_FULL = /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(([+-]\d\d:\d\d)|Z)?$/i
    return ISO_8601_FULL.test(inputDate);
}
isInputDateTime = (inputDate) => {
    var INPUT_DATE = /^([0]{0,1}[1-9]|1[012])-([1-9]|([012][0-9])|(3[01]))-\d\d\d\d (20|21|22|23|[0-1]?\d):[0-5]?\d:[0-5]?\d$/;
    return INPUT_DATE.test(inputDate);
}

isInputDate = (inputDate) => {
    var INPUT_DATE = /^([0]{0,1}[1-9]|1[012])-([1-9]|([012][0-9])|(3[01]))-\d\d\d\d$/;
    return INPUT_DATE.test(inputDate);
}


formatSearchToDate = (timezone, toDate) => {
    let toMerchantTimeZone = timeZoneConvertor.timeZoneConvert(parseInt(timezone), moment(toDate).utc(true));
    let endDay = moment(toMerchantTimeZone).endOf('day').format(DATE_TIME_DB_FORMAT);
    
    var formattedDate = momentTz.tz(endDay, EnumHelper.getEnumByValue(TimeZone, timezone));
    var utcDate = formattedDate.utc().format(DATE_TIME_DB_FORMAT);
    return utcDate;
}


module.exports = {
    convertUCfirst: convertUCfirst,
    prefixPad: prefixPad,
    getUTCDate: getUTCDate,
    isISOFormat: isISOFormat,
    isInputDateTime: isInputDateTime,
    isInputDate: isInputDate,
    formatSearchToDate: formatSearchToDate
}