const DATE_TIME_DB_FORMAT = "YYYY-MM-DD HH:mm:ss";
const moment = require("moment");
const AuditLogRepository = require("./AuditLoggerRepository");

class AuditLoggerService {

    constructor() {
        this.auditLogRepository = new AuditLogRepository();
    }

    async addAuditLog(entityId = 0, subject = "", message = "", currentUserName = "", ipAddress = "", currentTime = "") {

        try {
            const auditLog = {
                Id: entityId,
                CurrentUserName: currentUserName,
                EntityType: subject,
                EventData: message,
                CurrentTime: currentTime,
                IPAddress: ipAddress
            }

            await this.auditLogRepository.add(auditLog);

        } catch (error) {
            console.log(` AuditLoggerService - Error occured while adding Auding Log- subject - ${subject} ${error}`)
        }
    }

    UTC() {
        return moment().utc().format(DATE_TIME_DB_FORMAT);
    }



}

module.exports = AuditLoggerService;