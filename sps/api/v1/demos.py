# Copyright 2013 OpenStack Foundation
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

"""
/demos endpoint for sps v1 API
"""

import copy

import eventlet
import json
from oslo.config import cfg
import six.moves.urllib.parse as urlparse
from webob.exc import HTTPBadRequest
from webob.exc import HTTPConflict
from webob.exc import HTTPForbidden
from webob.exc import HTTPMethodNotAllowed
from webob.exc import HTTPNotFound
from webob.exc import HTTPRequestEntityTooLarge
from webob import Response

from sps.api import policy
import sps.api.v1
import sps.db
from sps.api.v1 import controller
from sps.common import exception
from sps.common import property_utils
from sps.common import wsgi
from sps import notifier
import sps.openstack.common.log as logging
from sps.openstack.common import strutils



LOG = logging.getLogger(__name__)
SUPPORTED_PARAMS = sps.api.v1.SUPPORTED_PARAMS
SUPPORTED_FILTERS = sps.api.v1.SUPPORTED_FILTERS
ACTIVE_IMMUTABLE = sps.api.v1.ACTIVE_IMMUTABLE

CONF = cfg.CONF
CONF.import_opt('image_property_quota', 'sps.common.config')

class Controller(controller.BaseController):
    """
    WSGI controller for demos resource in sps v1 API

    The demos resource API is a RESTful web service for image data. The API
    is as follows::

        GET /demos -- Returns a set of brief metadata about demos
        GET /demos/detail -- Returns a set of detailed metadata about
                              demos
        HEAD /demos/<ID> -- Return metadata about an image with id <ID>
        GET /demos/<ID> -- Return image data for image with id <ID>
        POST /demos -- Store image data and return metadata about the
                        newly-stored image
        PUT /demos/<ID> -- Update image metadata and/or upload image
                            data for a previously-reserved image
        DELETE /demos/<ID> -- Delete the image with id <ID>
    """

    def __init__(self, db_api=None):
        self.db_api = db_api or sps.db.get_api()
        self.notifier = notifier.Notifier()
        self.policy = policy.Enforcer()
        self.pool = eventlet.GreenPool(size=1024)
        if property_utils.is_property_protection_enabled():
            self.prop_enforcer = property_utils.PropertyRules(self.policy)
        else:
            self.prop_enforcer = None

    def _enforce(self, req, action):
        """Authorize an action against our policies"""
        try:
            self.policy.enforce(req.context, action, {})
        except exception.Forbidden:
            raise HTTPForbidden()

    def create(self, req, body):
        self._enforce(req, 'add_demo')
        try:
            if body.has_key('demo'):
                demo = body['demo']
                demo = self.db_api.add_demo(req.context, demo)
            else:
                raise HTTPBadRequest(explanation="create demo params dicts %s has not demo key." %body)
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation="%s" % e)
        demo_dict = self._translate_demo_to_json(demo)
        return {'demo' : demo_dict}

    def show(self, req, id):
        self._enforce(req, 'get_demo')
        try:
            demo = self.db_api.get_demo(req.context, id)
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation="%s" % e)
        demo_dict = {}
        if demo:
            demo_dict = self._translate_demo_to_json(demo)
        return {'demo' : demo_dict}

    def index(self, req):
        self._enforce(req, 'get_demos_all')
        try:
            demos = self.db_api.get_demo_list(req.context)
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation="%s" % e)
        demo_list = []
        if demos:
            demo_list = [self._translate_demo_to_json(demo) for demo in demos]
        return demo_list

    def update(self, req, id, body):
        self._enforce(req, 'update_demo')
        try:
            if body.has_key('demo'):
                demo = body['demo']
                db_demo = self.db_api.update_demo(req.context, id, demo)
            else:
                raise HTTPBadRequest(explanation="create demo params dicts %s has not demo key." %body)
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation="%s" % e)
        demo_dict = self._translate_demo_to_json(db_demo)
        return {'demo' : demo_dict}

    def delete(self, req, id):
        self._enforce(req, 'delete_demo')
        try:
            self.db_api.delete_demo(req.context, id)
        except exception.Invalid as e:
            raise HTTPBadRequest(explanation="%s" % e)
        return {'result' : 'success'}

def create_resource():
    deserializer = wsgi.JSONRequestDeserializer()
    serializer = wsgi.JSONResponseSerializer()
    return wsgi.Resource(Controller(), deserializer, serializer)
