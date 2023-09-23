
import logging
import json

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/greedymonkey', methods=['POST'])
def greedy_monkey():
    data = request.get_json()
    w = data["w"]
    v = data["v"]
    f = data["f"]
    n = len(f)
    dp = [[[0] * (v + 1) for _ in range(w + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, volume, value = f[i - 1]
        for j in range(w + 1):
            for k in range(v + 1):
                if weight <= j and volume <= k:
                    dp[i][j][k] = max(dp[i - 1][j][k], dp[i - 1][j - weight][k - volume] + value)
                else:
                    dp[i][j][k] = dp[i - 1][j][k]

    return json.dumps(dp[n][w][v])

