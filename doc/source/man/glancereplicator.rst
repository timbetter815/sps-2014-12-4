=================
sps-replicator
=================

---------------------------------------------
Replicate demos across multiple data centers
---------------------------------------------

:Author: sps@lists.launchpad.net
:Date:   2014-01-16
:Copyright: OpenStack LLC
:Version: 2014.1
:Manual section: 1
:Manual group: cloud computing

SYNOPSIS
========

sps-replicator <command> [options] [args]

DESCRIPTION
===========

sps-replicator is a utility can be used to populate a new sps
server using the demos stored in an existing sps server. The demos
in the replicated sps server preserve the uuids, metadata, and image
data from the original.

COMMANDS
========

  **help <command>**
        Output help for one of the commands below

  **compare**
        What is missing from the slave sps?

  **dump**
        Dump the contents of a sps instance to local disk.

  **livecopy**
       Load the contents of one sps instance into another.

  **load**
        Load the contents of a local directory into sps.

  **size**
        Determine the size of a sps instance if dumped to disk.

OPTIONS
=======

  **-h, --help**
        Show this help message and exit

  **-c CHUNKSIZE, --chunksize=CHUNKSIZE**
        Amount of data to transfer per HTTP write

  **-d, --debug**
        Print debugging information

  **-D DONTREPLICATE, --dontreplicate=DONTREPLICATE**
        List of fields to not replicate

  **-m, --metaonly**
        Only replicate metadata, not demos

  **-l LOGFILE, --logfile=LOGFILE**
        Path of file to log to

  **-s, --syslog**
        Log to syslog instead of a file

  **-t TOKEN, --token=TOKEN**
        Pass in your authentication token if you have one. If
        you use this option the same token is used for both
        the master and the slave.

  **-M MASTERTOKEN, --mastertoken=MASTERTOKEN**
        Pass in your authentication token if you have one.
        This is the token used for the master.

  **-S SLAVETOKEN, --slavetoken=SLAVETOKEN**
        Pass in your authentication token if you have one.
        This is the token used for the slave.

  **-v, --verbose**
         Print more verbose output

  .. include:: footer.rst
