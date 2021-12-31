const convert = require('./convert.js');

const payload = JSON.stringify({
    "Items": [
        {
            "locationId": {
                "S": "gbsvh"
            },
            "listingId": {
                "S": "1d93bc1a-8037-4659-a523-4a77f4bb5b6c"
            },
            "isShared": {
                "BOOL": true
            },
            "depth": {
                "N": "4"
            },
            "isNegotiable": {
                "BOOL": false
            },
            "address": {
                "M": {
                    "street": {
                        "S": "Via Roma 123"
                    },
                    "city": {
                        "S": "Torino"
                    },
                    "state": {
                        "S": "TO"
                    },
                    "zip": {
                        "S": "12345"
                    },
                    "country": {
                        "S": "Italy"
                    }
                }
            },
            "email": {
                "S": "email@example.com"
            },
            "availability": {
                "M": {
                    "from": {
                        "S": "2018-01-01T00:00:00Z"
                    },
                    "to": {
                        "S": "2018-01-31T00:00:00Z"
                    }
                }
            },
            "photos": {
                "SS": [
                    "avMQpjqbGEzCCPuTZjTEJQ==",
                    "bvMQpjqbGEzCCPuTZjTEJQ=="
                ]
            },
            "height": {
                "N": "5"
            },
            "width": {
                "N": "6"
            },
            "category": {
                "S": "BOX"
            },
            "rent": {
                "N": "40"
            },
            "owner": {
                "S": "b5708bf5-dcec-4b5a-8d1f-9bfe985ecb79"
            },
            "description": {
                "S": "Example description"
            },
            "phone": {
                "S": "+393211234567"
            },
            "position": {
                "M": {
                    "latitude": {
                        "N": "46.076035"
                    },
                    "longitude": {
                        "N": "8.669416"
                    }
                }
            }
        }
    ]
});
const params = {};
const context = {}
const filePath = 'templates/get_listings_response.vm';

console.info(convert(filePath, payload, params, context))