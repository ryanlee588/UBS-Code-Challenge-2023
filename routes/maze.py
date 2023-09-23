# import logging
# import json

# from flask import request

# from routes import app

# logger = logging.getLogger(__name__)

# current_maze = None

# def wall_follower(nearby)

# @app.route('/maze', methods=['POST'])
# def solver():
#     try:
#         global current_maze
#         data = request.json
#         mazeId = data["mazeId"]
#         nearby = data["nearby"]
#         mazeWidth = data["mazeWidth"]
#         step = data["step"]
#         isPreviousMovementValid = data["isPreviousMovementValid"]
#         message = data["message"]

#         current_maze = data

#         if not isPreviousMovementValid:
#             action = "respawn"
#         else:
#             action = wall_follower(nearby)
        

#     except Exception as e:
#         return json.dumps({"error": str(e)}), 400
        
        
