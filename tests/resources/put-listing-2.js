const convert = require('./convert.js');

const payload = JSON.stringify({
    geohash: '9q8xj',
    id: 'cd8513e1-5cf0-4375-accd-71d51a0f83aa',
    category: 'CELLAR',
    rent: '60',
    address: {
        street: 'Via Roma 123',
        city: 'Torino',
        state: 'TO',
        zip: '12345',
        country: 'Italy',
    },
    position: {
        latitude: '46.0',
        longitude: '7.0'
    },
    width: '5',
    height: '4',
    depth: '6',
    isNegotiable: 'true',
    isShared: 'false',
    phone: '+39123456789',
    email: 'user@example.com',
    photos: ['photo1', 'photo2'],
    description: 'Some description about this listing',
    availability: {
        from: '2018-01-01',
        to: '2018-01-31'
    }
});
const params = {};
const context = {
    authorizer: {
        claims: {
            sub: 'eab735b5-efb4-4a15-a963-10aac80f1d71',
            phone_number: '+393476543210',
            email: 'user@example.com'
        }
    }
}
const filePath = 'templates/put_listing_request.vm';

console.info(convert(filePath, payload, params, context))