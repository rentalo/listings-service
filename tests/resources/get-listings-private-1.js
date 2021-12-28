const convert = require('./convert.js');

const payload = '';
const params = {
    querystring: {
        geohash: '9q8xj',
        category: 'CELLAR',
        max_rent: '100',
        min_width: '2',
        min_height: '3',
        min_depth: '4',
        is_shared: 'false',
        from_date: '2018-01-15',
        to_date: '2018-01-16'
    }
};
const context = {}
const filePath = 'templates/get_listings_request_private.vm';

console.info(convert(filePath, payload, params, context))