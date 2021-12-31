const convert = require('./convert.js');

const payload = JSON.stringify({
    geohash: '9q8yv0',
    id: '3a83bd23-b1ec-40f8-a727-8b1393ddf41b',
    category: 'BOX',
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
            sub: 'b989e224-6c93-48f3-80b2-fa5ee5f6db81',
            phone_number: '+393476543210',
            email: 'user@example.com'
        }
    }
}
const filePath = 'templates/put_listing_request.vm';

console.info(convert(filePath, payload, params, context))