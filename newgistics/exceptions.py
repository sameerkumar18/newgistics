# -*- coding: utf-8 -*-

"""
newgistics.exceptions
~~~~~~~~~~~~~~~~~~~~~

This module contains all the custom defined exceptions.
"""


class NewgisticsException(Exception):
    def __init__(self, message=None, response=None):
        super(NewgisticsException, self).__init__(message)
        if response:
            http_body = response.text
            http_status = response.status_code
            json_body = response.json()
            self.http_body = http_body
            self.http_status = http_status
            self.json_body = json_body


class ResourceEntityNotFound(NewgisticsException):
    pass


class InternalServerError(NewgisticsException):
    pass


class AccessNotGrantedError(NewgisticsException):
    pass


class AuthenticationParameterError(NewgisticsException):
    pass


class UnAuthorizedAccessError(NewgisticsException):
    pass


class IncorrectParameterError(NewgisticsException):
    pass


class RequiredParameterMissing(NewgisticsException):
    pass


class InvalidFormat(NewgisticsException):
    pass


class InvalidAccessType(NewgisticsException):
    pass
