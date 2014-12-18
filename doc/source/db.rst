..
      Copyright 2012 OpenStack Foundation
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

Database Management
===================

The default metadata driver for sps uses sqlalchemy, which implies there
exists a backend database which must be managed. The ``sps-manage`` binary
provides a set of commands for making this easier.

The commands should be executed as a subcommand of 'db':

    sps-manage db <cmd> <args>


Sync the Database
-----------------

    sps-manage db sync <version> <current_version>

Place a database under migration control and upgrade, creating it first if necessary.


Determining the Database Version
--------------------------------

    sps-manage db version

This will print the current migration level of a sps database.


Upgrading an Existing Database
------------------------------

    sps-manage db upgrade <VERSION>

This will take an existing database and upgrade it to the specified VERSION.


Downgrading an Existing Database
--------------------------------

    sps-manage db downgrade <VERSION>

This will downgrade an existing database from the current version to the
specified VERSION.

