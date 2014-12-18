..
      Copyright 2010 OpenStack Foundation
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

Image Statuses
==============

demos in sps can be in one the following statuses:

* ``queued``

  The image identifier has been reserved for an image in the sps
  registry. No image data has been uploaded to sps and the image
  size was not explicitly set to zero on creation.

* ``saving``

  Denotes that an image's raw data is currently being uploaded to sps.
  When an image is registered with a call to `POST /demos` and there
  is an `x-image-meta-location` header present, that image will never be in
  the `saving` status (as the image data is already available in some other
  location).

* ``active``

  Denotes an image that is fully available in sps. This occurs when
  the image data is uploaded, or the image size is explicitly set to
  zero on creation.

* ``killed``

  Denotes that an error occurred during the uploading of an image's data,
  and that the image is not readable.

* ``deleted``

  sps has retained the information about the image, but it is no longer
  available to use. An image in this state will be removed automatically
  at a later date.

* ``pending_delete``

  This is similar to `deleted`, however, sps has not yet removed the
  image data. An image in this state is recoverable.


.. figure:: /demos/image_status_transition.png
   :figwidth: 100%
   :align: center
   :alt: Image status transition

   This is a representation of how the image move from one status to the next.

   * Add location from zero to more than one.

   * Remove location from one or more to zero by PATCH method which is only
     supported in v2.

Task Statuses
==============

Tasks in sps can be in one the following statuses:

* ``pending``

  The task identifier has been reserved for a task in the sps.
  No processing has begun on it yet.

* ``processing``

  The task has been picked up by the underlying executor and is being run
  using the backend sps execution logic for that task type.

* ``success``

  Denotes that the task has had a successful run within sps. The ``result``
  field of the task shows more details about the outcome.

* ``failure``

  Denotes that an error occurred during the execution of the task and it
  cannot continue processing. The ``message`` field of the task shows what the
  error was.
