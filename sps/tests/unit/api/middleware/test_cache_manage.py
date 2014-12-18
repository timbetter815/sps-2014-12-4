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

from sps.api import cached_demos
from sps.api.middleware import cache_manage
import sps.common.config
import sps.common.wsgi
import sps.image_cache
from sps.tests import utils as test_utils

import mock
import webob


class TestCacheManageFilter(test_utils.BaseTestCase):
    @mock.patch.object(sps.image_cache.ImageCache, "init_driver")
    def setUp(self, mock_init_driver):
        super(TestCacheManageFilter, self).setUp()
        self.stub_application_name = "stubApplication"
        self.stub_value = "Stub value"
        self.image_id = "image_id_stub"

        mock_init_driver.return_value = None

        self.cache_manage_filter = cache_manage.CacheManageFilter(
            self.stub_application_name)

    def test_bogus_request(self):
        # prepare
        bogus_request = webob.Request.blank("/bogus/")

        # call
        resource = self.cache_manage_filter.process_request(bogus_request)

        #check
        self.assertIsNone(resource)

    @mock.patch.object(cached_demos.Controller, "get_cached_demos")
    def test_get_cached_demos(self,
                               mock_get_cached_demos):
        # setup
        mock_get_cached_demos.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/cached_demos")

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_get_cached_demos.assert_called_with(request)
        self.assertEqual('"' + self.stub_value + '"', resource.body)

    @mock.patch.object(cached_demos.Controller, "delete_cached_image")
    def test_delete_cached_image(self,
                                 mock_delete_cached_image):
        # setup
        mock_delete_cached_image.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/cached_demos/" + self.image_id,
                                      environ={'REQUEST_METHOD': "DELETE"})

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_delete_cached_image.assert_called_with(request,
                                                    image_id=self.image_id)
        self.assertEqual('"' + self.stub_value + '"', resource.body)

    @mock.patch.object(cached_demos.Controller, "delete_cached_demos")
    def test_delete_cached_demos(self,
                                  mock_delete_cached_demos):
        # setup
        mock_delete_cached_demos.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/cached_demos",
                                      environ={'REQUEST_METHOD': "DELETE"})

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_delete_cached_demos.assert_called_with(request)
        self.assertEqual('"' + self.stub_value + '"', resource.body)

    @mock.patch.object(cached_demos.Controller, "queue_image")
    def test_put_queued_image(self,
                              mock_queue_image):
        # setup
        mock_queue_image.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/queued_demos/" + self.image_id,
                                      environ={'REQUEST_METHOD': "PUT"})

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_queue_image.assert_called_with(request, image_id=self.image_id)
        self.assertEqual('"' + self.stub_value + '"', resource.body)

    @mock.patch.object(cached_demos.Controller, "get_queued_demos")
    def test_get_queued_demos(self,
                               mock_get_queued_demos):
        # setup
        mock_get_queued_demos.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/queued_demos")

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_get_queued_demos.assert_called_with(request)
        self.assertEqual('"' + self.stub_value + '"', resource.body)

    @mock.patch.object(cached_demos.Controller, "delete_queued_image")
    def test_delete_queued_image(self,
                                 mock_delete_queued_image):
        # setup
        mock_delete_queued_image.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/queued_demos/" + self.image_id,
                                      environ={'REQUEST_METHOD': 'DELETE'})

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_delete_queued_image.assert_called_with(request,
                                                    image_id=self.image_id)
        self.assertEqual('"' + self.stub_value + '"', resource.body)

    @mock.patch.object(cached_demos.Controller, "delete_queued_demos")
    def test_delete_queued_demos(self,
                                  mock_delete_queued_demos):
        # setup
        mock_delete_queued_demos.return_value = self.stub_value

        # prepare
        request = webob.Request.blank("/v1/queued_demos",
                                      environ={'REQUEST_METHOD': 'DELETE'})

        # call
        resource = self.cache_manage_filter.process_request(request)

        # check
        mock_delete_queued_demos.assert_called_with(request)
        self.assertEqual('"' + self.stub_value + '"', resource.body)
