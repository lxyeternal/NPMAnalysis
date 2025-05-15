const momentTz = require('moment-timezone');
const DISPLAY_DATETIME_FORMAT = "MM-DD-YYYY HH:mm:ss";

module.exports = {
    timeZoneConvert(timeZone, dateTime) {
        let convertedDate;
        if (dateTime) {
            switch (timeZone) {
                case 1:
                    convertedDate = momentTz.tz(dateTime, 'America/New_York').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 2:
                    convertedDate = momentTz.tz(dateTime, 'America/Chicago').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 3:
                    convertedDate = momentTz.tz(dateTime, 'America/Denver').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 4:
                    convertedDate = momentTz.tz(dateTime, 'America/Los_Angeles').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 5:
                    convertedDate = momentTz.tz(dateTime, 'America/Anchorage').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 6:
                    convertedDate = momentTz.tz(dateTime, 'Pacific/Honolulu').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 7:
                    convertedDate = momentTz.tz(dateTime, 'America/Halifax').format(DISPLAY_DATETIME_FORMAT);
                    break;
                case 8:
                    convertedDate = momentTz.tz(dateTime, 'America/St_Johns').format(DISPLAY_DATETIME_FORMAT);
                    break;

            }

        }
        return convertedDate;
    }
}