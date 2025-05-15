const log = require('../../Logger').getLogger();
const AWS = require('aws-sdk');

const awsEnv = (process.env.NODE_ENVIRONMENT || 'Test');
const awsRegion = (process.env.AWS_DEFAULT_REGION || 'us-east-2');
AWS.config.update({ region: awsRegion });

var s3 = new AWS.S3();

module.exports = {

/* This api is used to get file from s3 bucket  */
async getS3File(bucket,file) {

  log.info("AWSUtility : getS3File Start ");
  try{
  validate(bucket, file);
      const params = {
          Bucket: bucket,
          Key: file
        };
      
        const response = await s3.getObject(params).promise();
        let content = response.Body.toString();
        log.info(`s3 response - ${content}`);
      log.info("AWSUtility : getS3File End ");
        return content; 
  } catch (error) {
    log.info(`error occured while fetching ${file} file from s3 bucket ${bucket}`);
      log.error("AWSUtility : getS3File Error : " + error.message);
      throw  error;
  }
},
/* This api is used to get file from s3 bucket  */
async getS3FileStream(bucket,file) {

  log.info("AWSUtility : getS3File Start ");
  try{
  validate(bucket, file);
      const params = {
          Bucket: bucket,
          Key: file
        };
      
        const response = await s3.getObject(params).promise();
        let content = response.Body;
      log.info("AWSUtility : getS3File End ");
        return content; 
  } catch (error) {
    log.info(`error occured while fetching ${file} file from s3 bucket ${bucket}`);
      log.error("AWSUtility : getS3File Error : " + error.message);
      throw  error;
  }
},
async deleteS3File(bucket, file, content, contentType) {

  log.info("AWSUtility : deleteS3File Start ");
  try {

      validate(bucket, file);
      const params = {
          Bucket: bucket,
          Key: file
      };

      const response = await s3.deleteObject(params).promise();

      log.info(`${file} deleteS3File successfully on s3 ${response}`);
      log.info("AWSUtility : deleteS3File End ");
      return content;
  } catch (error) {
      log.info(`error occured while uploading ${file} file to s3 bucket ${bucket}`)

      log.error("AWSUtility : deleteS3File Error : " + error);
      throw error;
  }
},
async putS3File(bucket,file,content,contentType) {

  log.info("AWSUtility : putS3File Start ");
  try{
    if (content === undefined) {
      log.info('content is invalid');
      throw new Error('content is invalid');
    }
      validate(bucket, file);
      const params = {
          Bucket: bucket,
          Key: file,
          Body: content,
          ACL: 'public-read'
        };
        if(contentType!= undefined && contentType != null && contentType != ""){
          params.ContentType = contentType
        }

       
      
     /*   const response = await s3.putObject(params, (err) => {
          if (err) {
            log.info(`error occured while uploading ${file} file to s3 bucket ${bucket}`)
          }
        }).promise();*/
        const response = await s3.putObject(params).promise();

        log.info(`${file} uploaded successfully on s3 ${response}`);
      log.info("AWSUtility : putS3File End ");
        return content; 
  } catch (error) {
      log.info(`error occured while uploading ${file} file to s3 bucket ${bucket}`)

      log.error("AWSUtility : putS3File Error : " + error);
      throw  error;
  }
}
}
function validate(bucket, file) {
  if (bucket === undefined) {
    log.error('bucket name is invalid');
    throw new Error('bucket name is invalid');
  }
  else if (file === undefined) {
    log.error('file name is invalid');
    throw new Error('file name is invalid');
  }
}


