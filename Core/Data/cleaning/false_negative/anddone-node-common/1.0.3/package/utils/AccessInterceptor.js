const swaggerJSDoc = require('swagger-jsdoc');
//const swaggerDefinition = require('./controllers/swaggerDefinition')
const { pathToRegexp, match, parse, compile } = require('path-to-regexp')

function authorize(req, res, options, httpContext, next) {
    console.log('AccessInterceptor -> authorize');
    /*var options = {
        swaggerDefinition: swaggerDefinition,
        apis: ['swagger/*.js']
    };*/

    const swaggerSpec = swaggerJSDoc(options)
    const swaggerJson = JSON.parse(JSON.stringify(swaggerSpec))
    try {
        const isAllowed = validateAccess(swaggerJson, req, httpContext, res);
        if (isAllowed === false) {
            return isAllowed
        }
        return true;

    } catch (error) {
        console.log(error);
        return error;
    }
    next();
}



function validateAccess(jsonData, request, httpContext, res) {
    let accessRightArray = [];
    let isAllowed = true;
    for (var path in jsonData.paths) {
        const values = Object.values(jsonData.paths[path]);
        values.forEach((method) => {
            const replacePath = getReplacePath(path);
            const regexp = pathToRegexp(replacePath);
            var regexp1 = new RegExp(regexp);

            let value = method === jsonData.paths[path][request.method.toLowerCase()];
            const checkExp = regexp1.test(request.path)

            if (checkExp && value) {

                const data = jsonData.paths[path][request.method.toLowerCase()]
                const accessRights = data['accessrights'];

                if (accessRights != undefined) {
                    accessRights.forEach((type) => {
                        var values = Object.values(type);
                        accessRightArray.push(values[0]);
                    })
                    isAllowed = hasAccess(accessRightArray, httpContext)
                    if (isAllowed === false) {
                        return isAllowed;
                    }
                    accessRightArray = [];
                }
            }
        })
    }
    return isAllowed;
}

function hasAccess(accessRights, httpContext) {
    let isAllowed = false;
    if (httpContext.ns.active.IsMerchantAdmin != undefined && httpContext.ns.active.IsMerchantAdmin && accessRights.includes('Merchant'))
        isAllowed = true;
    if (httpContext.ns.active.IsResellerAdmin != undefined && httpContext.ns.active.IsResellerAdmin && accessRights.includes('Reseller'))
        isAllowed = true;
    if (httpContext.ns.active.IsGlobalAdmin != undefined && httpContext.ns.active.IsGlobalAdmin && accessRights.includes('Global'))
        isAllowed = true;
    if (httpContext.ns.active.IsPartnerAdmin != undefined && httpContext.ns.active.IsPartnerAdmin && accessRights.includes('Partner'))
        isAllowed = true;
    if (httpContext.ns.active.IsAdmin != undefined && !httpContext.ns.active.IsAdmin)
        isAllowed = true;
    if (httpContext.get('UserType') === 'Customer' && accessRights.includes('Customer'))
        isAllowed = true;
    return isAllowed;

}


function getReplacePath(path) {
    let str = path.replace(/{/g, ':');
    str = str.replace(/}/g, '');
    return str
}
exports.authorize = authorize;