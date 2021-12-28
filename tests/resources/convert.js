const fs = require('fs');
const map = require('api-gateway-mapping-template')

module.exports = function convertTemplateToJson(filePath, payload, params, context) {

    const file = fs.readFileSync(filePath, 'utf8');
    return map({template: file, payload: payload, params: params, context: context});

}