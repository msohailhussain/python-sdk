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


class ConditionTreeEvaluatorTests(base.BaseTest):

  def setUp(self):
    base.BaseTest.setUp(self)
    self.condition_structure, self.condition_list = condition_helper.loads(
      self.config_dict['audiences'][0]['conditions']
    )
    attributes = {
      'test_attribute': 'test_value_1',
      'browser_type': 'firefox',
      'location': 'San Francisco'
    }

    self.condition_tree_evaluator = condition_helper.ConditionTreeEvaluator()

    self.conditionA = {
      'name': 'browser_type',
      'value': 'safari',
      'type': 'custom_attribute',
    };

    self.conditionB = {
      'name': 'device_model',
      'value': 'iphone6',
      'type': 'custom_attribute',
    };

    self.conditionC = {
      'name': 'location',
      'match': 'exact',
      'type': 'custom_attribute',
      'value': 'CA',
    };

  def test_evaluate__returns_true(self):
    """ Test that evaluate returns True when the leaf condition evaluator returns True. """

    self.assertTrue(self.condition_tree_evaluator.evaluate(self.conditionA, lambda a: True))

  def test_evaluate__returns_false(self):
    """ Test that evaluate returns False when the leaf condition evaluator returns False. """

    self.assertFalse(self.condition_tree_evaluator.evaluate(self.conditionA, lambda a: False))

#   def test_and_evaluator__returns_true(self):
#     """ Test that and_evaluator returns True when all conditions evaluate to True. """

#     conditions = range(5)

#     with mock.patch('optimizely.helpers.condition.ConditionTreeEvaluator.evaluate', return_value=True):
#       self.assertTrue(self.condition_tree_evaluator.and_evaluator(conditions, None))

#   def test_and_evaluator__returns_false(self):
#     """ Test that and_evaluator returns False when any one condition evaluates to False. """

#     conditions = range(5)

#     with mock.patch('optimizely.helpers.condition.ConditionTreeEvaluator.evaluate',
#                     side_effect=[True, True, False, True, True]):
#       self.assertFalse(self.condition_tree_evaluator.and_evaluator(conditions, None))

#   def test_or_evaluator__returns_true(self):
#     """ Test that or_evaluator returns True when any one condition evaluates to True. """

#     conditions = range(5)

#     with mock.patch('optimizely.helpers.condition.ConditionTreeEvaluator.evaluate',
#                     side_effect=[False, False, True, False, False]):
#       self.assertTrue(self.condition_tree_evaluator.or_evaluator(conditions, None))

#   def test_or_evaluator__returns_false(self):
#     """ Test that or_evaluator returns False when all conditions evaluator to False. """

#     conditions = range(5)

#     with mock.patch('optimizely.helpers.condition.ConditionTreeEvaluator.evaluate', return_value=False):
#       self.assertFalse(self.condition_tree_evaluator.or_evaluator(conditions, None))

#   def test_not_evaluator__returns_true(self):
#     """ Test that not_evaluator returns True when condition evaluates to False. """

#     with mock.patch('optimizely.helpers.condition.ConditionTreeEvaluator.evaluate', return_value=False):
#       self.assertTrue(self.condition_tree_evaluator.not_evaluator([42], None))

#   def test_not_evaluator__returns_false(self):
#     """ Test that not_evaluator returns False when condition evaluates to True. """

#     with mock.patch('optimizely.helpers.condition.ConditionTreeEvaluator.evaluate', return_value=True):
#       self.assertFalse(self.condition_tree_evaluator.not_evaluator([42], None))

#   def test_not_evaluator__returns_false_more_than_one_condition(self):
#     """ Test that not_evaluator returns False when list has more than 1 condition. """

#     self.assertFalse(self.condition_tree_evaluator.not_evaluator([42, 43], None))


# class ConditionDecoderTests(base.BaseTest):

#   def test_loads(self):
#     """ Test that loads correctly sets condition structure and list. """

#     condition_structure, condition_list = condition_helper.loads(
#       self.config_dict['audiences'][0]['conditions']
#     )

#     self.assertEqual(['and', ['or', ['or', 0]]], condition_structure)
#     self.assertEqual([['test_attribute', 'test_value_1', 'custom_attribute', 'exact']], condition_list)
