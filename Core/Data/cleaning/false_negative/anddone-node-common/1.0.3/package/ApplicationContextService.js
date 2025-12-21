//const log = require('./Logger/index').getLogger();

const sendResponse= require('./exception/SendResponse')
var jwt = require('jsonwebtoken');
const {UserType} = require('./constants/UserType');

exports.setContextAttributes = async (req, res,httpContext, next)=>{
  const log = require('./index').Logger;
    let  authToken=req.get('Authorization');
     log.info('httpContext : ' + httpContext);

    if (!authToken) {

     // console.log('authToken ' + authToken);
     // const result = sendResponse.unAuthorizedAccess(res);
     // res.status(result.statuscode).send(result.response);
     next();

    } else {
      try{

       

      authToken = authToken.replace('Bearer','').trim();
       const payload = jwt.decode(authToken, {complete: true}).payload;

       if (payload) {
        log.info(JSON.stringify(payload));
      
        if (payload.Admin=='1' && (payload.UserType).toLowerCase()===UserType.GLOBAL) {
          httpContext.set('IsGlobalAdmin',true);
          httpContext.set('IsAdmin',true);

          log.info(`Context - IsGlobalAdmin - ${httpContext.get('IsGlobalAdmin')}`);
          log.info(`Context - IsAdmin - ${httpContext.get('IsAdmin')}`);

        } else if ((payload.Admin==='1') && ((payload.UserType).toLowerCase()==UserType.MERCHANT)) {
          httpContext.set('IsAdmin',true);
          httpContext.set('IsMerchantAdmin',true);

          log.info(`Context - IsMerchantAdmin - ${httpContext.get('IsMerchantAdmin')}`);
          log.info(`Context - IsAdmin - ${httpContext.get('IsAdmin')}`);

        } else if (payload.Admin==='1' && (payload.UserType).toLowerCase()===UserType.RESELLER) {
          httpContext.set('IsResellerAdmin',true);
          httpContext.set('IsAdmin',true);

          log.info(`Context - IsResellerAdmin - ${httpContext.get('IsResellerAdmin')}`);
          log.info(`Context - IsAdmin - ${httpContext.get('IsAdmin')}`);

        } else if (payload.Admin==='1' && (payload.UserType).toLowerCase()===UserType.PARTNER) {
          httpContext.set('IsPartnerAdmin',true);
          httpContext.set('IsAdmin',true);

          log.info(`Context - IsPartnerAdmin - ${httpContext.get('IsPartnerAdmin')}`);
          log.info(`Context - IsAdmin - ${httpContext.get('IsAdmin')}`);

        }else if(payload.Admin==='1' && (payload.UserType).toLowerCase() === UserType.CUSTOMER){
          httpContext.set('IsAdmin',true);
          httpContext.set('CustomerUserName',payload.Id);
          
          log.info(`Context - IsAdmin - ${httpContext.get('IsAdmin')}`);
        }else if (payload.Admin==='0'){
          httpContext.set('IsAdmin',false);
          log.info(`Context - UserType - ${payload.UserType}`);
          log.info(`Context - IsAdmin - ${httpContext.get('IsAdmin')}`);
        }
        httpContext.set('ParentId',payload.ParentId)
        httpContext.set('ResellerId',payload.ResellerId)
        httpContext.set('PartnerId',payload.PartnerId)
        httpContext.set('MerchantId',payload.MerchantId)
        httpContext.set('CustomerId',payload.CustomerId)
        httpContext.set('UserType', payload.UserType)
        httpContext.set('Admin', payload.Admin)

        httpContext.set('username',payload.sub)
        httpContext.set('TimeZone',payload.TimeZone)

        log.info(`username - ${httpContext.get('username')}`);
         next();
       } else {
        return sendResponse.unAuthorizedAccess(res);
       }
      }catch(error){
        const result = sendResponse.unAuthorizedAccess(res);
        res.status(result.statuscode).send(result.response);
      }
    }
  }

//   function userMiddleware (req, res, next) {
//     getUserViaJWT(req.headers.authentication)
//     .then(function(user) {
//       req.user = user
//       next()
//     })
//     .catch(function (error) {
//       res.status(401).end() //replace with proper error handling
//     })
//   }
//   app.use(userMiddleware)


