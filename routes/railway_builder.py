import logging
import json

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def count_railway_combinations(length_of_railway, num_types_of_track_piece, track_piece_lengths):
    dp = [0] * (length_of_railway + 1)
    dp[0] = 1

    for length in track_piece_lengths:
        for i in range(length, length_of_railway + 1):
            dp[i] += dp[i - length]

    return dp[length_of_railway]

@app.route('/railway-builder', methods=['POST'])
def railway_builder():
    try:
        input_data = request.json
        output = []

        for data in input_data:
            values = data.split(', ')
            length_of_railway = int(values[0])
            num_types_of_track_piece = int(values[1])
            track_piece_lengths = [int(x) for x in values[2:]]

            combinations = count_railway_combinations(length_of_railway, num_types_of_track_piece, track_piece_lengths)
            output.append(combinations)

        return json.dumps(output)

    except Exception as e:
        return json.dumps({"error": str(e)}), 400