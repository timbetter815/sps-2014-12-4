====================
sps-cache-cleaner
====================

----------------------------------------------------------------
sps Image Cache Invalid Cache Entry and Stalled Image cleaner
----------------------------------------------------------------

:Author: sps@lists.launchpad.net
:Date:   2014-01-16
:Copyright: OpenStack LLC
:Version: 2014.1
:Manual section: 1
:Manual group: cloud computing

SYNOPSIS
========

sps-cache-cleaner [options]

DESCRIPTION
===========

This is meant to be run as a periodic task from cron.

If something goes wrong while we're caching an image (for example the fetch
times out, or an exception is raised), we create an 'invalid' entry. These
entires are left around for debugging purposes. However, after some period of
time, we want to clean these up.

Also, if an incomplete image hangs around past the image_cache_stall_time
period, we automatically sweep it up.

OPTIONS
=======

  **General options**

  .. include:: general_options.rst

FILES
======

  **/etc/sps/sps-cache.conf**
    Default configuration file for the sps Cache

  .. include:: footer.rst
