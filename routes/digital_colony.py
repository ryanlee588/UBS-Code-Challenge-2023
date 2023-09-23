import logging
import json

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    data = request.get_json()
    return_list = []
    seen = {}
    for req in data:
        generations = int(req["generations"])
        colony_str = req["colony"]
        for i in range(generations):
            seen, colony_str = insert_children(colony_str, seen)
        weight = 0
        weight = str(sum(map(int, colony_str)))
        # for char in colony_str:
        #     weight += int(char)
        return_list.append(weight)
    return json.dumps(return_list)

def insert_children(number_str: str, seen: dict) -> str:
    """
    This function takes a number string and inserts a calculated 'child' 
    between every two digits in the original string.
    """
    
    # Calculate the weight of the number_str
    weight = sum(map(int, number_str))
    # weight = sum(int(num) for num in number_str)
    
    # Initialize children list to hold the calculated 'children'
    children = []
    
    number_pair = zip(number_str, number_str[1:]) 
    if number_pair in seen:
        children.append(seen[number_pair])
    else:
        # Use zip to create pairs of adjacent characters from number_str for processing
        for first, second in zip(number_str, number_str[1:]):
            
            first, second = int(first), int(second)
            
            # Calculate the signature based on the difference between adjacent digits
            signature = first - second if first >= second else 10 - (second - first)
            
            # Calculate raw_child and append the last digit to the children list
            children.append(str(weight + signature)[-1])
    
    # Create return string by interleaving the original string and the children string.
    # Use str.join() for efficient string concatenation.
    return_string = ''.join([f"{a}{b}" for a, b in zip(number_str, children)] + [number_str[-1]])
    
    return seen, return_string





# def insert_children(number_str: str):
#     weight = 0
#     children = []
#     for num in number_str:
#         value = int(num)
#         weight += value
#     for i, num in enumerate(number_str):
#         if i < (len(number_str) - 1):
#             first = int(num)
#             second = int(number_str[i + 1])
#             if first >= second:
#                 signature = first - second
#             else:
#                 diff = second - first
#                 signature = 10 - diff
#             # get child
#             raw_child = str(weight + signature)
#             children.append(raw_child[-1])
#         else: 
#             break
#     return_string = number_str
#     for i, child in enumerate(children):
#         insert_index = (2 * i) + 1
#         return_string = return_string[:insert_index] + child + return_string[insert_index:]
#     return return_string