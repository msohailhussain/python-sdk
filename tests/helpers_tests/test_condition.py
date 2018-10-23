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

conditionA = {
    'name': 'browser_type',
    'value': 'safari',
    'type': 'custom_attribute',
  }

conditionB = {
    'name': 'device_model',
    'value': 'iphone6',
    'type': 'custom_attribute',
  }

conditionC = {
    'name': 'location',
    'match': 'exact',
    'type': 'custom_attribute',
    'value': 'CA',
  }


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

  def test_evaluate__returns_true(self):
    """ Test that evaluate returns True when the leaf condition evaluator returns True. """

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(conditionA, lambda a: True))

  def test_evaluate__returns_false(self):
    """ Test that evaluate returns False when the leaf condition evaluator returns False. """

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(conditionA, lambda a: False))

  def test_and_evaluator__returns_true(self):
    """ Test that and_evaluator returns True when all conditions evaluate to True. """

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: True
    ))

  def test_and_evaluator__returns_false(self):
    """ Test that and_evaluator returns False when any one condition evaluates to False. """

    leafEvaluator = mock.MagicMock(side_effect=[True, False])

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_and_evaluator__returns_null__when_all_null(self):
    """ Test that and_evaluator returns False when any one condition evaluates to False. """

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: None
    ))

  def test_and_evaluator__returns_null__when_trues_and_null(self):
    """ Test that and_evaluator returns False when any one condition evaluates to False. """

    leafEvaluator = mock.MagicMock(side_effect=[True, None])

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

    leafEvaluator = mock.MagicMock(side_effect=[None, True])

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_and_evaluator__returns_false__when_falses_and_null(self):
    """ Test that and_evaluator returns False when any one condition evaluates to False. """

    leafEvaluator = mock.MagicMock(side_effect=[False, None])

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

    leafEvaluator = mock.MagicMock(side_effect=[None, False])

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_and_evaluator__returns_false__when_trues_falses_and_null(self):
    """ Test that and_evaluator returns False when any one condition evaluates to False. """

    leafEvaluator = mock.MagicMock(side_effect=[True, False, None])

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['and', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_or_evaluator__returns_true__when_any_true(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    leafEvaluator = mock.MagicMock(side_effect=[False, True])

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_or_evaluator__returns_false__when_all_false(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: False
    ))

  def test_or_evaluator__returns_null__when_all_null(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: None
    ))

  def test_or_evaluator__returns_true__when_trues_and_null(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    leafEvaluator = mock.MagicMock(side_effect=[None, True])

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

    leafEvaluator = mock.MagicMock(side_effect=[True, None])

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_or_evaluator__returns_null__when_falses_and_null(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    leafEvaluator = mock.MagicMock(side_effect=[False, None])

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

    leafEvaluator = mock.MagicMock(side_effect=[None, False])

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

  def test_or_evaluator__returns_true__when_trues_falses_and_null(self):
    """ Test that or_evaluator returns True when any one condition evaluates to True. """

    leafEvaluator = mock.MagicMock(side_effect=[False, None, True])

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['or', conditionA, conditionB, conditionC],
      lambda a: leafEvaluator()
    ))

  def test_not_evaluator__returns_true(self):
    """ Test that not_evaluator returns True when condition evaluates to False. """

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['not', conditionA],
      lambda a: False
    ))

  def test_not_evaluator__returns_false(self):
    """ Test that not_evaluator returns True when condition evaluates to False. """

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['not', conditionA],
      lambda a: True
    ))

  def test_not_evaluator_negates_first_condition__ignores_rest(self):
    """ Test that not_evaluator returns True when condition evaluates to False. """
    leafEvaluator = mock.MagicMock(side_effect=[False, True, None])

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      ['not', conditionA, conditionB, conditionC],
      lambda a: leafEvaluator()
    ))

    leafEvaluator = mock.MagicMock(side_effect=[True, False, None])

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      ['not', conditionA, conditionB, conditionC],
      lambda a: leafEvaluator()
    ))

    leafEvaluator = mock.MagicMock(side_effect=[None, True, False])

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['not', conditionA, conditionB, conditionC],
      lambda a: leafEvaluator()
    ))

  def test_not_evaluator__returns_null__when_null(self):
    """ Test that not_evaluator returns True when condition evaluates to False. """

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['not', conditionA],
      lambda a: None
    ))

  def test_not_evaluator__returns_null__when_there_are_no_operands(self):
    """ Test that not_evaluator returns True when condition evaluates to False. """

    self.assertIsNone(self.condition_tree_evaluator.evaluate(
      ['not'],
      lambda a: True
    ))

  def test_evaluate_assumes__OR_operator__when_first_item_in_array_not_recognized_operator(self):

    leafEvaluator = mock.MagicMock(side_effect=[False, True])

    self.assertStrictTrue(self.condition_tree_evaluator.evaluate(
      [conditionA, conditionB],
      lambda a: leafEvaluator()
    ))

    self.assertStrictFalse(self.condition_tree_evaluator.evaluate(
      [conditionA, conditionB],
      lambda a: False
    ))


class ConditionDecoderTests(base.BaseTest):

  def test_loads(self):
    """ Test that loads correctly sets condition structure and list. """

    condition_structure, condition_list = condition_helper.loads(
      self.config_dict['audiences'][0]['conditions']
    )

    self.assertEqual(['and', ['or', ['or', 0]]], condition_structure)
    self.assertEqual([['test_attribute', 'test_value_1', 'custom_attribute', 'exact']], condition_list)
