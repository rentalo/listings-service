const convert = require('./convert.js');

const payload = '';
const params = {};
const context = {
    authorizer: {
        claims: {
            sub: 'b989e224-6c93-48f3-80b2-fa5ee5f6db81'
        }
    }
}
const filePath = 'templates/get_user_listings_request.vm';

console.info(convert(filePath, payload, params, context))