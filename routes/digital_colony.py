import logging
import json

from flask import request

from routes import app

logger = logging.getLogger(__name__)

@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    data = request.get_json()
    return_list = []
    for req in data:
        generations = int(req["generations"])
        colony_str = req["colony"]
        for i in range(generations):
            colony_str = insert_children(colony_str)
        weight = 0
        for char in colony_str:
            weight += int(char)
        return_list.append(weight)
    return json.dumps(return_list)

def insert_children(number_str: str):
    weight = 0
    children = []
    for num in number_str:
        value = int(num)
        weight += value
    for i, num in enumerate(number_str):
        if i < (len(number_str) - 1):
            first = int(num)
            second = int(number_str[i + 1])
            if first >= second:
                signature = first - second
            else:
                diff = second - first
                signature = 10 - diff
            # get child
            raw_child = str(weight + signature)
            children.append(raw_child[-1])
        else: 
            break
    return_string = number_str
    for i, child in enumerate(children):
        insert_index = (2 * i) + 1
        return_string = return_string[:insert_index] + child + return_string[insert_index:]
    return return_string