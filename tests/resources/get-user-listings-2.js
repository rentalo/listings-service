const convert = require('./convert.js');

const payload = '';
const params = {};
const context = {
    authorizer: {
        claims: {
            sub: '6711ec07-e4d9-4097-a0fc-414748315989'
        }
    }
}
const filePath = 'templates/get_user_listings_request.vm';

console.info(convert(filePath, payload, params, context))