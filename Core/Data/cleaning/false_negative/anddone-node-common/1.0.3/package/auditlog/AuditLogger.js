const DATE_TIME_DB_FORMAT = "YYYY-MM-DD HH:mm:ss";
const moment = require("moment");
AuditLoggerService = require("./AuditLoggerService");

class AuditLogger {

  constructor() {
    this.auditLoggerService = new AuditLoggerService();
  }

  getPropertyValue(obj, property) {
    let entityId;
    for (let key of Object.keys(obj)) {
      if (typeof obj[key] === 'object') {
        return this.getPropertyValue(obj[key], property)
      }
      if (typeof obj[key] === 'string' && key === property) {
        entityId = obj[key];
        break;

      } else if (typeof obj[key] === 'number' && key === property) {
        entityId = String(obj[key]);
        break;
      }

    }
    return entityId;
  }

  UTC() {
    return moment().utc().format(DATE_TIME_DB_FORMAT);
  }


  async audit(message, subject, messageAttributes) {
    try {



      const entityId = this.getPropertyValue(JSON.parse(message), "id");
      const currentTime = this.UTC();
      const userName = (messageAttributes && messageAttributes.CurrentUserName) ? messageAttributes.CurrentUserName.Value : "system";
      const ipaddress = (messageAttributes && messageAttributes.IPAddress) ? messageAttributes.IPAddress.Value : "255.255.255.255";
      if (entityId === undefined) {
        return;
      }
      console.log("Event Received : EntityId = " + entityId + ", Topic Name = " + subject +
        ", UserName = " + userName + ", IP Address = " + ipaddress);


      await this.auditLoggerService.addAuditLog(entityId, subject, message, userName, ipaddress, currentTime);
    } catch (error) {
      console.log(`AuditLogger - Logs Not Added due to Error : ${error}`);
    }

  }

}
module.exports = AuditLogger;