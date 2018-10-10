# Copyright 2016,2018, Optimizely
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
from six import string_types


class ConditionalOperatorTypes(object):
  AND = 'and'
  OR = 'or'
  NOT = 'not'


class ConditionalMatchTypes(object):
  EXACT = 'exact'
  EXISTS = 'exists'
  GREATER_THAN = 'gt'
  LESS_THAN = 'lt'
  SUBSTRING = 'substring'

DEFAULT_OPERATOR_TYPES = [
  ConditionalOperatorTypes.AND,
  ConditionalOperatorTypes.OR,
  ConditionalOperatorTypes.NOT
]

CUSTOM_ATTRIBUTE_CONDITION_TYPE = 'custom_attribute'

MATCH_TYPES = [
  ConditionalMatchTypes.EXACT,
  ConditionalMatchTypes.EXISTS,
  ConditionalMatchTypes.GREATER_THAN,
  ConditionalMatchTypes.LESS_THAN,
  ConditionalMatchTypes.SUBSTRING
]

class ConditionEvaluator(object):
  """ Class encapsulating methods to be used in audience condition evaluation. """

  def __init__(self, attributes):
    self.attributes = attributes

  def evaluator(self, condition):
    """ Method to compare single audience condition against provided user data i.e. attributes.

    Args:
      condition: Dict representing audience condition name, value, type etc.

    Returns:
      Boolean indicating the result of comparing the condition value against the user attributes.
    """

    return self.attributes.get(condition['name']) == condition['value']

  def and_evaluator(self, conditions):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to each entry and the results AND-ed together

    Args:
      conditions: List of conditions ex: [operand_1, operand_2]

    Returns:
      Boolean: True if all operands evaluate to True
    """

    found_none = False

    for condition in conditions:
      result = self.evaluate(condition)
      if result is False:
        return False

      if result is None:
        found_none = True

    return None if found_none == True else True

  def or_evaluator(self, conditions):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to each entry and the results OR-ed together

    Args:
      conditions: List of conditions ex: [operand_1, operand_2]

    Returns:
      Boolean: True if any operand evaluates to True
    """

    found_none = False
    for condition in conditions:
      result = self.evaluate(condition)
      if result is True:
        return True

      if result is None:
        found_none = True

    return None if found_none == True else False

  def not_evaluator(self, conditions):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to a single entry and NOT was applied to the result.

    Args:
      single_condition: List of of a single condition ex: [operand_1]

    Returns:
      Boolean: True if the operand evaluates to False
    """
    if not len(conditions) > 0:
      return False
    result = self.evaluate(conditions[0])

    return None if result == None else not result


  def exact_evaluator(self, leaf_condition):
    condition_value = leaf_condition['value']
    condition_value_type = type(condition_value.encode('utf8'))

    user_provided_value = self.attributes.get(leaf_condition['name'])
    user_provided_value_type = type(user_provided_value)

    if not self.is_value_valid_for_exact_conditions(condition_value) or \
       not self.is_value_valid_for_exact_conditions(user_provided_value) or \
            condition_value_type != user_provided_value_type:
      return None

    return condition_value == user_provided_value


  def exists_evaluator(self, leaf_condition):
    if not attributes:
        return False
    return leaf_condition[leaf_condition['name']] is not None

  def greater_than_evaluator(self, leaf_condition):
    condition_value = leaf_condition['value']
    user_provided_value = self.attributes.get(leaf_condition['name'])

    if not math.isfinite(condition_value) or not math.isfinite(user_provided_value):
      return None

    return user_provided_value > condition_value

  def less_than_evaluator(self, leaf_condition):
    condition_value = leaf_condition['value']
    user_provided_value = self.attributes.get(leaf_condition['name'])

    if not math.isfinite(condition_value) or not math.isfinite(user_provided_value):
      return None

    return user_provided_value < condition_value

  def substring_evaluator(self, leaf_condition):
    condition_value = leaf_condition['value']
    user_provided_value = self.attributes.get(leaf_condition['name'])

    if not isinstance(condition_value, string_types) or not isinstance(user_provided_value, string_types):
      return None

    return condition_value in user_provided_value

  DEFAULT_OPERATORS = {
    ConditionalOperatorTypes.AND: and_evaluator,
    ConditionalOperatorTypes.OR: or_evaluator,
    ConditionalOperatorTypes.NOT: not_evaluator
  }

  EVALUATORS_BY_MATCH_TYPE = {
    ConditionalMatchTypes.EXACT: exact_evaluator,
    ConditionalMatchTypes.EXISTS: exists_evaluator,
    ConditionalMatchTypes.GREATER_THAN: greater_than_evaluator,
    ConditionalMatchTypes.LESS_THAN: less_than_evaluator,
    ConditionalMatchTypes.SUBSTRING: substring_evaluator
  }

  def evaluate(self, conditions):
    """ Top level method to evaluate audience conditions.

    Args:
      conditions: Nested list of and/or conditions.
                  Ex: ['and', operand_1, ['or', operand_2, operand_3]]

    Returns:
      Boolean result of evaluating the conditions evaluate
    """

    if isinstance(conditions, list):

      if conditions[0] in DEFAULT_OPERATOR_TYPES:
        return self.DEFAULT_OPERATORS[conditions[0]](self, conditions[1:])
      else:
        return self.DEFAULT_OPERATORS[ConditionalOperatorTypes.OR](self, conditions)

    if 'type' in conditions and conditions['type'] != CUSTOM_ATTRIBUTE_CONDITION_TYPE:
      return None

    if 'match' in conditions and conditions['match'] not in MATCH_TYPES:
      return None

    if 'match' in conditions:
      return self.EVALUATORS_BY_MATCH_TYPE[conditions['match']](self, conditions)
    else:
      return self.EVALUATORS_BY_MATCH_TYPE[ConditionalMatchTypes.EXACT](self, conditions)



  def is_value_valid_for_exact_conditions(self, value):
    return isinstance(value, string_types) or isinstance(value, bool) or math.isfinite(value)


class ConditionDecoder(object):
  """ Class encapsulating methods to be used in audience condition decoding. """

  @staticmethod
  def deserialize_audience_conditions(conditions_string):
    """ Deserializes the conditions property into a list of structures and conditions.

    Args:
      conditions_string: String defining valid and/or conditions.

    Returns:
      list of conditions.
    """

    return json.loads(conditions_string)
