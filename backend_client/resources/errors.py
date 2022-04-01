class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "missing required fields in the request",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "user with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "invalid username or password",
         "status": 401
     }
}