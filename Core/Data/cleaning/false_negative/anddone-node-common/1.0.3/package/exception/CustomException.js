

class InputValidationException extends Error {
  constructor(name, message) {

    const log = require('../index').Logger;
    super(message)
    // Ensure the name of this error is the same as the class name
    this.name = this.constructor.name;
    this.message = message
    Error.captureStackTrace(this, this.constructor);
  }
}
class AuthorizationException extends Error {
  constructor(message) {

    const log = require('../index').Logger;
    super(message)
    this.name = 'PermissionError'
    this.message = message
    //this.data = { name, message };
  }
}
class DatabaseException extends Error {
  constructor(name, message) {
    const log = require('../index').Logger;
    log.error('DatabaseException ' + message);
    super(name, message)
    this.name = name
    this.message = message
  }
}
module.exports = {
  InputValidationException,
  AuthorizationException,
  DatabaseException
}