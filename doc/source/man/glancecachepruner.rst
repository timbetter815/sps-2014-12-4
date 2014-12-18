===================
sps-cache-pruner
===================

-------------------
sps cache pruner
-------------------

:Author: sps@lists.launchpad.net
:Date:   2014-01-16
:Copyright: OpenStack LLC
:Version: 2014.1
:Manual section: 1
:Manual group: cloud computing

SYNOPSIS
========

  sps-cache-pruner [options]

DESCRIPTION
===========

Prunes demos from the sps cache when the space exceeds the value
set in the image_cache_max_size configuration option. This is meant
to be run as a periodic task, perhaps every half-hour.

OPTIONS
========

  **General options**

  .. include:: general_options.rst

FILES
=====

  **/etc/sps/sps-cache.conf**
        Default configuration file for the sps Cache

  .. include:: footer.rst
