# Copyright 2011 OpenStack Foundation
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


from sps.api.v1 import demos
from sps.common import wsgi


class API(wsgi.Router):

    """WSGI router for sps v1 API requests."""

    def __init__(self, mapper):
        demos_resource = demos.create_resource()

        mapper.connect("/",
                       controller=demos_resource,
                       action="index")
        mapper.connect("/demos",
                       controller=demos_resource,
                       action='index',
                       conditions={'method': ['GET']})
        mapper.connect("/demos",
                       controller=demos_resource,
                       action='create',
                       conditions={'method': ['POST']})
        mapper.connect("/demos/detail",
                       controller=demos_resource,
                       action='detail',
                       conditions={'method': ['GET', 'HEAD']})
        mapper.connect("/demos/{id}",
                       controller=demos_resource,
                       action="meta",
                       conditions=dict(method=["HEAD"]))
        mapper.connect("/demos/{id}",
                       controller=demos_resource,
                       action="show",
                       conditions=dict(method=["GET"]))
        mapper.connect("/demos/{id}",
                       controller=demos_resource,
                       action="update",
                       conditions=dict(method=["PUT"]))
        mapper.connect("/demos/{id}",
                       controller=demos_resource,
                       action="delete",
                       conditions=dict(method=["DELETE"]))

        #add you API route at this ,ex: define you demos2_resource = demos2.create_resource()

        super(API, self).__init__(mapper)
