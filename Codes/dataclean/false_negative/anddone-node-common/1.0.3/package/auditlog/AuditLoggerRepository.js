const DATE_TIME_DB_FORMAT = "YYYY-MM-DD HH:mm:ss";
const moment = require( "moment" );
const TABLE_NAME = "AuditLog";
var AWS = require('aws-sdk');
const awsEnvironment = (process.env.CORE_ENVIRONMENT || 'dev');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');

class AuditLoggerRepository{

    constructor() {
        /*AWS.config.update({
          accessKeyId: "7grldc",
          secretAccessKey:"04fxu",
          region: "localhost",
          endpoint: "http://localhost:8000"
      });
      this.docClient = new AWS.DynamoDB.DocumentClient();*/
          this.docClient = new AWS.DynamoDB.DocumentClient({ region: awsRegion });
      }
  
      async add(auditLog){
          var params = {
              TableName: TABLE_NAME,
              Item: auditLog
            }
            try {
              let res = await this.docClient.put(params).promise();
              console.log(`AuditLoggerRepository - add -end `)

            } catch (error) {
                console.log(`AuditLoggerRepository - error occured while adding in audit log - ${JSON.stringify(auditLog)} ${error}`)
              //throw new DatabaseException(error);
            }
      }

}

module.exports = AuditLoggerRepository;
