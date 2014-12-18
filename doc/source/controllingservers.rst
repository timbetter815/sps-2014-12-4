..
      Copyright 2011 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Controlling sps Servers
==========================

This section describes the ways to start, stop, and reload sps's server
programs.

Starting a server
-----------------

There are two ways to start a sps server (either the API server or the
registry server):

* Manually calling the server program

* Using the ``sps-control`` server daemon wrapper program

We recommend using the second method.

Manually starting the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first is by directly calling the server program, passing in command-line
options and a single argument for a ``paste.deploy`` configuration file to
use when configuring the server application.

.. note::

  sps ships with an ``etc/`` directory that contains sample ``paste.deploy``
  configuration files that you can copy to a standard configuation directory and
  adapt for your own uses. Specifically, bind_host must be set properly.

If you do `not` specify a configuration file on the command line, sps will
do its best to locate a configuration file in one of the
following directories, stopping at the first config file it finds:

* ``$CWD``
* ``~/.sps``
* ``~/``
* ``/etc/sps``
* ``/etc``

The filename that is searched for depends on the server application name. So,
if you are starting up the API server, ``sps-api.conf`` is searched for,
otherwise ``sps-registry.conf``.

If no configuration file is found, you will see an error, like::

  $> sps-api
  ERROR: Unable to locate any configuration file. Cannot load application sps-api

