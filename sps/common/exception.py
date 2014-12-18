# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""sps exception subclasses"""

import six
import six.moves.urllib.parse as urlparse
from sps.openstack.common.gettextutils import _

_FATAL_EXCEPTION_FORMAT_ERRORS = False


class RedirectException(Exception):
    def __init__(self, url):
        self.url = urlparse.urlparse(url)


class spsException(Exception):
    """
    Base sps Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = _("An unknown exception occurred")

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = self.message
        try:
            if kwargs:
                message = message % kwargs
        except Exception:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                # at least get the core message out if something happened
                pass
        self.msg = message
        super(spsException, self).__init__(message)

    def __unicode__(self):
        # NOTE(flwang): By default, self.msg is an instance of Message, which
        # can't be converted by str(). Based on the definition of
        # __unicode__, it should return unicode always.
        return six.text_type(self.msg)


class MissingCredentialError(spsException):
    message = _("Missing required credential: %(required)s")


class BadAuthStrategy(spsException):
    message = _("Incorrect auth strategy, expected \"%(expected)s\" but "
                "received \"%(received)s\"")


class NotFound(spsException):
    message = _("An object with the specified identifier was not found.")


class UnknownScheme(spsException):
    message = _("Unknown scheme '%(scheme)s' found in URI")


class BadStoreUri(spsException):
    message = _("The Store URI was malformed.")


class Duplicate(spsException):
    message = _("An object with the same identifier already exists.")


class Conflict(spsException):
    message = _("An object with the same identifier is currently being "
                "operated on.")


class StorageFull(spsException):
    message = _("There is not enough disk space on the image storage media.")


class StorageQuotaFull(spsException):
    message = _("The size of the data %(image_size)s will exceed the limit. "
                "%(remaining)s bytes remaining.")


class StorageWriteDenied(spsException):
    message = _("Permission to write image storage media denied.")


class AuthBadRequest(spsException):
    message = _("Connect error/bad request to Auth service at URL %(url)s.")


class AuthUrlNotFound(spsException):
    message = _("Auth service at URL %(url)s not found.")


class AuthorizationFailure(spsException):
    message = _("Authorization failed.")


class NotAuthenticated(spsException):
    message = _("You are not authenticated.")


class Forbidden(spsException):
    message = _("You are not authorized to complete this action.")


class ForbiddenPublicImage(Forbidden):
    message = _("You are not authorized to complete this action.")


class ProtectedImageDelete(Forbidden):
    message = _("Image %(image_id)s is protected and cannot be deleted.")


class Invalid(spsException):
    message = _("Data supplied was not valid.")


class InvalidSortKey(Invalid):
    message = _("Sort key supplied was not valid.")


class InvalidPropertyProtectionConfiguration(Invalid):
    message = _("Invalid configuration in property protection file.")


class InvalidFilterRangeValue(Invalid):
    message = _("Unable to filter using the specified range.")


class ReadonlyProperty(Forbidden):
    message = _("Attribute '%(property)s' is read-only.")


class ReservedProperty(Forbidden):
    message = _("Attribute '%(property)s' is reserved.")


class AuthorizationRedirect(spsException):
    message = _("Redirecting to %(uri)s for authorization.")


class ClientConnectionError(spsException):
    message = _("There was an error connecting to a server")


class ClientConfigurationError(spsException):
    message = _("There was an error configuring the client.")


class MultipleChoices(spsException):
    message = _("The request returned a 302 Multiple Choices. This generally "
                "means that you have not included a version indicator in a "
                "request URI.\n\nThe body of response returned:\n%(body)s")


class LimitExceeded(spsException):
    message = _("The request returned a 413 Request Entity Too Large. This "
                "generally means that rate limiting or a quota threshold was "
                "breached.\n\nThe response body:\n%(body)s")

    def __init__(self, *args, **kwargs):
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)
        super(LimitExceeded, self).__init__(*args, **kwargs)


class ServiceUnavailable(spsException):
    message = _("The request returned 503 Service Unavilable. This "
                "generally occurs on service overload or other transient "
                "outage.")

    def __init__(self, *args, **kwargs):
        self.retry_after = (int(kwargs['retry']) if kwargs.get('retry')
                            else None)
        super(ServiceUnavailable, self).__init__(*args, **kwargs)


class ServerError(spsException):
    message = _("The request returned 500 Internal Server Error.")


class UnexpectedStatus(spsException):
    message = _("The request returned an unexpected status: %(status)s."
                "\n\nThe response body:\n%(body)s")


class InvalidContentType(spsException):
    message = _("Invalid content type %(content_type)s")


class BadRegistryConnectionConfiguration(spsException):
    message = _("Registry was not configured correctly on API server. "
                "Reason: %(reason)s")


class BadStoreConfiguration(spsException):
    message = _("Store %(store_name)s could not be configured correctly. "
                "Reason: %(reason)s")


class BadDriverConfiguration(spsException):
    message = _("Driver %(driver_name)s could not be configured correctly. "
                "Reason: %(reason)s")


class StoreDeleteNotSupported(spsException):
    message = _("Deleting demos from this store is not supported.")


class StoreGetNotSupported(spsException):
    message = _("Getting demos from this store is not supported.")


class StoreAddNotSupported(spsException):
    message = _("Adding demos to this store is not supported.")


class StoreAddDisabled(spsException):
    message = _("Configuration for store failed. Adding demos to this "
                "store is disabled.")


class MaxRedirectsExceeded(spsException):
    message = _("Maximum redirects (%(redirects)s) was exceeded.")


class InvalidRedirect(spsException):
    message = _("Received invalid HTTP redirect.")


class NoServiceEndpoint(spsException):
    message = _("Response from Keystone does not contain a sps endpoint.")


class RegionAmbiguity(spsException):
    message = _("Multiple 'image' service matches for region %(region)s. This "
                "generally means that a region is required and you have not "
                "supplied one.")


class WorkerCreationFailure(spsException):
    message = _("Server worker creation failed: %(reason)s.")


class SchemaLoadError(spsException):
    message = _("Unable to load schema: %(reason)s")


class InvalidObject(spsException):
    message = _("Provided object does not match schema "
                "'%(schema)s': %(reason)s")


class UnsupportedHeaderFeature(spsException):
    message = _("Provided header feature is unsupported: %(feature)s")


class InUseByStore(spsException):
    message = _("The image cannot be deleted because it is in use through "
                "the backend store outside of sps.")


class demosizeLimitExceeded(spsException):
    message = _("The provided image is too large.")


class ImageMemberLimitExceeded(LimitExceeded):
    message = _("The limit has been exceeded on the number of allowed image "
                "members for this image. Attempted: %(attempted)s, "
                "Maximum: %(maximum)s")


class ImagePropertyLimitExceeded(LimitExceeded):
    message = _("The limit has been exceeded on the number of allowed image "
                "properties. Attempted: %(attempted)s, Maximum: %(maximum)s")


class ImageTagLimitExceeded(LimitExceeded):
    message = _("The limit has been exceeded on the number of allowed image "
                "tags. Attempted: %(attempted)s, Maximum: %(maximum)s")


class ImageLocationLimitExceeded(LimitExceeded):
    message = _("The limit has been exceeded on the number of allowed image "
                "locations. Attempted: %(attempted)s, Maximum: %(maximum)s")


class RPCError(spsException):
    message = _("%(cls)s exception was raised in the last rpc call: %(val)s")


class TaskException(spsException):
    message = _("An unknown task exception occurred")


class TaskNotFound(TaskException, NotFound):
    message = _("Task with the given id %(task_id)s was not found")


class InvalidTaskStatus(TaskException, Invalid):
    message = _("Provided status of task is unsupported: %(status)s")


class InvalidTaskType(TaskException, Invalid):
    message = _("Provided type of task is unsupported: %(type)s")


class InvalidTaskStatusTransition(TaskException, Invalid):
    message = _("Status transition from %(cur_status)s to"
                " %(new_status)s is not allowed")


class DuplicateLocation(Duplicate):
    message = _("The location %(location)s already exists")


class ImageDataNotFound(NotFound):
    message = _("No image data could be found")


class InvalidParameterValue(Invalid):
    message = _("Invalid value '%(value)s' for parameter '%(param)s': "
                "%(extra_msg)s")


class InvaliddemostatusTransition(Invalid):
    message = _("Image status transition from %(cur_status)s to"
                " %(new_status)s is not allowed")

class DemoNotFound(NotFound):
    msg_fmt = _("Demo %(id)s not found.")

class DemoCanNotUpdatate(spsException):
    message = _("Demo %(id)s can not updatate.")

class DemoCanNotDelete(spsException):
    message = _("Demo %(id)s can not delete.")

class DemoCanNotAdd(spsException):
    message = _("Demo %(id)s can not add.")