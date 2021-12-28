const convert = require('./convert.js');

const payload = '';
const params = {
    querystring: {
        geohash: '9q8yv0',
        category: 'CELLAR',
        max_rent: '100',
        min_width: '5',
        min_height: '3',
        min_depth: '6',
        is_shared: 'false',
        from_date: '2000-12-31',
        to_date: '2018-01-16'
    }
};
const context = {}
const filePath = 'templates/get_listings_request_private.vm';

console.info(convert(filePath, payload, params, context))