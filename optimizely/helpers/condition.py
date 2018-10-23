# Copyright 2016, 2018, Optimizely
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

import json
import math
import numbers

from six import string_types

CUSTOM_ATTRIBUTE_CONDITION_TYPE = 'custom_attribute'

class ConditionOperatorTypes(object):
  AND = 'and'
  OR = 'or'
  NOT = 'not'


class ConditionMatchTypes(object):
  EXACT = 'exact'
  EXISTS = 'exists'
  GREATER_THAN = 'gt'
  LESS_THAN = 'lt'
  SUBSTRING = 'substring'


class ConditionTreeEvaluator(object):
  """ Class encapsulating methods to be used in audience condition evaluation. """

  def and_evaluator(self, conditions, leaf_evaluator):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to each entry and the results AND-ed together

    Args:
      conditions: List of conditions ex: [operand_1, operand_2]

    Returns:
      Boolean: True if all operands evaluate to True
    """
    saw_null_result = False

    for condition in conditions:
      result = self.evaluate(condition, leaf_evaluator)
      if result is False:
        return False
      if result is None:
        saw_null_result = True

    return None if saw_null_result else True

  def or_evaluator(self, conditions, leaf_evaluator):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to each entry and the results OR-ed together

    Args:
      conditions: List of conditions ex: [operand_1, operand_2]

    Returns:
      Boolean: True if any operand evaluates to True
    """
    saw_null_result = False

    for condition in conditions:
      result = self.evaluate(condition, leaf_evaluator)
      if result is True:
        return True
      if result is None:
        saw_null_result = True

    return None if saw_null_result else False

  def not_evaluator(self, single_condition, leaf_evaluator):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to a single entry and NOT was applied to the result.

    Args:
      single_condition: List of of a single condition ex: [operand_1]

    Returns:
      Boolean: True if the operand evaluates to False
    """
    if not len(single_condition) > 0:
      return None

    result = self.evaluate(single_condition[0], leaf_evaluator)
    return None if result is None else not result

  DEFAULT_OPERATOR_TYPES = [
    ConditionOperatorTypes.AND,
    ConditionOperatorTypes.OR,
    ConditionOperatorTypes.NOT
  ]

  EVALUATORS_BY_OPERATOR_TYPE = {
    ConditionOperatorTypes.AND: and_evaluator,
    ConditionOperatorTypes.OR: or_evaluator,
    ConditionOperatorTypes.NOT: not_evaluator
  }

  def evaluate(self, conditions, leaf_evaluator):

    if isinstance(conditions, list):
      if conditions[0] in self.DEFAULT_OPERATOR_TYPES:
        return self.EVALUATORS_BY_OPERATOR_TYPE[conditions[0]](self, conditions[1:], leaf_evaluator)
      else:
        # assume OR when operator is not explicit
        return self.EVALUATORS_BY_OPERATOR_TYPE[ConditionOperatorTypes.OR](self, conditions, leaf_evaluator)

    leaf_condition = conditions
    return leaf_evaluator(leaf_condition)


class CustomAttributeConditionEvaluator(object):

  MATCH_TYPES = [
    ConditionMatchTypes.EXACT,
    ConditionMatchTypes.EXISTS,
    ConditionMatchTypes.GREATER_THAN,
    ConditionMatchTypes.LESS_THAN,
    ConditionMatchTypes.SUBSTRING
  ]

  def __init__(self, condition_data, attributes):
    self.condition_data = condition_data
    self.attributes = attributes or {}

  def is_finite(self, value):
    if not isinstance(value, (numbers.Integral, float)):
      return False

    if math.isnan(value) or match.isinf(value):
      return False

    return True


  def is_value_valid_for_exact_conditions(self, value):
    if isinstance(value, string_types) or isinstance(value, bool) or self.is_finite(value):
      return True
      
    return False

  def exact_evaluator(self, condition):
    condition_value = self.condition_data[condition][1]
    condition_value_type = type(condition_value)

    user_value = self.attributes.get(self.condition_data[condition][0])
    user_value_type = type(user_value)

    if not self.is_value_valid_for_exact_conditions(condition_value) or \
       not self.is_value_valid_for_exact_conditions(user_value) or \
            condition_value_type != user_value_type:
      return None

    return condition_value == user_value

  def exists_evaluator(self, condition):
    attr_name = self.condition_data[condition][0]
    return self.attributes.get(attr_name) is not None

  def greater_than_evaluator(self, condition):
    condition_value = self.condition_data[condition][1]
    user_value = self.attributes.get(self.condition_data[condition][0])

    if not self.is_finite(condition_value) or not self.is_finite(user_value):
      return None

    return user_value > condition_value

  def less_than_evaluator(self, condition):
    condition_value = self.condition_data[condition][1]
    user_value = self.attributes.get(self.condition_data[condition][0])

    if not self.is_finite(condition_value) or not self.is_finite(user_value):
      return None

    return user_value < condition_value

  def substring_evaluator(self, condition):
    condition_value = self.condition_data[condition][1]
    user_value = self.attributes.get(self.condition_data[condition][0])

    if not isinstance(condition_value, string_types) or not isinstance(user_value, string_types):
      return None

    return condition_value in user_value

  EVALUATORS_BY_MATCH_TYPE = {
    ConditionMatchTypes.EXACT: exact_evaluator,
    ConditionMatchTypes.EXISTS: exists_evaluator,
    ConditionMatchTypes.GREATER_THAN: greater_than_evaluator,
    ConditionMatchTypes.LESS_THAN: less_than_evaluator,
    ConditionMatchTypes.SUBSTRING: substring_evaluator
  }

  def evaluate(self, condition):
    """ Top level method to evaluate audience conditions.
    Args:
      conditions: Nested list of and/or conditions.
                  Ex: ['and', operand_1, ['or', operand_2, operand_3]]
    Returns:
      Boolean result of evaluating the conditions evaluate
    """

    if self.condition_data[condition][2] != CUSTOM_ATTRIBUTE_CONDITION_TYPE:
      return null

    condition_match = self.condition_data[condition][3]

    if condition_match not in self.MATCH_TYPES:
      return null

    return self.EVALUATORS_BY_MATCH_TYPE[condition_match](self, condition)

class ConditionDecoder(object):
  """ Class which provides an object_hook method for decoding dict
  objects into a list when given a condition_decoder. """

  def __init__(self, condition_decoder):
    self.condition_list = []
    self.index = -1
    self.decoder = condition_decoder

  def object_hook(self, object_dict):
    """ Hook which when passed into a json.JSONDecoder will replace each dict
    in a json string with its index and convert the dict to an object as defined
    by the passed in condition_decoder. The newly created condition object is
    appended to the conditions_list.

    Args:
      object_dict: Dict representing an object.

    Returns:
      An index which will be used as the placeholder in the condition_structure
    """
    instance = self.decoder(object_dict)
    self.condition_list.append(instance)
    self.index += 1
    return self.index


def _audience_condition_deserializer(obj_dict):
  """ Deserializer defining how dict objects need to be decoded for audience conditions.

  Args:
    obj_dict: Dict representing one audience condition.

  Returns:
    List consisting of condition key and corresponding value.
  """
  return [
    obj_dict.get('name'),
    obj_dict.get('value'),
    obj_dict.get('type'),
    obj_dict.get('match', ConditionMatchTypes.EXACT)
  ]


def loads(conditions_string):
  """ Deserializes the conditions property into its corresponding
  components: the condition_structure and the condition_list.

  Args:
    conditions_string: String defining valid and/or conditions.

  Returns:
    A tuple of (condition_structure, condition_list).
    condition_structure: nested list of operators and placeholders for operands.
    condition_list: list of conditions whose index correspond to the values of the placeholders.
  """
  decoder = ConditionDecoder(_audience_condition_deserializer)

  # Create a custom JSONDecoder using the ConditionDecoder's object_hook method
  # to create the condition_structure as well as populate the condition_list
  json_decoder = json.JSONDecoder(object_hook=decoder.object_hook)

  # Perform the decoding
  condition_structure = json_decoder.decode(conditions_string)
  condition_list = decoder.condition_list

  return (condition_structure, condition_list)