Here is an example showing how you can manually start the ``sps-api`` server and ``sps-registry`` in a shell.::

  $ sudo sps-api sps-api.conf --debug &
  jsuh@mc-ats1:~$ 2011-04-13 14:50:12    DEBUG [sps-api] ********************************************************************************
  2011-04-13 14:50:12    DEBUG [sps-api] Configuration options gathered from config file:
  2011-04-13 14:50:12    DEBUG [sps-api] /home/jsuh/sps-api.conf
  2011-04-13 14:50:12    DEBUG [sps-api] ================================================
  2011-04-13 14:50:12    DEBUG [sps-api] bind_host                      65.114.169.29
  2011-04-13 14:50:12    DEBUG [sps-api] bind_port                      9292
  2011-04-13 14:50:12    DEBUG [sps-api] debug                          True
  2011-04-13 14:50:12    DEBUG [sps-api] default_store                  file
  2011-04-13 14:50:12    DEBUG [sps-api] filesystem_store_datadir       /home/jsuh/demos/
  2011-04-13 14:50:12    DEBUG [sps-api] registry_host                  65.114.169.29
  2011-04-13 14:50:12    DEBUG [sps-api] registry_port                  9191
  2011-04-13 14:50:12    DEBUG [sps-api] verbose                        False
  2011-04-13 14:50:12    DEBUG [sps-api] ********************************************************************************
  2011-04-13 14:50:12    DEBUG [routes.middleware] Initialized with method overriding = True, and path info altering = True
  2011-04-13 14:50:12    DEBUG [eventlet.wsgi.server] (21354) wsgi starting up on http://65.114.169.29:9292/

  $ sudo sps-registry sps-registry.conf &
  jsuh@mc-ats1:~$ 2011-04-13 14:51:16     INFO [sqlalchemy.engine.base.Engine.0x...feac] PRAGMA table_info("demos")
  2011-04-13 14:51:16     INFO [sqlalchemy.engine.base.Engine.0x...feac] ()
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Col ('cid', 'name', 'type', 'notnull', 'dflt_value', 'pk')
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (0, u'created_at', u'DATETIME', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (1, u'updated_at', u'DATETIME', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (2, u'deleted_at', u'DATETIME', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (3, u'deleted', u'BOOLEAN', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (4, u'id', u'INTEGER', 1, None, 1)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (5, u'name', u'VARCHAR(255)', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (6, u'disk_format', u'VARCHAR(20)', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (7, u'container_format', u'VARCHAR(20)', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (8, u'size', u'INTEGER', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (9, u'status', u'VARCHAR(30)', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (10, u'is_public', u'BOOLEAN', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (11, u'location', u'TEXT', 0, None, 0)
  2011-04-13 14:51:16     INFO [sqlalchemy.engine.base.Engine.0x...feac] PRAGMA table_info("image_properties")
  2011-04-13 14:51:16     INFO [sqlalchemy.engine.base.Engine.0x...feac] ()
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Col ('cid', 'name', 'type', 'notnull', 'dflt_value', 'pk')
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (0, u'created_at', u'DATETIME', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (1, u'updated_at', u'DATETIME', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (2, u'deleted_at', u'DATETIME', 0, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (3, u'deleted', u'BOOLEAN', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (4, u'id', u'INTEGER', 1, None, 1)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (5, u'image_id', u'INTEGER', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (6, u'key', u'VARCHAR(255)', 1, None, 0)
  2011-04-13 14:51:16    DEBUG [sqlalchemy.engine.base.Engine.0x...feac] Row (7, u'value', u'TEXT', 0, None, 0)

  $ ps aux | grep sps
  root     20009  0.7  0.1  12744  9148 pts/1    S    12:47   0:00 /usr/bin/python /usr/bin/sps-api sps-api.conf --debug
  root     20012  2.0  0.1  25188 13356 pts/1    S    12:47   0:00 /usr/bin/python /usr/bin/sps-registry sps-registry.conf
  jsuh     20017  0.0  0.0   3368   744 pts/1    S+   12:47   0:00 grep sps

Simply supply the configuration file as the first argument
(the ``etc/sps-api.conf`` and  ``etc/sps-registry.conf`` sample configuration
files were used in the above example) and then any common options
you want to use (``--debug`` was used above to show some of the debugging
output that the server shows when starting up. Call the server program
with ``--help`` to see all available options you can specify on the
command line.)

For more information on configuring the server via the ``paste.deploy``
configuration files, see the section entitled
:doc:`Configuring sps servers <configuring>`

Note that the server `daemonizes` itself by using the standard
shell backgrounding indicator, ``&``, in the previous example. For most use cases, we recommend
using the ``sps-control`` server daemon wrapper for daemonizing. See below
for more details on daemonization with ``sps-control``.

Using the ``sps-control`` program to start the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The second way to start up a sps server is to use the ``sps-control``
program. ``sps-control`` is a wrapper script that allows the user to
start, stop, restart, and reload the other sps server programs in
a fashion that is more conducive to automation and scripting.

Servers started via the ``sps-control`` program are always `daemonized`,
meaning that the server program process runs in the background.

To start a sps server with ``sps-control``, simply call
``sps-control`` with a server and the word "start", followed by
any command-line options you wish to provide. Start the server with ``sps-control``
in the following way::

  $> sudo sps-control [OPTIONS] <SERVER> start [CONFPATH]

.. note::

  You must use the ``sudo`` program to run ``sps-control`` currently, as the
  pid files for the server programs are written to /var/run/sps/

Here is an example that shows how to start the ``sps-registry`` server
with the ``sps-control`` wrapper script. ::


  $ sudo sps-control api start sps-api.conf
  Starting sps-api with /home/jsuh/sps.conf

  $ sudo sps-control registry start sps-registry.conf
  Starting sps-registry with /home/jsuh/sps.conf

  $ ps aux | grep sps
  root     20038  4.0  0.1  12728  9116 ?        Ss   12:51   0:00 /usr/bin/python /usr/bin/sps-api /home/jsuh/sps-api.conf
  root     20039  6.0  0.1  25188 13356 ?        Ss   12:51   0:00 /usr/bin/python /usr/bin/sps-registry /home/jsuh/sps-registry.conf
  jsuh     20042  0.0  0.0   3368   744 pts/1    S+   12:51   0:00 grep sps


The same configuration files are used by ``sps-control`` to start the
sps server programs, and you can specify (as the example above shows)
a configuration file when starting the server.


In order for your launched sps service to be monitored for unexpected death
and respawned if necessary, use the following option:


  $ sudo sps-control [service] start --respawn ...


Note that this will cause ``sps-control`` itself to remain running. Also note
that deliberately stopped services are not respawned, neither are rapidly bouncing
services (where process death occurred within one second of the last launch).


By default, output from sps services is discarded when launched with ``sps-control``.
In order to capture such output via syslog, use the following option:


  $ sudo sps-control --capture-output ...


Stopping a server
-----------------

If you started a sps server manually and did not use the ``&`` backgrounding
function, simply send a terminate signal to the server process by typing
``Ctrl-C``

If you started the sps server using the ``sps-control`` program, you can
use the ``sps-control`` program to stop it. Simply do the following::

  $> sudo sps-control <SERVER> stop

as this example shows::

  $> sudo sps-control registry stop
  Stopping sps-registry  pid: 17602  signal: 15

Restarting a server
-------------------

You can restart a server with the ``sps-control`` program, as demonstrated
here::

  $> sudo sps-control registry restart etc/sps-registry.conf
  Stopping sps-registry  pid: 17611  signal: 15
  Starting sps-registry with /home/jpipes/repos/sps/trunk/etc/sps-registry.conf
