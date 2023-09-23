
import logging
import json

from flask import request

from routes import app
import numpy as np

logger = logging.getLogger(__name__)


@app.route('/greedymonkey', methods=['POST'])
def greedy_monkey():
    data = request.get_json()
    w = data["w"]
    v = data["v"]
    f = data["f"]

    # Efficient Pruning
    f = [(weight, volume, value) for weight, volume, value in f if weight <= w and volume <= v]

    dp = np.zeros((w + 1, v + 1), dtype=int)

    for weight, volume, value in f:
        # We update the dp array for valid weight and volume indices,
        # avoiding the need for the second and third nested loops
        dp[weight:, volume:] = np.maximum(
            dp[weight:, volume:],
            dp[:w - weight + 1, :v - volume + 1] + value
        )

    result = int(dp[w, v])
    return json.dumps(result)

    # # Initialize a 2D array to store the maximum value for each (weight, volume) pair
    # dp = [[0] * (v + 1) for _ in range(w + 1)]

    # for item in f:
    #     weight, volume, value = item
    #     for j in range(w, weight - 1, -1):
    #         for k in range(v, volume - 1, -1):
    #             if j >= weight and k >= volume:
    #                 dp[j][k] = max(dp[j][k], dp[j - weight][k - volume] + value)
    # return json.dumps(dp[w][v])

