const convert = require('./convert.js');

const payload = JSON.stringify({
    geohash: '9q8yv0',
    id: '83fa260d-15e7-4e71-9053-6d287cdc30d8',
    category: 'CELLAR',
    rent: '60',
    address: 'Piazza Rivoli 123, Genova, GE, 12345, Italia',
    position: {
        latitude: '46.0',
        longitude: '7.0'
    },
    width: '6',
    height: '4',
    depth: '5',
    isNegotiable: 'true',
    isShared: 'false',
    phone: '+39123456789',
    email: 'user@example.com',
    photos: ['photo1', 'photo2'],
    description: 'Some description about this listing',
    availability: {
        from: '2018-01-01',
        to: '2018-02-28'
    }
});
const params = {};
const context = {
    authorizer: {
        claims: {
            sub: 'af93332f-ce76-41de-979e-9151c5518456',
            phone_number: '+393476543210',
            email: 'user@example.com'
        }
    }
}
const filePath = 'templates/put_listing_request.vm';

console.info(convert(filePath, payload, params, context))