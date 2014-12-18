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

import mock
import sys

import six

import sps.cmd.api
import sps.cmd.cache_cleaner
import sps.cmd.cache_pruner
import sps.common.config
from sps.common import exception as exc
import sps.common.wsgi
import sps.image_cache.cleaner
import sps.image_cache.pruner
from sps.tests import utils as test_utils


class TestspsApiCmd(test_utils.BaseTestCase):

    __argv_backup = None

    def _do_nothing(self, *args, **kwargs):
        pass

    def _raise(self, exc):
        def fake(*args, **kwargs):
            raise exc
        return fake

    def setUp(self):
        super(TestspsApiCmd, self).setUp()
        self.__argv_backup = sys.argv
        sys.argv = ['sps-api']
        self.stderr = six.StringIO()
        sys.stderr = self.stderr

        self.stubs.Set(sps.common.config, 'load_paste_app',
                       self._do_nothing)
        self.stubs.Set(sps.common.wsgi.Server, 'start',
                       self._do_nothing)
        self.stubs.Set(sps.common.wsgi.Server, 'wait',
                       self._do_nothing)

    def tearDown(self):
        sys.stderr = sys.__stderr__
        sys.argv = self.__argv_backup
        super(TestspsApiCmd, self).tearDown()

    def test_supported_default_store(self):
        self.config(default_store='file')
        sps.cmd.api.main()

    def test_unsupported_default_store(self):
        self.config(default_store='shouldnotexist')
        exit = self.assertRaises(SystemExit, sps.cmd.api.main)
        self.assertEqual(exit.code, 1)

    def test_worker_creation_failure(self):
        failure = exc.WorkerCreationFailure(reason='test')
        self.stubs.Set(sps.common.wsgi.Server, 'start',
                       self._raise(failure))
        exit = self.assertRaises(SystemExit, sps.cmd.api.main)
        self.assertEqual(exit.code, 2)

    @mock.patch.object(sps.common.config, 'parse_cache_args')
    @mock.patch.object(sps.openstack.common.log, 'setup')
    @mock.patch.object(sps.image_cache.ImageCache, 'init_driver')
    @mock.patch.object(sps.image_cache.ImageCache, 'clean')
    def test_cache_cleaner_main(self, mock_cache_clean,
                                mock_cache_init_driver, mock_log_setup,
                                mock_parse_config):
        mock_cache_init_driver.return_value = None

        manager = mock.MagicMock()
        manager.attach_mock(mock_log_setup, 'mock_log_setup')
        manager.attach_mock(mock_parse_config, 'mock_parse_config')
        manager.attach_mock(mock_cache_init_driver, 'mock_cache_init_driver')
        manager.attach_mock(mock_cache_clean, 'mock_cache_clean')
        sps.cmd.cache_cleaner.main()
        expected_call_sequence = [mock.call.mock_parse_config(),
                                  mock.call.mock_log_setup('sps'),
                                  mock.call.mock_cache_init_driver(),
                                  mock.call.mock_cache_clean()]
        self.assertEqual(expected_call_sequence, manager.mock_calls)

    @mock.patch.object(sps.image_cache.base.CacheApp, '__init__')
    def test_cache_cleaner_main_runtime_exception_handling(self, mock_cache):
        mock_cache.return_value = None
        self.stubs.Set(sps.image_cache.cleaner.Cleaner, 'run',
                       self._raise(RuntimeError))
        exit = self.assertRaises(SystemExit, sps.cmd.cache_cleaner.main)
        self.assertEqual('ERROR: ', exit.code)

    @mock.patch.object(sps.common.config, 'parse_cache_args')
    @mock.patch.object(sps.openstack.common.log, 'setup')
    @mock.patch.object(sps.image_cache.ImageCache, 'init_driver')
    @mock.patch.object(sps.image_cache.ImageCache, 'prune')
    def test_cache_pruner_main(self, mock_cache_prune,
                               mock_cache_init_driver, mock_log_setup,
                               mock_parse_config):
        mock_cache_init_driver.return_value = None

        manager = mock.MagicMock()
        manager.attach_mock(mock_log_setup, 'mock_log_setup')
        manager.attach_mock(mock_parse_config, 'mock_parse_config')
        manager.attach_mock(mock_cache_init_driver, 'mock_cache_init_driver')
        manager.attach_mock(mock_cache_prune, 'mock_cache_prune')
        sps.cmd.cache_pruner.main()
        expected_call_sequence = [mock.call.mock_parse_config(),
                                  mock.call.mock_log_setup('sps'),
                                  mock.call.mock_cache_init_driver(),
                                  mock.call.mock_cache_prune()]
        self.assertEqual(expected_call_sequence, manager.mock_calls)

    @mock.patch.object(sps.image_cache.base.CacheApp, '__init__')
    def test_cache_pruner_main_runtime_exception_handling(self, mock_cache):
        mock_cache.return_value = None
        self.stubs.Set(sps.image_cache.pruner.Pruner, 'run',
                       self._raise(RuntimeError))
        exit = self.assertRaises(SystemExit, sps.cmd.cache_pruner.main)
        self.assertEqual('ERROR: ', exit.code)
