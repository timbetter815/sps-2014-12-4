#!/usr/bin/env python

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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

"""
sps API Server
"""

import eventlet
import os
import sys

from sps.common import utils

# Monkey patch socket, time, select, threads
eventlet.patcher.monkey_patch(all=False, socket=True, time=True,
                              select=True, thread=False)

# If ../sps/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'sps', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from sps.common import config
from sps.common import exception
from sps.common import wsgi
from sps.openstack.common import log


def fail(returncode, e):
    sys.stderr.write("ERROR: %s\n" % utils.exception_to_str(e))
    sys.exit(returncode)


def main():
    try:
        config.parse_args()
        log.setup('sps')
        server = wsgi.Server()
        server.start(config.load_paste_app('sps-api'), default_port=9898)
        server.wait()
    except exception.WorkerCreationFailure as e:
        fail(2, e)
    except RuntimeError as e:
        fail(1, e)


if __name__ == '__main__':
    main()
