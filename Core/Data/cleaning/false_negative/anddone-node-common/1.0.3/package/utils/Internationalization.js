const moment = require('moment');
const log = require('../Logger').getLogger();

module.exports = {

    FormatCurrency(amount, culture, currencyFormat) {
        log.info(`Internationalization: FormatCurrency start`);
        log.info(`Amount:${amount}, Culture: ${culture} And currencyFormat: ${currencyFormat}`);

        if (amount === null || amount === undefined) {
            log.error(`Internationalization: FormatCurrency Error amount null or undfined`);
            return null;
        }
        if (culture === null || culture === undefined) {
            log.error(`Internationalization: FormatCurrency Error currencyFormat null or undfined`);
            return null;
        }
        if ((currencyFormat === null || currencyFormat === undefined)) {

            log.error(`Internationalization: FormatCurrency Error   currencyFormat null or undfined`);
            return null;
        }

        if (typeof amount != "number") {
            log.error(`Internationalization: FormatCurrency Error amount not number`);
            return null;
        }
        if (typeof culture != "string") {
            log.error(`Internationalization: FormatCurrency Error culture not string`);
            return null;
        }
        if (typeof currencyFormat != "string") {
            log.error(`Internationalization: FormatCurrency Error currencyFormat not string`);
            return null;
        }

        const formatter = new Intl.NumberFormat(culture, {
            style: 'currency',
            currency: currencyFormat,
            minimumFractionDigits: 2
        });

        amount = formatter.format(amount);

        log.info(`Amount: ${amount}`);
        log.info(`Internationalization: FormatCurrency End`);
        return amount;
    },

    FormatDate(date, dateFormat) {
        log.info(`Internationalization: FormatDate start`);
        log.info(`Date:${date},  And DateFormat: ${dateFormat}`);

        if (date === null || date === undefined && dateFormat === null || dateFormat === undefined) {
            log.error(`Internationalization: FormatDate Error, Date and currencyFormat null or undfined`);
            return null;
        }

        if (typeof dateFormat != "string") {

            log.error(`Internationalization: FormatCurrency Error dateFormat not string`);
            return null;
        }

        date = moment(date).format(dateFormat);
        log.info(`Date: ${date}`);
        log.info(`Internationalization: FormatDate End`);
        return date;
    },

    FormatDateTime(dateTime, dateFormatTime) {
        log.info(`Internationalization: FormatDateTime start`);
        log.info(`DateTime :${dateTime},  And DateFormatTime: ${dateFormatTime}`);

        if (dateTime === null || dateTime === undefined && dateFormatTime === null || dateFormatTime === undefined) {
            log.error(`Internationalization: FormatDate Error, dateTime and dateFormatTime null or undfined`);
            return null;
        }

        if (typeof dateFormatTime != "string") {
            log.error(`Internationalization: FormatCurrency Error dateFormatTime not string`);
            return null;
        }

        dateTime = moment(dateTime).format(dateFormatTime);

        log.info(`DateTime: ${dateTime}`);
        log.info(`Internationalization: FormatDateTime End`);
        return dateTime;
    }
}