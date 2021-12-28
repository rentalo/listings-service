# listings-service

### Open endpoints

- [Get listings (public)](#get-listings-public) - `GET /public/v1/listings/{geohash}`
- [Get a listing photo](#get-a-listing-photo) - `GET /v1/listing/photo/{hash}`

### Authenticated endpoints

- [Get listings (private)](#get-listings-private) - `GET /v1/listings/{geohash}`
- [Publish a listing](#publish-a-listing) - `PUT /v1/listing`
- [Get listing details](#get-listing-details) - `GET /v1/listing/{geohash}/{id}`
- [Delete a listing](#delete-a-listing) - `DELETE /v1/listing/{geohash}/{id}`
- [Publish a listing photo](#publish-a-listing-photo) - `PUT /v1/listing/photo`

### Endpoints details

#### Get listings (public)

Uri: `/public/v1/listings/{geohash}`

Method: `GET`

Description: `Get some listings in a region`

Path parameters:
- `geohash`

#### Get listings (private)

Uri: `/v1/listings/{geohash}`

Method: `GET`

Description: `Get listings in a region while applying some filters`

Path parameters:
- `geohash`

Query parameters:
- `category`
- `min_height`
- `min_width`
- `min_depth`
- `max_price`
- `is_shared`
- `from_date`
- `to_date`

#### Publish a listing

Uri: `/v1/listing`

Method: `PUT`

Description: `Publish or update a listing`

Sample body:
```json
{

  "id": "4c343850-13b3-41e1-974c-aaaa2c387444",
  "geohash": "gbsvh",
  "category": "BOX",
  "rent": 40,
  "address": "Via Roma 42, Genova, GE, 12345, Italia",
  "position": {
    "latitude": 45.076035, 
    "longitude": 7.669416
  },
  "height": 5,
  "width": 6,
  "depth": 4,
  "isNegotiable": false,
  "isShared": true,
  "photos": ["avMQpjqbGEzCCPuTZjTEJQ=="],
  "phone": "+393211234567",
  "description": "Esempio descrizione con dettagli particolari",
  "availability": {
    "from": "2018-01-01T00:00:00Z",
    "to": "2021-01-01T00:00:00Z"
  }

}
```

#### Get listing details

Uri: `/v1/listing/{geohash}/{id}`

Method: `GET`

Sample response:
```json
{

  "id": "4c343850-13b3-41e1-974c-aaaa2c387444",
  "geohash": "gbsvh",
  "category": "BOX",
  "rent": 40,
  "address": "Via Roma 42, Genova, GE, 12345, Italia",
  "position": {
    "latitude": 45.076035, 
    "longitude": 7.669416
  },
  "height": 5,
  "width": 6,
  "depth": 4,
  "isNegotiable": false,
  "isShared": true,
  "photos": ["avMQpjqbGEzCCPuTZjTEJQ=="],
  "email": "sample@email.com", 
  "phone": "+393211234567",
  "owner": "42e9b4da-f4c9-4f8f-93be-97fb7bec9bc5",
  "description": "Esempio descrizione con dettagli particolari",
  "availability": {
    "from": "2018-01-01T00:00:00Z",
    "to": "2021-01-01T00:00:00Z"
  }

}
```

#### Delete a listing

Uri: `/v1/listing/{geohash}/{id}`

Method: `DELETE`

#### Publish a listing photo

Uri: `/v1/listing/photo`

Method: `PUT`

Body:
- `hash`: Base64-encoded MD5 hash of base64-encoded image
- `base64`: Base64-encoded image

Sample body:
```json
{
  "hash": "eteFLxUBax1QDtrbBXiszQ==",
  "base64": "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"
}
```

#### Get a listing photo

Uri: `/v1/listing/photo/{hash}`

Method: `GET`

Description: `Get a listing photo by its hash`


### Testing

#### Requirements

- `localstack`
- `awslocal`
- `api-gateway-mapping-template`

#### Setup

1. Run localstack

    ```
    export USE_SINGLE_REGION=true; localstack start -d
    ```

2. Initialize resources

    ```
    awslocal dynamodb create-table --cli-input-json file://tests/init/listings-table.json
    awslocal s3 mb s3://listings-photos-bucket
    ```

#### Run

```
python -m unittest discover tests/
```