API - Helps two applications to communicate with each other

GET /api/ / GET ALL OR GET BY ID
POST /api
PATCH /api
DELETE /api
PUT /api

HTTP REQUESTS DO NOT REQUIRE ID => GET all AND POST

HTTP REQUESTS THAT REQUIRE ID => GET BY ID, DELETE, AND PATCH

example: users
 GET /api/users
 POST /api/users

 GET /api/users/<int:id>
 DELETE /api/users/<int:id>
 PATCH /api/users/<int:id>


<!-- AUTHENTICATION AND AUTHORIZATION -->
JWT Authentication

SETUP AUTH => install, secret key, initialize it with our app

<!-- Login -->
create access token and refresh token

protecting the Api endpoints

handle some jwt authentication errors

logout 


