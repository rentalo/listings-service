from aws_cdk import (
    core as cdk,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_s3 as s3
)


class ListingsServiceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, user_pool_arn: str, **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        # DATABASE------------------------------------------------------------------------------------------------------

        listings_table = dynamodb.Table(
            self, "ListingsTable",
            table_name="ListingsTable",
            partition_key=dynamodb.Attribute(name="locationId", type=dynamodb.AttributeType.STRING),                    # Identifies a location (geohash)
            sort_key=dynamodb.Attribute(name="listingId", type=dynamodb.AttributeType.STRING),                          # Identifies a listing at a location
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,                                                          # On demand pricing and scaling
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        listings_table.add_global_secondary_index(
            index_name="ListingCategoryIndex",
            partition_key=dynamodb.Attribute(name="category", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="rent", type=dynamodb.AttributeType.NUMBER),
            projection_type=dynamodb.ProjectionType.ALL
        )

        # BUCKET--------------------------------------------------------------------------------------------------------

        listings_photos_bucket = s3.Bucket(
            self, "ListingsPhotosBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # API-----------------------------------------------------------------------------------------------------------

        listings_api = apigateway.RestApi(
            self, "ListingsApi",
            rest_api_name="ListingsApi",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=["*"],
                allow_methods=["GET", "PUT", "DELETE", "OPTIONS"],
                allow_headers=["*"]
            ),
            cloud_watch_role=True,
            binary_media_types=["image/jpeg"]                                                                           # Allow binary content handling for these types
        )

        # INTEGRATIONS ROLES--------------------------------------------------------------------------------------------

        dynamodb_integration_policy = iam.Policy(
            self, "DynamoDbIntegrationPolicy",
            policy_name="DynamoDbIntegrationPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=["dynamodb:*"],
                    effect=iam.Effect.ALLOW,
                    resources=[
                        listings_table.table_arn,                                                                       # Grant permissions on table
                        listings_table.table_arn + "/index/*"                                                           # Grant permissions also on indices
                    ]
                )
            ]
        )
        dynamodb_integration_role = iam.Role(
            self, "DynamoDbIntegrationRole",
            role_name="DynamoDbIntegrationRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com")
        )
        dynamodb_integration_role.attach_inline_policy(policy=dynamodb_integration_policy)

        s3_integration_policy = iam.Policy(
            self, "S3IntegrationPolicy",
            policy_name="S3IntegrationPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=["s3:*"],
                    effect=iam.Effect.ALLOW,
                    resources=[
                        listings_photos_bucket.bucket_arn,                                                              # Grant permissions on bucket
                        listings_photos_bucket.bucket_arn + "/*"                                                        # Grant permissions also on objects
                    ]
                )
            ]
        )
        s3_integration_role = iam.Role(
            self, "S3IntegrationRole",
            role_name="S3IntegrationRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com")
        )
        s3_integration_role.attach_inline_policy(policy=s3_integration_policy)

        # INTEGRATIONS--------------------------------------------------------------------------------------------------

        # Query listings integration (private)
        with open("templates/get_listings_request_private.vm") as request_template, \
             open("templates/get_listings_response.vm") as response_template:
            private_query_integration = apigateway.AwsIntegration(
                service="dynamodb",
                action="Query",
                options=apigateway.IntegrationOptions(
                    passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                    credentials_role=dynamodb_integration_role,
                    request_parameters={
                        "integration.request.path.geohash": "method.request.path.geohash",
                        "integration.request.querystring.category": "method.request.querystring.category",
                        "integration.request.querystring.max_price": "method.request.querystring.max_price",
                        "integration.request.querystring.min_width": "method.request.querystring.min_width",
                        "integration.request.querystring.min_height": "method.request.querystring.min_height",
                        "integration.request.querystring.min_depth": "method.request.querystring.min_depth",
                        "integration.request.querystring.is_shared": "method.request.querystring.is_shared",
                    },
                    request_templates={"application/json": request_template.read()},
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={"application/json": response_template.read()}
                        ),
                        apigateway.IntegrationResponse(
                            status_code="400",
                            selection_pattern="^4[0-9][0-9]$",
                            response_templates={"application/json": "{}"}
                        )
                    ]
                )
            )

        # Query listings integration (public)
        with open("templates/get_listings_request_public.vm") as request_template, \
             open("templates/get_listings_response.vm") as response_template:
            public_query_integration = apigateway.AwsIntegration(
                service="dynamodb",
                action="Query",
                options=apigateway.IntegrationOptions(
                    passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                    credentials_role=dynamodb_integration_role,
                    request_parameters={
                        "integration.request.path.geohash": "method.request.path.geohash"
                    },
                    request_templates={"application/json": request_template.read()},
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={"application/json": response_template.read()}
                        ),
                        apigateway.IntegrationResponse(
                            status_code="400",
                            selection_pattern="^4[0-9][0-9]$",
                            response_templates={"application/json": "{}"}
                        )
                    ]
                )
            )

        # Put listing integration
        with open("templates/put_listing_request.vm") as request_template:
            put_listing_integration = apigateway.AwsIntegration(
                service="dynamodb",
                action="PutItem",
                options=apigateway.IntegrationOptions(
                    passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                    credentials_role=dynamodb_integration_role,
                    request_templates={"application/json": request_template.read()},
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={"application/json": "{}"}
                        ),
                        apigateway.IntegrationResponse(
                            status_code="400",
                            selection_pattern="^4[0-9][0-9]$",
                            response_templates={"application/json": "{}"}
                        )
                    ]
                )
            )

        # Get listing integration
        with open("templates/get_listing_request.vm") as request_template, \
             open("templates/get_listing_response.vm") as response_template:
            get_listing_integration = apigateway.AwsIntegration(
                service="dynamodb",
                action="GetItem",
                options=apigateway.IntegrationOptions(
                    passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                    credentials_role=dynamodb_integration_role,
                    request_parameters={
                        "integration.request.path.geohash": "method.request.path.geohash",
                        "integration.request.path.id": "method.request.path.id"
                    },
                    request_templates={"application/json": request_template.read()},
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={"application/json": response_template.read()}
                        ),
                        apigateway.IntegrationResponse(
                            status_code="400",
                            selection_pattern="^4[0-9][0-9]$",
                            response_templates={"application/json": "{}"}
                        )
                    ]
                )
            )

        # Delete listing integration
        with open("templates/delete_listing_request.vm") as request_template:
            delete_listing_integration = apigateway.AwsIntegration(
                service="dynamodb",
                action="DeleteItem",
                options=apigateway.IntegrationOptions(
                    passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                    credentials_role=dynamodb_integration_role,
                    request_parameters={
                        "integration.request.path.geohash": "method.request.path.geohash",
                        "integration.request.path.id": "method.request.path.id"
                    },
                    request_templates={"application/json": request_template.read()},
                    integration_responses=[
                        apigateway.IntegrationResponse(
                            status_code="200",
                            response_templates={"application/json": "{}"}
                        ),
                        apigateway.IntegrationResponse(
                            status_code="400",
                            selection_pattern="^4[0-9][0-9]$",
                            response_templates={"application/json": "{}"}
                        )
                    ]
                )
            )

        # Put listing photo integration
        put_listing_photo_integration = apigateway.AwsIntegration(
            service="s3",
            integration_http_method="PUT",
            path="{}/{{hash}}".format(listings_photos_bucket.bucket_name),
            options=apigateway.IntegrationOptions(
                passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                credentials_role=s3_integration_role,
                request_parameters={
                    "integration.request.path.hash": "method.request.body.hash",
                    "integration.request.header.Content-Type": "'image/jpeg+base64'",                                   # Objects are base64 encoded images
                    "integration.request.header.Content-MD5": "method.request.body.hash"                                # Enforce integrity: object name must match object hash
                },
                request_templates={
                    "application/json": "$input.path('$.base64')"                                                       # Store base64 encoded image
                },
                integration_responses=[
                    apigateway.IntegrationResponse(
                        status_code="200",
                        selection_pattern="200",
                        response_templates={"application/json": "{}"}
                    ),
                    apigateway.IntegrationResponse(
                        status_code="400",
                        selection_pattern="^4[0-9][0-9]$",
                        response_templates={"application/json": "{}"}
                    )
                ]
            )
        )

        # Get listing photo integration
        get_listing_photo_integration = apigateway.AwsIntegration(
            service="s3",
            integration_http_method="GET",
            path="{}/{{hash}}".format(listings_photos_bucket.bucket_name),
            options=apigateway.IntegrationOptions(
                credentials_role=s3_integration_role,
                request_parameters={
                    "integration.request.path.hash": "method.request.path.hash",
                    "integration.request.header.Accept": "'image/jpeg'"
                },
                integration_responses=[
                    apigateway.IntegrationResponse(
                        status_code="200",
                        selection_pattern="200",
                        content_handling=apigateway.ContentHandling.CONVERT_TO_BINARY                                   # Convert stored base64 image to binary
                    ),
                    apigateway.IntegrationResponse(
                        status_code="400",
                        selection_pattern="^4[0-9][0-9]$",
                        response_templates={"application/json": "{}"}
                    )
                ]
            )
        )

        # AUTHORIZATION-------------------------------------------------------------------------------------------------

        publishers_user_pool = cognito.UserPool.from_user_pool_arn(
            self, "PublishersUserPool",
            user_pool_arn=user_pool_arn
        )
        listings_api_authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "ListingsApiAuthorizer",
            authorizer_name="ListingsApiAuthorizer",
            identity_source="method.request.header.Authorization",                                                      # Authorization must be passed on this header
            cognito_user_pools=[publishers_user_pool]
        )

        # RESOURCES-----------------------------------------------------------------------------------------------------

        public = listings_api.root.add_resource(path_part="public")                                                     # /public
        public_v1 = public.add_resource(path_part="v1")                                                                 # /public/v1
        public_v1_listings = public_v1.add_resource(path_part="listings")                                               # /public/v1/listings
        public_v1_listings_geohash = public_v1_listings.add_resource(path_part="{geohash}")                             # /public/v1/listings/{geohash}
        v1 = listings_api.root.add_resource(path_part="v1")                                                             # /v1
        v1_listings = v1.add_resource(path_part="listings")                                                             # /v1/listings
        v1_listings_geohash = v1_listings.add_resource(path_part="{geohash}")                                           # /v1/listings/{geohash}
        v1_listing = v1.add_resource(path_part="listing")                                                               # /v1/listing
        v1_listing_photo = v1_listing.add_resource(path_part="photo")                                                   # /v1/listing/photo
        v1_listing_photo_hash = v1_listing_photo.add_resource(path_part="{hash}")                                       # /v1/listing/photo/{hash}
        v1_listing_geohash = v1_listing.add_resource(path_part="{geohash}")                                             # /v1/listing/{geohash}
        v1_listing_geohash_id = v1_listing_geohash.add_resource(path_part="{id}")                                       # /v1/listing/{geohash}/{id}

        # MODELS--------------------------------------------------------------------------------------------------------

        put_listing_photo_request_model = apigateway.Model(
            self, "PutListingPhotoRequestModel",
            model_name="PutListingPhotoRequestModel",
            rest_api=listings_api,
            content_type="application/json",
            schema=apigateway.JsonSchema(
                type=apigateway.JsonSchemaType.OBJECT,
                required=["hash", "base64"],
                properties={
                    "hash": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                        pattern="^[A-Za-z0-9\\+\\/]{22}==$",
                        description="Base64 encoded hash of base64 encoded image"
                    ),
                    "base64": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                        max_length=1_048_576,
                        pattern="^[A-Za-z0-9\\+\\/]+[=]{1,2}$",
                        description="Base64 encoded image"
                    )
                }
            )
        )

        put_listing_request_model = apigateway.Model(
            self, "PutListingRequestModel",
            model_name="PutListingRequestModel",
            rest_api=listings_api,
            content_type="application/json",
            schema=apigateway.JsonSchema(
                type=apigateway.JsonSchemaType.OBJECT,
                required=[
                    "id", "geohash", "category", "rent", "address", "position", "width", "height", "depth",
                    "isNegotiable", "isShared", "photos", "phone"
                ],
                properties={
                    "id": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"                        # Match only UUIDs
                    ),
                    "geohash": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                        pattern="^[0-9b-hj-km-np-z]{5}$"                                                                # Match only Geohash alphabet strings
                    ),
                    "category": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                        enum=["BOX", "CELLAR"]
                    ),
                    "rent": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.NUMBER,
                        minimum=0, maximum=9999
                    ),
                    "address": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,                                                          # Match only this format:
                        pattern="^[a-zA-Z'\\s]+[\\d]+([/][A-Z]+)?, [a-zA-Z]+, [A-Z]{2}, [0-9]{5}, [a-zA-Z]+$"           # Via Roma 123, Torino, TO, 12345, Italy
                    ),
                    "position": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.OBJECT,
                        properties={
                            "latitude": apigateway.JsonSchema(
                                type=apigateway.JsonSchemaType.NUMBER,
                                minimum=-90, maximum=90
                            ),
                            "longitude": apigateway.JsonSchema(
                                type=apigateway.JsonSchemaType.NUMBER,
                                minimum=-180, maximum=180
                            )
                        }
                    ),
                    "width": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.NUMBER,
                        minimum=0, maximum=99
                    ),
                    "height": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.NUMBER,
                        minimum=0, maximum=99
                    ),
                    "depth": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.NUMBER,
                        minimum=0, maximum=99
                    ),
                    "isNegotiable": apigateway.JsonSchema(type=apigateway.JsonSchemaType.BOOLEAN),
                    "isShared": apigateway.JsonSchema(type=apigateway.JsonSchemaType.BOOLEAN),
                    "photos": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.ARRAY,
                        min_length=1,
                        items=apigateway.JsonSchema(
                            type=apigateway.JsonSchemaType.STRING,
                            pattern="^[A-Za-z0-9\\+\\/]{22}==$"                                                         # Match only base64 encoded hashes
                        )
                    ),
                    "phone": apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                        pattern="^\\+39[0-9]{10}$"                                                                      # Match only italian phone numbers
                    )
                }
            )
        )

        # METHODS-------------------------------------------------------------------------------------------------------

        v1_listings_geohash.add_method(
            http_method="GET",
            integration=private_query_integration,
            request_parameters={
                "method.request.path.geohash": True,
                "method.request.querystring.category": False,
                "method.request.querystring.min_width": False,
                "method.request.querystring.min_height": False,
                "method.request.querystring.min_depth": False,
                "method.request.querystring.max_price": False,
                "method.request.querystring.is_shared": False,
            },
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ],
            authorizer=listings_api_authorizer
        )

        v1_listing.add_method(
            http_method="PUT",
            integration=put_listing_integration,
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ],
            request_validator=apigateway.RequestValidator(
                self, "PutListingRequestValidator",
                request_validator_name="PutListingRequestValidator",
                rest_api=listings_api,
                validate_request_body=True
            ),
            request_models={
                "application/json": put_listing_request_model
            },
            authorizer=listings_api_authorizer
        )

        v1_listing_photo.add_method(
            http_method="PUT",
            integration=put_listing_photo_integration,
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ],
            request_validator=apigateway.RequestValidator(
                self, "PutListingPhotoRequestValidator",
                request_validator_name="PutListingPhotoRequestValidator",
                rest_api=listings_api,
                validate_request_body=True
            ),
            request_models={
                "application/json": put_listing_photo_request_model
            },
            authorizer=listings_api_authorizer
        )

        v1_listing_photo_hash.add_method(
            http_method="GET",
            integration=get_listing_photo_integration,
            request_parameters={
                "method.request.path.hash": True
            },
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ],
            authorizer=listings_api_authorizer
        )

        v1_listing_geohash_id.add_method(
            http_method="GET",
            integration=get_listing_integration,
            request_parameters={
                "method.request.path.geohash": True,
                "method.request.path.id": True
            },
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ],
            authorizer=listings_api_authorizer
        )

        v1_listing_geohash_id.add_method(
            http_method="DELETE",
            integration=delete_listing_integration,
            request_parameters={
                "method.request.path.geohash": True,
                "method.request.path.id": True
            },
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ],
            authorizer=listings_api_authorizer
        )

        public_v1_listings_geohash.add_method(
            http_method="GET",
            integration=public_query_integration,
            request_parameters={
                "method.request.path.geohash": True
            },
            method_responses=[
                apigateway.MethodResponse(status_code="200"),
                apigateway.MethodResponse(status_code="400")
            ]
        )