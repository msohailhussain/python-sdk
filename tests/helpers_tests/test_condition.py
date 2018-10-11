# Copyright 2016-2018, Optimizely
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from optimizely.helpers import condition as condition_helper

from tests import base


class ConditionEvaluatorTests(base.BaseTest):

  def setUp(self):
    base.BaseTest.setUp(self)
    self.condition_list = condition_helper.ConditionDecoder.deserialize_audience_conditions(
      self.config_dict['audiences'][0]['conditions']
    )

    self.exact_browser_condition = {'name': 'browser_type', 'match': 'exact', 'type': 'custom_attribute', 'value': 'firefox'}
    self.exact_device_condition = {'name': 'device', 'match': 'exact', 'type': 'custom_attribute', 'value': 'iphone'}
    self.exact_location_condition = {'name': 'location', 'match': 'exact', 'type': 'custom_attribute', 'value': 'san francisco'}
    self.exact_string_conditions = {'match': 'exact', 'name': 'location', 'type': 'custom_attribute', 'value': 'san francisco'}

    self.exists_conditions = {'match': 'exists', 'name': 'input_value', 'type': 'custom_attribute'}

    attributes = {
      'test_attribute': 'test_value_1',
      'browser_type': 'firefox',
      'location': 'San Francisco'
    }
    self.condition_evaluator = condition_helper.ConditionEvaluator(attributes)

  def test_evaluator__returns_true(self):
    """ Test that evaluator correctly returns True when there is an exact match.
    Also test that evaluator works for falsy values. """

    # string attribute value
    condition_list = {'type': 'custom_attribute', 'name': 'test_attribute', 'value': ''}
    condition_evaluator = condition_helper.ConditionEvaluator({'test_attribute': ''})
    self.assertTrue(condition_evaluator.evaluator(condition_list))

    # boolean attribute value
    condition_list = {'type': 'custom_attribute', 'name': 'boolean_key', 'value': False}
    condition_evaluator = condition_helper.ConditionEvaluator({'boolean_key': False})
    self.assertTrue(condition_evaluator.evaluator(condition_list))

    # integer attribute value
    condition_list = {'type': 'custom_attribute', 'name': 'integer_key', 'value': 0}
    condition_evaluator = condition_helper.ConditionEvaluator({'integer_key': 0})
    self.assertTrue(condition_evaluator.evaluator(condition_list))

    # double attribute value
    condition_list = {'type': 'custom_attribute', 'name': 'double_key', 'value': 0.0}
    condition_evaluator = condition_helper.ConditionEvaluator({'double_key': 0.0})
    self.assertTrue(condition_evaluator.evaluator(condition_list))

  def test_evaluator__returns_false(self):
    """ Test that evaluator correctly returns False when there is no match. """
    condition_list = {'type': 'custom_attribute', 'name': 'browser_type', 'value': 'firefox'}
    attributes = {
      'browser_type': 'chrome',
      'location': 'San Francisco'
    }
    condition_evaluator = condition_helper.ConditionEvaluator(attributes)

    self.assertFalse(condition_evaluator.evaluator(condition_list))

  def test_and_evaluator__returns_true(self):
    """ Test that and_evaluator returns True when all conditions evaluate to True. """

    conditions = range(5)

    with mock.patch('optimizely.helpers.condition.ConditionEvaluator.evaluate', return_value=True):
      self.assertTrue(self.condition_evaluator.and_evaluator(conditions))

  def test_and_evaluator__returns_false(self):
    """ Test that and_evaluator returns False when any one condition evaluates to False. """

    conditions = range(5)

    with mock.patch('optimizely.helpers.condition.ConditionEvaluator.evaluate',
                    side_effect=[True, True, False, True, True]):
      self.assertFalse(self.condition_evaluator.and_evaluator(conditions))

  def test_or_evaluator__returns_true(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    conditions = range(5)

    with mock.patch('optimizely.helpers.condition.ConditionEvaluator.evaluate',
                    side_effect=[False, False, True, False, False]):
      self.assertTrue(self.condition_evaluator.or_evaluator(conditions))

  def test_or_evaluator__returns_false(self):
    """ Test that or_evaluator returns False when all conditions evaluator to False. """

    conditions = range(5)

    with mock.patch('optimizely.helpers.condition.ConditionEvaluator.evaluate', return_value=False):
      self.assertFalse(self.condition_evaluator.or_evaluator(conditions))

  def test_not_evaluator__returns_true(self):
    """ Test that not_evaluator returns True when condition evaluates to False. """

    with mock.patch('optimizely.helpers.condition.ConditionEvaluator.evaluate', return_value=False):
      self.assertTrue(self.condition_evaluator.not_evaluator([42]))

  def test_not_evaluator__returns_false(self):
    """ Test that not_evaluator returns False when condition evaluates to True. """

    with mock.patch('optimizely.helpers.condition.ConditionEvaluator.evaluate', return_value=True):
      self.assertFalse(self.condition_evaluator.not_evaluator([42]))

  def test_not_evaluator__returns_false_none_condition(self):
    """ Test that not_evaluator returns False when list is empty. """

    self.assertFalse(self.condition_evaluator.not_evaluator([]))

  def test_evaluate__returns_true(self):
    """ Test that evaluate returns True when conditions evaluate to True. """

    self.assertTrue(self.condition_evaluator.evaluate(self.condition_list))

  def test_evaluate__returns_false(self):
    """ Test that evaluate returns False when conditions evaluate to False. """

    condition_structure = {"name": "test_attribute", "type": "custom_attribute", "value": "test_value_x"}
    self.assertFalse(self.condition_evaluator.evaluate(condition_structure))

  def test_evaluate__returns_none(self):
    """ Test that evaluate returns None when conditions evaluate to False. """

    # Invalid type
    condition_structure = {'match': 'exact', 'name': 'test_attribute', 'type': 'invalid', 'value': 'test_value_1'}
    self.assertIsNone(self.condition_evaluator.evaluate(condition_structure))

    # Invalid match
    condition_structure = {'match': 'invalid', 'name': 'test_attribute', 'type': 'custom_attribute', 'value': 'test_value_1'}
    self.assertIsNone(self.condition_evaluator.evaluate(condition_structure))

  def test_evaluation__and_evaluation__returns_none_when_operands_evaluate_to_none(self):
    """ Test that evaluate returns None when all operands evaluate to None. """

    attributes = {
      'browser_type': 4.5,
      'location': False
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertIsNone(condition_evaluator.evaluate(['and', self.exact_browser_condition, self.exact_location_condition]))

  def test_evaluation__and_evaluation__returns_none_when_operands_evaluate_to_true_and_none(self):
    """ Test that evaluate returns None when operands evaluate to True and None. """

    attributes = {
      'browser_type': 'firefox',
      'location': False
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertIsNone(condition_evaluator.evaluate(['and', self.exact_browser_condition, self.exact_location_condition]))

  def test_evaluation__and_evaluation__returns_false_when_operands_evaluate_to_false_and_none(self):
    """ Test that evaluate returns False when operands evaluate to False and None. """

    attributes = {
      'browser_type': 'chrome',
      'location': False
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertFalse(condition_evaluator.evaluate(['and', self.exact_browser_condition, self.exact_location_condition]))

  def test_evaluation__and_evaluation__returns_false_when_operands_evaluate_to_true_false_and_none(self):
    """ Test that evaluate returns False when operands evaluate to True, False and None. """

    attributes = {
      'browser_type': 'chrome',
      'device': 'android',
      'location': False
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertFalse(condition_evaluator.evaluate([
      'and',
      self.exact_browser_condition,
      self.exact_device_condition,
      self.exact_location_condition
    ]))

  def test_evaluation__or_evaluation__returns_none_when_operands_evaluate_to_none(self):
    """ Test that evaluate returns None when all operands evaluate to None. """

    attributes = {
      'browser_type': 4.5,
      'location': False
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertIsNone(condition_evaluator.evaluate(['or', self.exact_browser_condition, self.exact_location_condition]))

  def test_evaluation__or_evaluation__returns_true_when_operands_evaluate_to_true_and_none(self):
    """ Test that evaluate returns None when operands evaluate to True and None. """

    attributes = {
      'browser_type': False,
      'location': 'san francisco'
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertTrue(condition_evaluator.evaluate(['or', self.exact_browser_condition, self.exact_location_condition]))

  def test_evaluation__or_evaluation__returns_false_when_operands_evaluate_to_false_and_none(self):
    """ Test that evaluate returns False when operands evaluate to False and None. """

    attributes = {
      'browser_type': 'chrome',
      'location': False
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertFalse(condition_evaluator.evaluate(['or', self.exact_browser_condition, self.exact_location_condition]))

  def test_evaluation__or_evaluation__returns_true_when_operands_evaluate_to_true_false_and_none(self):
    """ Test that evaluate returns True when operands evaluate to True, False and None. """

    attributes = {
      'browser_type': False,
      'device': 'android',
      'location': 'san francisco'
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertTrue(condition_evaluator.evaluate([
      'or',
      self.exact_browser_condition,
      self.exact_device_condition,
      self.exact_location_condition
    ]))

  def test_evaluation__not_evaluation__returns_none_when_operands_evaluate_to_none(self):
    """ Test that evaluate returns None when all operands evaluate to None. """

    attributes = { 'browser_type': 4.5 }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertIsNone(condition_evaluator.evaluate(['not' , self.exact_browser_condition]))

  def test_evaluation__implicit_operator__returns_none_when_unsupported_operands_provided(self):
    """ Test that evaluater behaves like an "or" operator when the first item in the array
      is not a recognized operator """

    attributes = {
      'browser_type': 'chrome',
      'device': 'iphone'
    }

    condition_evaluator = condition_helper.ConditionEvaluator(attributes)
    self.assertTrue(condition_evaluator.evaluate([self.exact_browser_condition, self.exact_device_condition]))

  def test_evaluation__exists_match_type__returns_false_when_none_user_value(self):
    """ Test that evaluater returns False when no user value provided."""

    condition_evaluator = condition_helper.ConditionEvaluator({})
    self.assertFalse(condition_evaluator.evaluate(['and', self.exists_conditions]))

  def test_evaluation__exists_match_type__returns_false_when_none_user_value(self):
    """ Test that evaluater returns False when no user is None."""

    condition_evaluator = condition_helper.ConditionEvaluator({'input_value': None})
    self.assertFalse(condition_evaluator.evaluate(['and', self.exists_conditions]))

  # def test_evaluation__exists_match_type__returns_false_when_string_user_value(self):
  #   """ Test that evaluater returns False when no user is String."""
  #
  #   condition_evaluator = condition_helper.ConditionEvaluator({'input_value': 'test'})
  #   self.assertTrue(condition_evaluator.evaluate(['and', self.exists_conditions]))
  #
  # def test_evaluation__exists_match_type__returns_false_when_number_user_value(self):
  #   """ Test that evaluater returns False when no user is Number."""
  #
  #   condition_evaluator = condition_helper.ConditionEvaluator({'input_value': 5})
  #   self.assertFalse(condition_evaluator.evaluate(['and', self.exists_conditions]))
  #
  # def test_evaluation__exists_match_type__returns_false_when_boolean_user_value(self):
  #   """ Test that evaluater returns False when no user is Number."""
  #
  #   condition_evaluator = condition_helper.ConditionEvaluator({'input_value': True})
  #   self.assertFalse(condition_evaluator.evaluate(['and', self.exists_conditions]))


class ConditionDecoderTests(base.BaseTest):

  def test_deserialize_audience_conditions(self):
    """ Test that deserialize_audience_conditions correctly sets condition list. """

    condition_list = condition_helper.ConditionDecoder.deserialize_audience_conditions(
      self.config_dict['audiences'][0]['conditions']
    )

    self.assertEqual(
      ['and', ['or', ['or', {"name": "test_attribute", "type": "custom_attribute", "value": "test_value_1"}]]],
      condition_list
    )
