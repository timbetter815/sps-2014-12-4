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

import webob.exc

from sps.common import exception
import sps.openstack.common.log as logging
from oslo.config import cfg

auth_opts = [
    cfg.StrOpt('auth_url', default='http://controller:35357/v2.0',
               help=_('')),
    cfg.StrOpt('admin_tenant_name', default='service',
               help=_('')),
    cfg.StrOpt('admin_user', default='admin',
                help=_('')),
    cfg.StrOpt('admin_password', default='password',
               help=_('')),
]

CONF = cfg.CONF
CONF.register_opts(auth_opts, group='keystone_authtoken')


class BaseController(object):
    def get_sps_meta_or_404(self, request, sps_id):
        """
        Grabs the sps metadata for an sps with a supplied
        identifier or raises an HTTPNotFound (404) response

        :param request: The WSGI/Webob Request object
        :param sps_id: The opaque sps identifier

        :raises HTTPNotFound if sps does not exist
        """
        context = request.context


    def get_active_sps_meta_or_404(self, request, sps_id):
        """
        Same as get_sps_meta_or_404 except that it will raise a 404 if the
        sps isn't 'active'.
        """
        sps = self.get_sps_meta_or_404(request, sps_id)
        if sps['status'] != 'active':
            msg = "sps %s is not active" % sps_id
            LOG.debug(msg)
            raise webob.exc.HTTPNotFound(
                msg, request=request, content_type='text/plain')
        return sps

    def _translate_demo_to_json(self, obj):
        obj_dict = obj.__dict__
        del obj_dict['_sa_instance_state']
        return obj_dict

    def _get_ksclient(self):
        from keystoneclient.v2_0 import client
        return client.Client(username= CONF.keystone_authtoken.admin_user,
                             password= CONF.keystone_authtoken.admin_password,
                             tenant_name = CONF.keystone_authtoken.admin_tenant_name,
                             auth_url=CONF.keystone_authtoken.auth_url)


    def _get_roles(self, user_id, tenant_id):
        ksclient = self._get_ksclient()
        return ksclient.roles.roles_for_user(user_id, tenant_id)

    def _get_tenants_list(self, user_id):
        ksclient = self._get_ksclient()
        return ksclient.tenants.get_user_tenants(user_id)