# Copyright 2011, OpenStack Foundation
# Copyright 2012, Red Hat, Inc.
# Copyright 2013 IBM Corp.
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

from oslo.config import cfg
from oslo import messaging
import webob

from sps.common import exception
from sps.common import utils
from sps.openstack.common import excutils
import sps.openstack.common.log as logging
from sps.openstack.common import timeutils

notifier_opts = [
    cfg.StrOpt('notifier_strategy', default='default',
               help=_('Notifications can be sent when demos are create, '
                      'updated or deleted. There are three methods of sending '
                      'notifications, logging (via the log_file directive), '
                      'rabbit (via a rabbitmq queue), qpid (via a Qpid '
                      'message queue), or noop (no notifications sent, the '
                      'default). (DEPRECATED)')),

    cfg.StrOpt('default_publisher_id', default="image.localhost",
               help='Default publisher_id for outgoing notifications.'),
]

CONF = cfg.CONF
CONF.register_opts(notifier_opts)

LOG = logging.getLogger(__name__)

_STRATEGY_ALIASES = {
    "logging": "log",
    "rabbit": "messaging",
    "qpid": "messaging",
    "noop": "noop",
    "default": "noop",
}

_ALIASES = {
    'sps.openstack.common.rpc.impl_kombu': 'rabbit',
    'sps.openstack.common.rpc.impl_qpid': 'qpid',
    'sps.openstack.common.rpc.impl_zmq': 'zmq',
}


class Notifier(object):
    """Uses a notification strategy to send out messages about events."""

    def __init__(self, strategy=None):

        _driver = None
        _strategy = strategy

        if CONF.notifier_strategy != 'default':
            msg = _("notifier_strategy was deprecated in "
                    "favor of `notification_driver`")
            LOG.warn(msg)

            # NOTE(flaper87): Use this to keep backwards
            # compatibility. We'll try to get an oslo.messaging
            # driver from the specified strategy.
            _strategy = strategy or CONF.notifier_strategy
            _driver = _STRATEGY_ALIASES.get(_strategy)

        publisher_id = CONF.default_publisher_id

        try:
            # NOTE(flaper87): Assume the user has configured
            # the transport url.
            self._transport = messaging.get_transport(CONF,
                                                      aliases=_ALIASES)
        except messaging.DriverLoadFailure:
            # NOTE(flaper87): Catch driver load failures and re-raise
            # them *just* if the `transport_url` option was set. This
            # step is intended to keep backwards compatibility and avoid
            # weird behaviors (like exceptions on missing dependencies)
            # when the old notifier options are used.
            if CONF.transport_url is not None:
                with excutils.save_and_reraise_exception():
                    LOG.exception(_('Error loading the notifier'))

        # NOTE(flaper87): This needs to be checked
        # here because the `get_transport` call
        # registers `transport_url` into ConfigOpts.
        if not CONF.transport_url:
            # NOTE(flaper87): The next 3 lines help
            # with the migration to oslo.messaging.
            # Without them, gate tests won't know
            # what driver should be loaded.
            # Once this patch lands, devstack will be
            # updated and then these lines will be removed.
            url = None
            if _strategy in ['rabbit', 'qpid']:
                url = _strategy + '://'
            self._transport = messaging.get_transport(CONF, url,
                                                      aliases=_ALIASES)

        self._notifier = messaging.Notifier(self._transport,
                                            driver=_driver,
                                            publisher_id=publisher_id)

    def warn(self, event_type, payload):
        self._notifier.warn({}, event_type, payload)

    def info(self, event_type, payload):
        self._notifier.info({}, event_type, payload)

    def error(self, event_type, payload):
        self._notifier.error({}, event_type, payload)



