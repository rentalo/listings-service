const convert = require('./convert.js');

const payload = JSON.stringify({
    geohash: '9q8yy',
    id: '14572623-886b-47ba-9b23-13fb150fccdd',
    category: 'BOX',
    rent: '50',
    address: {
        street: 'Via Roma 123',
        city: 'Torino',
        state: 'TO',
        zip: '12345',
        country: 'Italy',
    },
    position: {
        latitude: '45.0',
        longitude: '8.0'
    },
    width: '3',
    height: '2',
    depth: '1',
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
            sub: '41906af2-1b81-4e15-b7d3-eda988fb4aeb',
            phone_number: '+393476543210',
            email: 'user@example.com'
        }
    }
}
const filePath = 'templates/put_listing_request.vm';

console.info(convert(filePath, payload, params, context))