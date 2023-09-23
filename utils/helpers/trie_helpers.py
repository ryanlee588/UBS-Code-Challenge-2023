from utils.classes.trie import Trie
from typing import Dict, List


def fill_class_tries(classes: List[Dict]) -> (Dict, Dict):
  """
  Function given a list of classes, returns tries to aid in hinting of fields and a dict 
  containing the field types of respective fields that are indexed using:         
  <parent_class>_<field>
  """
  # init dictionary to store tries
  class_tries = {}

  # init dicitonary to store field_types for fields in classes with key-value pairs with
  # key <parent_class>_<field> and value <field_type>
  field_types = {}

  # init root_class_trie to take into account class names for root class names completions
  class_tries["root_class_trie"] = Trie()
  for class_dict in classes:
    for class_name in class_dict:
      """
      For all class_names, init Trie
      
      If class_dict[class_name] is a dict, insert each key into the Trie and
      add the type (value) of each key into field_types dict

      Else if class_dict[class_name] is a list, insert each string into the Trie
      """
      class_tries["root_class_trie"].insert(class_name)
      if isinstance(class_dict[class_name], dict):
        class_tries[class_name] = Trie()
        for key in class_dict[class_name]:
          class_tries[class_name].insert(key)
          field_types_key = class_name + "_" + key
          field_types[field_types_key] = class_dict[class_name][key]
      else:
        class_tries[class_name] = Trie()
        for field in class_dict[class_name]:
          class_tries[class_name].insert(field)
  return (class_tries, field_types)
