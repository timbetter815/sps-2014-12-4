# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2010-2011 OpenStack Foundation
# Copyright 2012 Justin Santa Barbara
# Copyright 2013 IBM Corp.
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


"""Defines interface for DB access."""

from oslo.config import cfg
import six
from six.moves import xrange
import sqlalchemy
import sqlalchemy.orm as sa_orm
import sqlalchemy.sql as sa_sql
import functools
from nova.openstack.common.db.sqlalchemy import session as db_session

from sps.common import exception
from sps.db.sqlalchemy import models
from sps.openstack.common.db import exception as db_exception
from sps.openstack.common.db.sqlalchemy import session
import sps.openstack.common.log as os_logging
from sps.openstack.common.gettextutils import _
from sps.openstack.common import timeutils
import sps.context
import sys


BASE = models.BASE
sa_logger = None
LOG = os_logging.getLogger(__name__)


STATUSES = ['active', 'saving', 'queued', 'killed', 'pending_delete',
            'deleted']

connection_opts = [
    cfg.StrOpt('slave_connection',
               secret=True,
               help='The SQLAlchemy connection string used to connect to the '
                    'slave database'),
]

CONF = cfg.CONF
CONF.import_opt('debug', 'sps.openstack.common.log')
CONF.import_opt('connection', 'sps.openstack.common.db.options',
                group='database')
CONF.register_opts(connection_opts, group='database')

_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        _FACADE = session.EngineFacade(
            CONF.database.connection,
            **dict(six.iteritems(CONF.database)))
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(autocommit=True, expire_on_commit=False):
    facade = _create_facade_lazily()
    return facade.get_session(autocommit=autocommit,
                              expire_on_commit=expire_on_commit)


def clear_db_env():
    """
    Unset global configuration variables for database.
    """
    global _FACADE
    _FACADE = None



def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def require_admin_context(f):
    """Decorator to require admin request context.

    The first argument to the wrapped function must be the context.

    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        nova.context.require_admin_context(args[0])
        return f(*args, **kwargs)
    return wrapper


def require_context(f):
    """Decorator to require *any* user or admin context.

    This does no authorization for user or project access matching, see
    :py:func:`nova.context.authorize_project_context` and
    :py:func:`nova.context.authorize_user_context`.

    The first argument to the wrapped function must be the context.

    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        sps.context.require_context(args[0])
        return f(*args, **kwargs)
    return wrapper


def clear_db_env():
    """
    Unset global configuration variables for database.
    """
    global _FACADE
    _FACADE = None

def model_query(context, model, *args, **kwargs):
    """Query helper that accounts for context's `read_deleted` field.

    :param context: context to query under
    :param use_slave: If true, use slave_connection
    :param session: if present, the session to use
    :param read_deleted: if present, overrides context's read_deleted field.
    :param project_only: if present and context is user-type, then restrict
            query to match the context's project_id. If set to 'allow_none',
            restriction includes project_id = None.
    :param base_model: Where model_query is passed a "model" parameter which is
            not a subclass of NovaBase, we should pass an extra base_model
            parameter that is a subclass of NovaBase and corresponds to the
            model parameter.
    """

    use_slave = kwargs.get('use_slave') or False
    if CONF.database.slave_connection == '':
        use_slave = False

    session = kwargs.get('session') or get_session()
    read_deleted = kwargs.get('read_deleted') or context.read_deleted
    project_only = kwargs.get('project_only', False)

    def issubclassof_sps_base(obj):
        return isinstance(obj, type) and issubclass(obj, models.SpsBase)

    base_model = model
    if not issubclassof_sps_base(base_model):
        base_model = kwargs.get('base_model', None)
        if not issubclassof_sps_base(base_model):
            raise Exception(_("model or base_model parameter should be "
                              "subclass of NovaBase"))

    query = session.query(model, *args)

    default_deleted_value = base_model.__mapper__.c.deleted.default.arg
    if read_deleted == 'no':
        query = query.filter(base_model.deleted == default_deleted_value)
    elif read_deleted == 'yes':
        pass  # omit the filter to include deleted and active
    elif read_deleted == 'only':
        query = query.filter(base_model.deleted != default_deleted_value)
    else:
        raise Exception(_("Unrecognized read_deleted value '%s'")
                            % read_deleted)

    if sps.context.is_user_context(context) and project_only:
        if project_only == 'allow_none':
            query = query.\
                filter(or_(base_model.project_id == context.project_id,
                           base_model.project_id == None))
        else:
            query = query.filter_by(project_id=context.project_id)

    return query

def get_demo(context, id):
    session = get_session()
    query = model_query(context, models.Demo, session=session, read_deleted="no")
    result = query.filter_by(id=id).first()
    return  result

def get_demo_list(context):
    session = get_session()
    query = model_query(context, models.Demo, session=session, read_deleted="no")
    result = query.all()

    return result

def add_demo(context, demo):
    try:
        demo_ref = models.Demo()
        for key, val in demo.items():
            demo_ref.update({key: val})
        demo_ref.update({'created_at': timeutils.datetime.datetime.utcnow()})
        demo_ref.save()
    except:
        raise exception.DemoCanNotDelete(id=id)
    return demo_ref

def delete_demo(context, id):
    try:
        session = get_session()
        query = model_query(context, models.Demo, session=session, read_deleted="no")
        query.filter_by(id=id).first().soft_delete(session)
    except:
        raise exception.DemoCanNotDelete(id=id)

def update_demo(context, id, demo):
    try:
        session = get_session(autocommit=True)
        query = model_query(context, models.Demo, session=session, read_deleted="no")
        demo_ref = query.filter_by(id=id).first()
        if not demo_ref:
            raise exception.DemoNotFound(id=id)
        for key, val in demo.items():
            demo_ref.update({key: val})
        demo_ref.update({'updated_at': timeutils.datetime.datetime.utcnow()})
        session.add(demo_ref)
        session.flush()
    except:
        raise exception.DemoCanNotUpdatate(id=id)
    return  demo_ref
