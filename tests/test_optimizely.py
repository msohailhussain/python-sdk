# Copyright 2016-2017, Optimizely
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import mock

from optimizely import entities
from optimizely import error_handler
from optimizely import exceptions
from optimizely import logger
from optimizely import optimizely
from optimizely import project_config
from optimizely import user_profile
from optimizely import version
from optimizely.helpers import enums
from . import base


class OptimizelyTest(base.BaseTest):

  def _validate_event_object(self, event_obj, expected_url, expected_params, expected_verb, expected_headers):
    """ Helper method to validate properties of the event object. """

    self.assertEqual(expected_url, event_obj.url)
    self.assertEqual(expected_params, event_obj.params)
    self.assertEqual(expected_verb, event_obj.http_verb)
    self.assertEqual(expected_headers, event_obj.headers)

  def _validate_event_object_event_tags(self, event_obj, expected_event_metric_params, expected_event_features_params):
    """ Helper method to validate properties of the event object related to event tags. """

    # get event metrics from the created event object
    event_metrics = event_obj.params['eventMetrics']
    self.assertEqual(expected_event_metric_params, event_metrics)

    # get event features from the created event object
    event_features = event_obj.params['eventFeatures']
    self.assertEqual(expected_event_features_params, event_features)

  def test_init__invalid_datafile__logs_error(self):
    """ Test that invalid datafile logs error on init. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      opt_obj = optimizely.Optimizely('invalid_datafile')

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided "datafile" is in an invalid format.')
    self.assertFalse(opt_obj.is_valid)

  def test_init__invalid_event_dispatcher__logs_error(self):
    """ Test that invalid event_dispatcher logs error on init. """

    class InvalidDispatcher(object):
      pass

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      opt_obj = optimizely.Optimizely(json.dumps(self.config_dict), event_dispatcher=InvalidDispatcher)

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided "event_dispatcher" is in an invalid format.')
    self.assertFalse(opt_obj.is_valid)

  def test_init__invalid_logger__logs_error(self):
    """ Test that invalid logger logs error on init. """

    class InvalidLogger(object):
      pass

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      opt_obj = optimizely.Optimizely(json.dumps(self.config_dict), logger=InvalidLogger)

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided "logger" is in an invalid format.')
    self.assertFalse(opt_obj.is_valid)

  def test_init__invalid_error_handler__logs_error(self):
    """ Test that invalid error_handler logs error on init. """

    class InvalidErrorHandler(object):
      pass

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      opt_obj = optimizely.Optimizely(json.dumps(self.config_dict), error_handler=InvalidErrorHandler)

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided "error_handler" is in an invalid format.')
    self.assertFalse(opt_obj.is_valid)

  def test_init__v1_datafile__logs_error(self):
    """ Test that v1 datafile logs error on init. """

    self.config_dict['version'] = project_config.V1_CONFIG_VERSION
    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      opt_obj = optimizely.Optimizely(json.dumps(self.config_dict))

    mock_logging.assert_called_once_with(
      enums.LogLevels.ERROR,
      'Provided datafile has unsupported version. Please use SDK version 1.1.0 or earlier for datafile version 1.'
    )
    self.assertFalse(opt_obj.is_valid)

  def test_skip_json_validation_true(self):
    """ Test that on setting skip_json_validation to true, JSON schema validation is not performed. """

    with mock.patch('optimizely.helpers.validator.is_datafile_valid') as mock_datafile_validation:
      optimizely.Optimizely(json.dumps(self.config_dict), skip_json_validation=True)

    self.assertEqual(0, mock_datafile_validation.call_count)

  def test_invalid_json_raises_schema_validation_off(self):
    """ Test that invalid JSON logs error if schema validation is turned off. """

    # Not  JSON
    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      optimizely.Optimizely('invalid_json', skip_json_validation=True)

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided "datafile" is in an invalid format.')

    # JSON having valid version, but entities have invalid format
    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      optimizely.Optimizely({'version': '2', 'events': 'invalid_value', 'experiments': 'invalid_value'},
                            skip_json_validation=True)

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided "datafile" is in an invalid format.')

  def test_activate(self):
    """ Test that activate calls dispatch_event with right params and returns expected variation. """

    with mock.patch(
            'optimizely.decision_service.DecisionService.get_variation',
            return_value=self.project_config.get_variation_from_id('test_experiment', '111129')) as mock_decision, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.assertEqual('variation', self.optimizely.activate('test_experiment', 'test_user'))

    expected_params = {
      'visitorId': 'test_user',
      'accountId': '12001',
      'projectId': '111001',
      'layerId': '111182',
      'revision': '42',
      'decision': {
        'variationId': '111129',
        'isLayerHoldback': False,
        'experimentId': '111127'
      },
      'userFeatures': [],
      'isGlobalHoldback': False,
      'timestamp': 42000,
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk'
    }
    mock_decision.assert_called_once_with(
      self.project_config.get_experiment_from_key('test_experiment'), 'test_user', None
    )
    self.assertEqual(1, mock_dispatch_event.call_count)
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/decision',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_activate__with_attributes__audience_match(self):
    """ Test that activate calls dispatch_event with right params and returns expected
    variation when attributes are provided and audience conditions are met. """

    with mock.patch(
            'optimizely.decision_service.DecisionService.get_variation',
            return_value=self.project_config.get_variation_from_id('test_experiment', '111129')) \
            as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.assertEqual('variation', self.optimizely.activate('test_experiment', 'test_user',
                                                             {'test_attribute': 'test_value'}))

    expected_params = {
      'visitorId': 'test_user',
      'accountId': '12001',
      'projectId': '111001',
      'layerId': '111182',
      'revision': '42',
      'decision': {
        'variationId': '111129',
        'isLayerHoldback': False,
        'experimentId': '111127'
      },
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'isGlobalHoldback': False,
      'timestamp': 42000,
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk'
    }
    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/decision',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_activate__with_attributes__audience_match__forced_bucketing(self):
    """ Test that activate calls dispatch_event with right params and returns expected
    variation when attributes are provided and audience conditions are met after a
    set_forced_variation is called. """

    with mock.patch('time.time', return_value=42), \
         mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:

      self.assertTrue(self.optimizely.set_forced_variation('test_experiment', 'test_user', 'control'))
      self.assertEqual('control', self.optimizely.activate('test_experiment', 'test_user',
                                                           {'test_attribute': 'test_value'}))

    expected_params = {
      'visitorId': 'test_user',
      'accountId': '12001',
      'projectId': '111001',
      'layerId': '111182',
      'revision': '42',
      'decision': {
        'variationId': '111128',
        'isLayerHoldback': False,
        'experimentId': '111127'
      },
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'isGlobalHoldback': False,
      'timestamp': 42000,
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk'
    }

    self.assertEqual(1, mock_dispatch_event.call_count)
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/decision',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_activate__with_attributes__no_audience_match(self):
    """ Test that activate returns None when audience conditions do not match. """

    with mock.patch('optimizely.helpers.audience.is_user_in_experiment', return_value=False) as mock_audience_check:
      self.assertIsNone(self.optimizely.activate('test_experiment', 'test_user',
                                                 attributes={'test_attribute': 'test_value'}))
    mock_audience_check.assert_called_once_with(self.project_config,
                                                self.project_config.get_experiment_from_key('test_experiment'),
                                                {'test_attribute': 'test_value'})

  def test_activate__with_attributes__invalid_attributes(self):
    """ Test that activate returns None and does not bucket or dispatch event when attributes are invalid. """

    with mock.patch('optimizely.bucketer.Bucketer.bucket') as mock_bucket, \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.assertIsNone(self.optimizely.activate('test_experiment', 'test_user', attributes='invalid'))

    self.assertEqual(0, mock_bucket.call_count)
    self.assertEqual(0, mock_dispatch_event.call_count)

  def test_activate__experiment_not_running(self):
    """ Test that activate returns None and does not dispatch event when experiment is not Running. """

    with mock.patch('optimizely.helpers.audience.is_user_in_experiment', return_value=True) as mock_audience_check, \
            mock.patch('optimizely.helpers.experiment.is_experiment_running',
                       return_value=False) as mock_is_experiment_running, \
            mock.patch('optimizely.bucketer.Bucketer.bucket') as mock_bucket, \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.assertIsNone(self.optimizely.activate('test_experiment', 'test_user',
                                                 attributes={'test_attribute': 'test_value'}))

    mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))
    self.assertEqual(0, mock_audience_check.call_count)
    self.assertEqual(0, mock_bucket.call_count)
    self.assertEqual(0, mock_dispatch_event.call_count)

  def test_activate__whitelisting_overrides_audience_check(self):
    """ Test that during activate whitelist overrides audience check if user is in the whitelist. """

    with mock.patch('optimizely.helpers.audience.is_user_in_experiment', return_value=False) as mock_audience_check, \
            mock.patch('optimizely.helpers.experiment.is_experiment_running',
                       return_value=True) as mock_is_experiment_running:
      self.assertEqual('control', self.optimizely.activate('test_experiment', 'user_1'))
    mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))
    self.assertEqual(0, mock_audience_check.call_count)

  def test_activate__bucketer_returns_none(self):
    """ Test that activate returns None and does not dispatch event when user is in no variation. """

    with mock.patch('optimizely.helpers.audience.is_user_in_experiment', return_value=True), \
         mock.patch('optimizely.bucketer.Bucketer.bucket', return_value=None) as mock_bucket, \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.assertIsNone(self.optimizely.activate('test_experiment', 'test_user',
                                                 attributes={'test_attribute': 'test_value'}))
    mock_bucket.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'), 'test_user')
    self.assertEqual(0, mock_dispatch_event.call_count)

  def test_activate__invalid_object(self):
    """ Test that activate logs error if Optimizely object is not created correctly. """

    opt_obj = optimizely.Optimizely('invalid_file')

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.assertIsNone(opt_obj.activate('test_experiment', 'test_user'))

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Datafile has invalid format. Failing "activate".')

  def test_track__with_attributes(self):
    """ Test that track calls dispatch_event with right params when attributes are provided. """

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'})

    expected_params = {
      'visitorId': 'test_user',
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk',
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'projectId': '111001',
      'isGlobalHoldback': False,
      'eventEntityId': '111095',
      'eventName': 'test_event',
      'eventFeatures': [],
      'eventMetrics': [],
      'timestamp': 42000,
      'revision': '42',
      'layerStates': [{
        'revision': '42',
        'decision': {
          'variationId': '111128',
          'isLayerHoldback': False,
          'experimentId': '111127'
        },
        'actionTriggered': True,
        'layerId': '111182'
      }],
      'accountId': '12001'
    }
    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/event',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_track__with_attributes__no_audience_match(self):
    """ Test that track does not call dispatch_event when audience conditions do not match. """

    with mock.patch('optimizely.bucketer.Bucketer.bucket',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_bucket, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'wrong_test_value'})

    self.assertEqual(0, mock_bucket.call_count)
    self.assertEqual(0, mock_dispatch_event.call_count)

  def test_track__with_attributes__invalid_attributes(self):
    """ Test that track does not bucket or dispatch event if attributes are invalid. """

    with mock.patch('optimizely.bucketer.Bucketer.bucket') as mock_bucket, \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes='invalid')

    self.assertEqual(0, mock_bucket.call_count)
    self.assertEqual(0, mock_dispatch_event.call_count)

  def test_track__with_event_tags(self):
    """ Test that track calls dispatch_event with right params when event tags are provided. """

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'},
                            event_tags={'revenue': 4200, 'value': 1.234, 'non-revenue': 'abc'})

    expected_params = {
      'visitorId': 'test_user',
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk',
      'revision': '42',
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'projectId': '111001',
      'isGlobalHoldback': False,
      'eventEntityId': '111095',
      'eventName': 'test_event',
      'eventFeatures': [{
        'name': 'non-revenue',
        'type': 'custom',
        'value': 'abc',
        'shouldIndex': False,
      }, {
        'name': 'revenue',
        'type': 'custom',
        'value': 4200,
        'shouldIndex': False,
      }, {
        'name': 'value',
        'type': 'custom',
        'value': 1.234,
        'shouldIndex': False,
      }],
      'eventMetrics': [{
        'name': 'revenue',
        'value': 4200
      }, {
        'name': 'value',
        'value': 1.234
      }],
      'timestamp': 42000,
      'layerStates': [{
        'revision': '42',
        'decision': {
          'variationId': '111128',
          'isLayerHoldback': False,
          'experimentId': '111127'
        },
        'actionTriggered': True,
        'layerId': '111182'
      }],
      'accountId': '12001'
    }
    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)

    # Sort event features based on ID
    mock_dispatch_event.call_args[0][0].params['eventFeatures'] = sorted(
      mock_dispatch_event.call_args[0][0].params['eventFeatures'], key=lambda x: x.get('name')
    )
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/event',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_track__with_event_tags_revenue(self):
    """ Test that track calls dispatch_event with right params when only revenue
        event tags are provided only. """

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'},
                            event_tags={'revenue': 4200, 'non-revenue': 'abc'})

    expected_params = {
      'visitorId': 'test_user',
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk',
      'revision': '42',
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'projectId': '111001',
      'isGlobalHoldback': False,
      'eventEntityId': '111095',
      'eventName': 'test_event',
      'eventFeatures': [{
        'name': 'non-revenue',
        'type': 'custom',
        'value': 'abc',
        'shouldIndex': False,
      }, {
        'name': 'revenue',
        'type': 'custom',
        'value': 4200,
        'shouldIndex': False,
      }],
      'eventMetrics': [{
        'name': 'revenue',
        'value': 4200
      }],
      'timestamp': 42000,
      'layerStates': [{
        'revision': '42',
        'decision': {
          'variationId': '111128',
          'isLayerHoldback': False,
          'experimentId': '111127'
        },
        'actionTriggered': True,
        'layerId': '111182'
      }],
      'accountId': '12001'
    }
    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)

    # Sort event features based on ID
    mock_dispatch_event.call_args[0][0].params['eventFeatures'] = sorted(
      mock_dispatch_event.call_args[0][0].params['eventFeatures'], key=lambda x: x.get('name')
    )
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/event',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_track__with_event_tags_numeric_metric(self):
    """ Test that track calls dispatch_event with right params when only numeric metric
        event tags are provided. """

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'},
                            event_tags={'value': 1.234, 'non-revenue': 'abc'})

    expected_event_metrics_params = [{
      'name': 'value',
      'value': 1.234
    }]

    expected_event_features_params = [{
      'name': 'non-revenue',
      'type': 'custom',
      'value': 'abc',
      'shouldIndex': False,
    }, {
      'name': 'value',
      'type': 'custom',
      'value': 1.234,
      'shouldIndex': False,
    }]

    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)

    # Sort event features based on name
    mock_dispatch_event.call_args[0][0].params['eventFeatures'] = sorted(
      mock_dispatch_event.call_args[0][0].params['eventFeatures'], key=lambda x: x.get('name')
    )
    self._validate_event_object_event_tags(mock_dispatch_event.call_args[0][0],
                                           expected_event_metrics_params,
                                           expected_event_features_params)

  def test_track__with_event_tags__forced_bucketing(self):
    """ Test that track calls dispatch_event with right params when event_value information is provided
    after a forced bucket. """

    with mock.patch('time.time', return_value=42), \
         mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:

      self.assertTrue(self.optimizely.set_forced_variation('test_experiment', 'test_user', 'variation'))
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'},
                            event_tags={'revenue': 4200, 'value': 1.234, 'non-revenue': 'abc'})

    expected_params = {
      'visitorId': 'test_user',
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk',
      'revision': '42',
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'projectId': '111001',
      'isGlobalHoldback': False,
      'eventEntityId': '111095',
      'eventName': 'test_event',
      'eventFeatures': [{
        'name': 'non-revenue',
        'type': 'custom',
        'value': 'abc',
        'shouldIndex': False,
      }, {
        'name': 'revenue',
        'type': 'custom',
        'value': 4200,
        'shouldIndex': False,
      }, {
        'name': 'value',
        'type': 'custom',
        'value': 1.234,
        'shouldIndex': False,
      }],
      'eventMetrics': [{
        'name': 'revenue',
        'value': 4200
      }, {
        'name': 'value',
        'value': 1.234
      }],
      'timestamp': 42000,
      'layerStates': [{
        'revision': '42',
        'decision': {
          'variationId': '111129',
          'isLayerHoldback': False,
          'experimentId': '111127'
        },
        'actionTriggered': True,
        'layerId': '111182'
      }],
      'accountId': '12001'
    }

    self.assertEqual(1, mock_dispatch_event.call_count)

    # Sort event features based on ID
    mock_dispatch_event.call_args[0][0].params['eventFeatures'] = sorted(
      mock_dispatch_event.call_args[0][0].params['eventFeatures'], key=lambda x: x.get('name')
    )
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/event',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_track__with_deprecated_event_value(self):
    """ Test that track calls dispatch_event with right params when event_value information is provided. """

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'}, event_tags=4200)

    expected_params = {
      'visitorId': 'test_user',
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk',
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'projectId': '111001',
      'isGlobalHoldback': False,
      'eventEntityId': '111095',
      'eventName': 'test_event',
      'eventFeatures': [{
        'name': 'revenue',
        'type': 'custom',
        'value': 4200,
        'shouldIndex': False,
      }],
      'eventMetrics': [{
        'name': 'revenue',
        'value': 4200
      }],
      'timestamp': 42000,
      'revision': '42',
      'layerStates': [{
        'revision': '42',
        'decision': {
          'variationId': '111128',
          'isLayerHoldback': False,
          'experimentId': '111127'
        },
        'actionTriggered': True,
        'layerId': '111182'
      }],
      'accountId': '12001'
    }

    # Sort event features based on ID
    mock_dispatch_event.call_args[0][0].params['eventFeatures'] = sorted(
      mock_dispatch_event.call_args[0][0].params['eventFeatures'], key=lambda x: x.get('name')
    )

    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/event',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_track__with_invalid_event_tags(self):
    """ Test that track calls dispatch_event with right params when invalid event tags are provided. """

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111128'
                    )) as mock_get_variation, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user', attributes={'test_attribute': 'test_value'},
                            event_tags={'revenue': '4200', 'value': True})

    expected_params = {
      'visitorId': 'test_user',
      'clientVersion': version.__version__,
      'clientEngine': 'python-sdk',
      'revision': '42',
      'userFeatures': [{
        'shouldIndex': True,
        'type': 'custom',
        'id': '111094',
        'value': 'test_value',
        'name': 'test_attribute'
      }],
      'projectId': '111001',
      'isGlobalHoldback': False,
      'eventEntityId': '111095',
      'eventName': 'test_event',
      'eventFeatures': [{
        'name': 'revenue',
        'type': 'custom',
        'value': '4200',
        'shouldIndex': False,
      }, {
        'name': 'value',
        'type': 'custom',
        'value': True,
        'shouldIndex': False,
      }],
      'eventMetrics': [],
      'timestamp': 42000,
      'layerStates': [{
        'revision': '42',
        'decision': {
          'variationId': '111128',
          'isLayerHoldback': False,
          'experimentId': '111127'
        },
        'actionTriggered': True,
        'layerId': '111182'
      }],
      'accountId': '12001'
    }

    # Sort event features based on ID
    mock_dispatch_event.call_args[0][0].params['eventFeatures'] = sorted(
      mock_dispatch_event.call_args[0][0].params['eventFeatures'], key=lambda x: x.get('name')
    )
    mock_get_variation.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'),
                                               'test_user', {'test_attribute': 'test_value'})
    self.assertEqual(1, mock_dispatch_event.call_count)
    self._validate_event_object(mock_dispatch_event.call_args[0][0], 'https://logx.optimizely.com/log/event',
                                expected_params, 'POST', {'Content-Type': 'application/json'})

  def test_track__experiment_not_running(self):
    """ Test that track does not call dispatch_event when experiment is not running. """

    with mock.patch('optimizely.helpers.experiment.is_experiment_running',
                    return_value=False) as mock_is_experiment_running, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'test_user')

    mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))
    self.assertEqual(0, mock_dispatch_event.call_count)

  def test_track__whitelisted_user_overrides_audience_check(self):
    """ Test that track does not check for user in audience when user is in whitelist. """

    with mock.patch('optimizely.helpers.experiment.is_experiment_running',
                    return_value=True) as mock_is_experiment_running, \
            mock.patch('optimizely.helpers.audience.is_user_in_experiment',
                       return_value=False) as mock_audience_check, \
            mock.patch('time.time', return_value=42), \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event') as mock_dispatch_event:
      self.optimizely.track('test_event', 'user_1')

    mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))
    self.assertEqual(1, mock_dispatch_event.call_count)
    self.assertEqual(0, mock_audience_check.call_count)

  def test_track__invalid_object(self):
    """ Test that track logs error if Optimizely object is not created correctly. """

    opt_obj = optimizely.Optimizely('invalid_file')

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      opt_obj.track('test_event', 'test_user')

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Datafile has invalid format. Failing "track".')

  def test_get_variation__invalid_object(self):
    """ Test that get_variation logs error if Optimizely object is not created correctly. """

    opt_obj = optimizely.Optimizely('invalid_file')

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.assertIsNone(opt_obj.get_variation('test_experiment', 'test_user'))

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Datafile has invalid format. Failing "get_variation".')

class OptimizelyWithExceptionTest(base.BaseTest):

  def setUp(self):
    base.BaseTest.setUp(self)
    self.optimizely = optimizely.Optimizely(json.dumps(self.config_dict),
                                            error_handler=error_handler.RaiseExceptionErrorHandler)

  def test_activate__with_attributes__invalid_attributes(self):
    """ Test that activate raises exception if attributes are in invalid format. """

    self.assertRaisesRegexp(exceptions.InvalidAttributeException, enums.Errors.INVALID_ATTRIBUTE_FORMAT,
                            self.optimizely.activate, 'test_experiment', 'test_user', attributes='invalid')

  def test_track__with_attributes__invalid_attributes(self):
    """ Test that track raises exception if attributes are in invalid format. """

    self.assertRaisesRegexp(exceptions.InvalidAttributeException, enums.Errors.INVALID_ATTRIBUTE_FORMAT,
                            self.optimizely.track, 'test_event', 'test_user', attributes='invalid')

  def test_get_variation__with_attributes__invalid_attributes(self):
    """ Test that get variation raises exception if attributes are in invalid format. """

    self.assertRaisesRegexp(exceptions.InvalidAttributeException, enums.Errors.INVALID_ATTRIBUTE_FORMAT,
                            self.optimizely.get_variation, 'test_experiment', 'test_user', attributes='invalid')


class OptimizelyWithLoggingTest(base.BaseTest):

  def setUp(self):
    base.BaseTest.setUp(self)
    self.optimizely = optimizely.Optimizely(json.dumps(self.config_dict), logger=logger.SimpleLogger())
    self.project_config = self.optimizely.config

  def test_activate(self):
    """ Test that expected log messages are logged during activate. """

    variation_key = 'variation'
    experiment_key = 'test_experiment'
    user_id = 'test_user'

    with mock.patch('optimizely.decision_service.DecisionService.get_variation',
                    return_value=self.project_config.get_variation_from_id(
                      'test_experiment', '111129')), \
         mock.patch('time.time', return_value=42), \
         mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event'), \
         mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.assertEqual(variation_key, self.optimizely.activate(experiment_key, user_id))

    self.assertEqual(2, mock_logging.call_count)
    self.assertEqual(mock.call(enums.LogLevels.INFO, 'Activating user "%s" in experiment "%s".'
                               % (user_id, experiment_key)),
                     mock_logging.call_args_list[0])
    (debug_level, debug_message) = mock_logging.call_args_list[1][0]
    self.assertEqual(enums.LogLevels.DEBUG, debug_level)
    self.assertRegexpMatches(debug_message,
                             'Dispatching impression event to URL https://logx.optimizely.com/log/decision with params')

  def test_track(self):
    """ Test that expected log messages are logged during track. """

    user_id = 'test_user'
    event_key = 'test_event'
    experiment_key = 'test_experiment'

    with mock.patch('optimizely.helpers.audience.is_user_in_experiment',
                    return_value=False), \
         mock.patch('time.time', return_value=42), \
         mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event'), \
         mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.track(event_key, user_id)

    self.assertEqual(4, mock_logging.call_count)
    self.assertEqual(mock.call(enums.LogLevels.DEBUG,
                               'User "%s" is not in the forced variation map.' % user_id),
                     mock_logging.call_args_list[0])
    self.assertEqual(mock.call(enums.LogLevels.INFO,
                               'User "%s" does not meet conditions to be in experiment "%s".'
                               % (user_id, experiment_key)),
                     mock_logging.call_args_list[1])
    self.assertEqual(mock.call(enums.LogLevels.INFO,
                               'Not tracking user "%s" for experiment "%s".' % (user_id, experiment_key)),
                     mock_logging.call_args_list[2])
    self.assertEqual(mock.call(enums.LogLevels.INFO,
                               'There are no valid experiments for event "%s" to track.' % event_key),
                     mock_logging.call_args_list[3])

  def test_activate__experiment_not_running(self):
    """ Test that expected log messages are logged during activate when experiment is not running. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging, \
            mock.patch('optimizely.helpers.experiment.is_experiment_running',
                       return_value=False) as mock_is_experiment_running:
      self.optimizely.activate('test_experiment', 'test_user', attributes={'test_attribute': 'test_value'})

    self.assertEqual(2, mock_logging.call_count)
    self.assertEqual(mock_logging.call_args_list[0],
                     mock.call(enums.LogLevels.INFO, 'Experiment "test_experiment" is not running.'))
    self.assertEqual(mock_logging.call_args_list[1],
                     mock.call(enums.LogLevels.INFO, 'Not activating user "test_user".'))
    mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))

  def test_activate__no_audience_match(self):
    """ Test that expected log messages are logged during activate when audience conditions are not met. """

    experiment_key = 'test_experiment'
    user_id = 'test_user'

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.activate('test_experiment', 'test_user', attributes={'test_attribute': 'wrong_test_value'})

    self.assertEqual(3, mock_logging.call_count)

    self.assertEqual(mock_logging.call_args_list[0],
                     mock.call(enums.LogLevels.DEBUG,
                               'User "%s" is not in the forced variation map.' % user_id))
    self.assertEqual(mock_logging.call_args_list[1],
                     mock.call(enums.LogLevels.INFO,
                               'User "%s" does not meet conditions to be in experiment "%s".'
                               % (user_id, experiment_key)))
    self.assertEqual(mock_logging.call_args_list[2],
                     mock.call(enums.LogLevels.INFO, 'Not activating user "%s".' % user_id))

  def test_activate__dispatch_raises_exception(self):
    """ Test that activate logs dispatch failure gracefully. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging, \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event',
                       side_effect=Exception('Failed to send')):
      self.assertEqual('control', self.optimizely.activate('test_experiment', 'user_1'))

    mock_logging.assert_any_call(enums.LogLevels.ERROR, 'Unable to dispatch impression event. Error: Failed to send')

  def test_track__invalid_attributes(self):
    """ Test that expected log messages are logged during track when attributes are in invalid format. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.track('test_event', 'test_user', attributes='invalid')

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided attributes are in an invalid format.')

  def test_track__deprecated_event_tag(self):
    """ Test that expected log messages are logged during track when attributes are in invalid format. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.track('test_event', 'test_user', event_tags=4200)

    mock_logging.assert_any_call(enums.LogLevels.WARNING,
                                 'Event value is deprecated in track call. '
                                 'Use event tags to pass in revenue value instead.')

  def test_track__invalid_event_tag(self):
    """ Test that expected log messages are logged during track when attributes are in invalid format. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.track('test_event', 'test_user', event_tags='4200')

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided event tags are in an invalid format.')

  def test_track__dispatch_raises_exception(self):
    """ Test that track logs dispatch failure gracefully. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging, \
            mock.patch('optimizely.event_dispatcher.EventDispatcher.dispatch_event',
                       side_effect=Exception('Failed to send')):
      self.optimizely.track('test_event', 'user_1')

    mock_logging.assert_any_call(enums.LogLevels.ERROR, 'Unable to dispatch conversion event. Error: Failed to send')

  def test_get_variation__invalid_attributes(self):
    """ Test that expected log messages are logged during get variation when attributes are in invalid format. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.get_variation('test_experiment', 'test_user', attributes='invalid')

    mock_logging.assert_called_once_with(enums.LogLevels.ERROR, 'Provided attributes are in an invalid format.')

  def test_activate__invalid_attributes(self):
    """ Test that expected log messages are logged during activate when attributes are in invalid format. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.activate('test_experiment', 'test_user', attributes='invalid')

    self.assertEqual(2, mock_logging.call_count)
    self.assertEqual(mock.call(enums.LogLevels.ERROR, 'Provided attributes are in an invalid format.'),
                     mock_logging.call_args_list[0])
    self.assertEqual(mock.call(enums.LogLevels.INFO, 'Not activating user "test_user".'),
                     mock_logging.call_args_list[1])

  def test_get_variation__experiment_not_running(self):
    """ Test that expected log messages are logged during get variation when experiment is not running. """

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging, \
            mock.patch('optimizely.helpers.experiment.is_experiment_running',
                       return_value=False) as mock_is_experiment_running:
      self.optimizely.get_variation('test_experiment', 'test_user', attributes={'test_attribute': 'test_value'})

    mock_logging.assert_called_once_with(enums.LogLevels.INFO, 'Experiment "test_experiment" is not running.')
    mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))

  def test_get_variation__no_audience_match(self):
    """ Test that expected log messages are logged during get variation when audience conditions are not met. """

    experiment_key = 'test_experiment'
    user_id = 'test_user'

    with mock.patch('optimizely.logger.SimpleLogger.log') as mock_logging:
      self.optimizely.get_variation(experiment_key,
                                    user_id,
                                    attributes={'test_attribute': 'wrong_test_value'})

    self.assertEqual(2, mock_logging.call_count)
    self.assertEqual(mock.call(enums.LogLevels.DEBUG, 'User "%s" is not in the forced variation map.' % user_id), \
                     mock_logging.call_args_list[0])

    self.assertEqual(mock.call(enums.LogLevels.INFO, 'User "%s" does not meet conditions to be in experiment "%s".'
                               % (user_id, experiment_key)),
                     mock_logging.call_args_list[1])

  def test_get_variation__forced_bucketing(self):
    """ Test that the expected forced variation is called for a valid experiment and attributes """

    self.assertTrue(self.optimizely.set_forced_variation('test_experiment', 'test_user', 'variation'))
    self.assertEqual('variation', self.optimizely.get_forced_variation('test_experiment', 'test_user'))
    variation_key = self.optimizely.get_variation('test_experiment',
                                                  'test_user',
                                                  attributes={'test_attribute': 'test_value'})
    self.assertEqual('variation', variation_key)

  def test_get_variation__experiment_not_running__forced_bucketing(self):
    """ Test that the expected forced variation is called if an experiment is not running """

    with mock.patch('optimizely.helpers.experiment.is_experiment_running',
                    return_value=False) as mock_is_experiment_running:
      self.optimizely.set_forced_variation('test_experiment', 'test_user', 'variation')
      self.assertEqual('variation', self.optimizely.get_forced_variation('test_experiment', 'test_user'))
      variation_key = self.optimizely.get_variation('test_experiment',
                                                    'test_user',
                                                    attributes={'test_attribute': 'test_value'})
      self.assertIsNone(variation_key)
      mock_is_experiment_running.assert_called_once_with(self.project_config.get_experiment_from_key('test_experiment'))

  def test_get_variation__whitelisted_user_forced_bucketing(self):
    """ Test that the expected forced variation is called if a user is whitelisted """

    self.assertTrue(self.optimizely.set_forced_variation('group_exp_1', 'user_1', 'group_exp_1_variation'))
    forced_variation = self.optimizely.get_forced_variation('group_exp_1', 'user_1')
    self.assertEqual('group_exp_1_variation', forced_variation)
    variation_key = self.optimizely.get_variation('group_exp_1',
                                                  'user_1',
                                                  attributes={'test_attribute': 'test_value'})
    self.assertEqual('group_exp_1_variation', variation_key)

  def test_get_variation__user_profile__forced_bucketing(self):
    """ Test that the expected forced variation is called if a user profile exists """
    with mock.patch('optimizely.decision_service.DecisionService.get_stored_variation',
                    return_value=entities.Variation('111128', 'control')) as mock_get_stored_variation:
      self.assertTrue(self.optimizely.set_forced_variation('test_experiment', 'test_user', 'variation'))
      self.assertEqual('variation', self.optimizely.get_forced_variation('test_experiment', 'test_user'))
      variation_key = self.optimizely.get_variation('test_experiment',
                                                    'test_user',
                                                    attributes={'test_attribute': 'test_value'})
      self.assertEqual('variation', variation_key)

  def test_get_variation__invalid_attributes__forced_bucketing(self):
    """ Test that the expected forced variation is called if the user does not pass audience evaluation """

    self.assertTrue(self.optimizely.set_forced_variation('test_experiment', 'test_user', 'variation'))
    self.assertEqual('variation', self.optimizely.get_forced_variation('test_experiment', 'test_user'))
    variation_key = self.optimizely.get_variation('test_experiment',
                                                  'test_user',
                                                  attributes={'test_attribute': 'test_value_invalid'})
    self.assertEqual('variation', variation_key)
