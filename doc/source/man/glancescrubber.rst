===============
sps-scrubber
===============

--------------------
sps scrub service
--------------------

:Author: sps@lists.launchpad.net
:Date:   2014-01-16
:Copyright: OpenStack LLC
:Version: 2014.1
:Manual section: 1
:Manual group: cloud computing

SYNOPSIS
========

sps-scrubber [options]

DESCRIPTION
===========

sps-scrubber is a utility that cleans up demos that have been deleted. The
mechanics of this differ depending on the backend store and pending_deletion
options chosen.

Multiple sps-scrubbers can be run in a single deployment, but only one of
them may be designated as the 'cleanup_scrubber' in the sps-scrubber.conf
file. The 'cleanup_scrubber' coordinates other sps-scrubbers by maintaining
the master queue of demos that need to be removed.

The sps-scubber.conf file also specifies important configuration items such
as the time between runs ('wakeup_time' in seconds), length of time demos
can be pending before their deletion ('cleanup_scrubber_time' in seconds) as
well as registry connectivity options.

sps-scrubber can run as a periodic job or long-running daemon.

OPTIONS
=======

  **General options**

  .. include:: general_options.rst

  **-D, --daemon**
        Run as a long-running process. When not specified (the
        default) run the scrub operation once and then exits.
        When specified do not exit and run scrub on
        wakeup_time interval as specified in the config.

  **--nodaemon**
        The inverse of --daemon. Runs the scrub operation once and
        then exits. This is the default.

FILES
======

  **/etc/sps/sps-scrubber.conf**
      Default configuration file for the sps Scrubber

 .. include:: footer.rst
