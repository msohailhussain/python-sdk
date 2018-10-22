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

from six import string_types


CUSTOM_ATTRIBUTE_CONDITION_TYPE = 'custom_attribute'


class ConditionalOperatorTypes(object):
  AND = 'and'
  OR = 'or'
  NOT = 'not'

DEFAULT_OPERATOR_TYPES = [
  ConditionalOperatorTypes.AND,
  ConditionalOperatorTypes.OR,
  ConditionalOperatorTypes.NOT
]


class ConditionalMatchTypes(object):
  EXACT = 'exact'
  EXISTS = 'exists'
  GREATER_THAN = 'gt'
  LESS_THAN = 'lt'
  SUBSTRING = 'substring'

MATCH_TYPES = [
  ConditionalMatchTypes.EXACT,
  ConditionalMatchTypes.EXISTS,
  ConditionalMatchTypes.GREATER_THAN,
  ConditionalMatchTypes.LESS_THAN,
  ConditionalMatchTypes.SUBSTRING
]


class ConditionEvaluator(object):
  """ Class encapsulating methods to be used in audience condition evaluation. """

  def __init__(self, condition_data, attributes):
    self.condition_data = condition_data
    self.attributes = attributes

  def and_evaluator(self, conditions):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to each entry and the results AND-ed together

    Args:
      conditions: List of conditions ex: [operand_1, operand_2]

    Returns:
      Boolean: True if all operands evaluate to True
    """

    for condition in conditions:
      result = self.evaluate(condition)
      if result is False:
        return False

    return True

  def or_evaluator(self, conditions):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to each entry and the results OR-ed together

    Args:
      conditions: List of conditions ex: [operand_1, operand_2]

    Returns:
      Boolean: True if any operand evaluates to True
    """

    for condition in conditions:
      result = self.evaluate(condition)
      if result is True:
        return True

    return False

  def not_evaluator(self, single_condition):
    """ Evaluates a list of conditions as if the evaluator had been applied
    to a single entry and NOT was applied to the result.

    Args:
      single_condition: List of of a single condition ex: [operand_1]

    Returns:
      Boolean: True if the operand evaluates to False
    """
    if len(single_condition) != 1:
      return False

    return not self.evaluate(single_condition[0])

  def is_value_valid_for_exact_conditions(self, value):
    return isinstance(value, string_types) or isinstance(value, bool)
    return math.isfinite(value)

  def exact_evaluator(self, condition):
    condition_value = self.condition_data[condition][1]
    condition_value_type = type(condition_value.encode('utf8'))

    user_provided_value = self.attributes.get(self.condition_data[condition][0])
    user_provided_value_type = type(user_provided_value)

    if not self.is_value_valid_for_exact_conditions(condition_value) or \
       not self.is_value_valid_for_exact_conditions(user_provided_value) or \
            condition_value_type != user_provided_value_type:
      return None

    return condition_value == user_provided_value

  def exists_evaluator(self, leaf_condition):
    if not self.attributes:
      return False
    return leaf_condition.get(leaf_condition['name']) is not None

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

  EVALUATORS_BY_OPERATOR_TYPE = {
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
        return self.EVALUATORS_BY_OPERATOR_TYPE[conditions[0]](self, conditions[1:])
      else:
        return self.EVALUATORS_BY_OPERATOR_TYPE[ConditionalOperatorTypes.OR](self, conditions[1:])

    leaf_condition = conditions

    if self.condition_data[leaf_condition][2] != CUSTOM_ATTRIBUTE_CONDITION_TYPE:
      return null

    condition_match = self.condition_data[leaf_condition][3]

    if condition_match not in MATCH_TYPES:
      return null

    return self.EVALUATORS_BY_MATCH_TYPE[condition_match](self, leaf_condition)


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
    obj_dict.get('match', ConditionalMatchTypes.EXACT)
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
