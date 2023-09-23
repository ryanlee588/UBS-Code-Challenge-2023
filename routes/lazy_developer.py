from utils.helpers.trie_helpers import fill_class_tries
from typing import Dict, List
import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/lazy-developer', methods=['POST'])
def lazy_developer():
    data = request.get_json()
    classes = data["classes"]
    statements = data["statements"]
    return_dict = getNextProbableWords(classes, statements)
    return (json.dumps(return_dict))


# Assumptions:
# If field is type: List<...>, it is polymorphic and therefore, return [""]
# Statements provided are valid
# There are no fields that have the same name as classes.


def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:
    # Get class_tries and field_types
    class_tries, field_types = fill_class_tries(classes)

    completions_dict = {}
    for statement in statements:
        parts = statement.split(".")
        """
        If parts == 1, means it is class name, finish class names
        If parts == 2, means that we are getting completions of a specific field in a class
        If parts > 2, means that the target_trie might not be a class, but a field
        which would require us to get its corresponding type from the field_types dict
        """
        if len(parts) == 1:
            completions = class_tries["root_class_trie"].get_completion(
                parts[0])
        elif len(parts) == 2:
            target_trie = parts[0]
            prefix = parts[1]
            if class_tries.get(target_trie) is not None:
                # target_trie in class_tries:
                completions = class_tries[target_trie].get_completion(prefix)
            else:
                completions = []
        elif len(parts) > 2:
            target_trie_parent = parts[-3]
            target_trie = parts[-2]
            prefix = parts[-1]
            """
            target_trie_parent cannot be used to concatenate as a key for field type if target_trie_parent is a field name. 
            Need to keep going back to get the originating class to trace the type
            To check if target_trie_parent is a field name, check if it exists within class tries. If it doesn't, it means it is a field name.
            """
            if target_trie_parent not in class_tries:
                current_index = -3
                root_parent = target_trie_parent
                # get root parent
                while (len(parts) + current_index > 0) and (root_parent
                                                            not in class_tries):
                    current_index -= 1
                    root_parent = parts[current_index]
                # Trace back, to third last part. Can take it that all preceeding are field names, given that they did not appear in class_tries.
                while (current_index != -3):
                    current_index += 1
                    type_key = root_parent + "_" + parts[current_index]
                    root_parent = field_types[type_key]
                target_trie_parent = root_parent
            # Create target_field_key
            target_field_key = target_trie_parent + "_" + target_trie
            """
            First check if target_field_key is a valid key in field_types, which would
            mean that our completion is from a field, thus we need to get its corresponding 
            type from the field_types dict. 
            
            If target_field_key is a valid key in field_types, but not in class tries, it means there are no completions as it is either a polymorphic type (i.e. Lists, Dict) or basic type (i.e. String, Double, Float).

            If target_field_key is not a valid key in field_types, check if the target_trie is 
            a valid key in class_tries. If target_trie is a valid key in class_tries, it means 
            that our completion is from a class in the list of classes, thus get completions 
            using the target_trie Trie. 

            As statement is assumed to be valid, it will not be possible that the statement will not fall into either of these checks.
            """
            if target_field_key in field_types:
                target_field_type = field_types[target_field_key]
                if target_field_type in class_tries:
                    completions = class_tries[target_field_type].get_completion(
                        prefix)
                else:
                    completions = [""]
            elif target_trie in class_tries:
                completions = class_tries[target_trie].get_completion(prefix)
        if completions == []:
            completions = [""]

        # sort completions in alphabetical order
        sorted_completions = sorted(completions)

        # if completions > 5, return first 5 completions
        if len(sorted_completions) >= 5:
            completions_dict[statement] = sorted_completions[:5]
        else:
            completions_dict[statement] = sorted_completions
    return completions_dict
