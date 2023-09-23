
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
    dp = [[0] * (v + 1) for _ in range(w + 1)]

    for i in range(n):
        weight, volume, value = f[i]
        for j in range(w, 0, -1):
            for k in range(v, 0, -1):
                if weight <= j and volume <= k:
                    dp[j][k] = max(dp[j][k], dp[j - weight]
                                   [k - volume] + value)

    return json.dumps(dp[w][v])
