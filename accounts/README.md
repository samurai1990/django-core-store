# Accounting App API Document
## Claim Token APIs
### Create Account
* permission: `null`

* endpoint: `/users/`

* HTTP method: `POST`

* request:
```json
{
  "username":"myusername",
  "email":"myemail@example.com",
  "password":"mypassword"
}
```
* ok response

  HTTP status code: `201`
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "user": { "id": "e035f750-5dfe-4b87-a8ad-ff907aa7523a",
              "username": "testuser",
              "email": "test@example.com",
              "is_active": true,
              "is_superuser": false,
              "profile": {},
              "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJfaWQiOiJlMDM1Zjc1MC01ZGZlLTRiODctYThhZC1mZjkwN2FhNzUyM2EifX0.Nl8ioe4fqrosgJ4M7ifXQPCSNPyUV8L-cquPL4zPmjA"
            }
        }
}
```
* duplicate user response:

  HTTP status code: `400`
```json
{
  "err": true, "err_code": 9, "err_msg": "User is already exists", "data": {}
}
```
### Signin
* permission: `null`

* endpoint: `/users/signin/`

* HTTP method: `POST`

* request:
```json
{
    "username":"myusername",
    "password":"mypassword"
}
```
* ok response:

  HTTP status code: `200`
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "user": { "id": "e035f750-5dfe-4b87-a8ad-ff907aa7523a",
              "username": "testuser",
              "email": "test@example.com",
              "is_active": true,
              "is_superuser": false,
              "profile": {},
              "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJfaWQiOiJlMDM1Zjc1MC01ZGZlLTRiODctYThhZC1mZjkwN2FhNzUyM2EifX0.Nl8ioe4fqrosgJ4M7ifXQPCSNPyUV8L-cquPL4zPmjA"
            }
        }
}
```
* non existence user

  HTTP status code: `404`
```json
{"err": true, "err_code": 3, "err_msg": "User not found", "data": {}}
```

* wrong password

  HTTP status code: `401`
```json
{"err": true, "err_code": 6, "err_msg": "Invalid Credentials", "data": {}}
```

## Protected Requests
all protected requests must have `Authorization` header with `token` raelm
```
Authorization: token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7InVzZXJfaWQiOiJlMDM1Zjc1MC01ZGZlLTRiODctYThhZC1mZjkwN2FhNzUyM2EifX0.Nl8ioe4fqrosgJ4M7ifXQPCSNPyUV8L-cquPL4zPmjA
```
OR
all protected requests must have `http` header with `Api-Key` field.
```
Api-Key: e54f0267-fa92-43af-bfc0-50f10ebba781
```

### Unauthorize Responses
* Invalid raelm

  HTTP status code: `403`
  ```json
  {"err": true, "err_code": 4, "err_msg": "raelm {raelm} is not valid", "data": {}}
  ```
* Malformed token

  HTTP status code: `403`
  ```json
  {"err": true, "err_code": 4, "err_msg": "malformed token", "data": {}}
  ```
* Expired token

  HTTP status code: `403`
  ```json
  {"err": true, "err_code": 4, "err_msg": "token has expired. try to re-authenticate", "data": {}}
  ```
* Not valid token

  HTTP status code: `403`
  ```json
  {"err": true, "err_code": 4, "err_msg": "not a valid token. try to re-authenticate", "data": {}}
  ```
* Banned user
  HTTP status code: `403`
  ```json
  {"err": true, "err_code": 4, "err_msg": "Your account has been inactive for 2 hours. If you have an emergency contact administrator", "data": {}}
  ```

### Signout
* permission: `Authenticated or null`

* endpoint: `/users/signout`

* HTTP method: `GET`

* ok response:
```json
{"err": false, "err_code": 0, "err_msg": null, "data": {}}
```

### List users
* permission: `Admin`

* endpoint: `/users/`

* HTTP method: `GET`

* query params: `is_active`, `is_deleted`, `is_superuser`

* ok response:
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "page": {
            "next": null,
            "previous": null,
            "current": 1,
            "count": 12,
            "total_pages": 1
        },
        "users": [
            {
                "id": "96fbf793-9190-44db-91a3-b9b33484b548",
                "username": "testuser9",
                "email": "testuser9@example.com",
                "is_active": false,
                "is_superuser": false,
                "last_login": null,
                "is_deleted": false,
                "created": "2022-12-07T14:41:52.002409Z"
            },
            {
                "id": "ad4d5a1e-b027-456c-b46e-a17cb39cab4f",
                "username": "testuser8",
                "email": "testuser8@example.com",
                "is_active": true,
                "is_superuser": true,
                "last_login": null,
                "is_deleted": false,
                "created": "2022-12-07T14:41:51.858960Z"
            },
            {
                "id": "8693f59a-8b8f-44a3-a2e4-841960cf88e4",
                "username": "testuser7",
                "email": "testuser7@example.com",
                "is_active": false,
                "is_superuser": false,
                "last_login": null,
                "is_deleted": false,
                "created": "2022-12-07T14:41:51.713314Z"
            }
        ]
    }
}
```

### Retrieve a user
* permission: `Admin`

* endpoint: `/users/<id>/`

* HTTP method: `GET`

* ok response:
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "user": { "id": "e035f750-5dfe-4b87-a8ad-ff907aa7523a",
              "username": "testuser",
              "email": "test@example.com",
              "is_active": true,
              "is_superuser": false,
              "profile": {},
            }
        }
}
```
### User profile
* permission: `IsAuthenticatedAndOwner`

* endpoint: `/users/profile/`

* HTTP method: `GET`

* ok response:
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "user": { "id": "e035f750-5dfe-4b87-a8ad-ff907aa7523a",
              "username": "testuser",
              "email": "test@example.com",
              "profile": {},
            }
        }
}
```

### User Update
* permission: `IsAuthenticatedAndOwner`

* endpoint: `/users/<id>/`

* HTTP method: `PUT`
* requests
```json
{         
  "id": "e035f750-5dfe-4b87-a8ad-ff907aa7523a",
  "username": "testuser",
  "email": "test@example.com",
  "profile": {},
}
```
* ok response:
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "user": { "id": "e035f750-5dfe-4b87-a8ad-ff907aa7523a",
              "username": "testuser",
              "email": "test@example.com",
              "profile": {},
            }
        }
}
```

### Active, Promote & Delete User
* permission: `Admin`

* endpoint: `/users/<id>/`

* HTTP method: `PATCH`
* requests
```json
{         
  "is_active": true,
  "is_deleted": false,
  "is_superuser": false,
  "failed_login_tries": 0
}
```
* ok response:
```json
{
  "err": false,
  "err_code": 0,
  "err_msg": null,
  "data": {
    "user": {
              "is_active": true,
              "is_deleted": false,
              "is_superuser": false,
              "failed_login_tries": 0
            }
        }
}
```

### Delete User
* permission: `IsAuthenticatedAndOwner`

* endpoint: `/users/<id>/`

* HTTP method: `DELETE`

* ok response status code: `204`
