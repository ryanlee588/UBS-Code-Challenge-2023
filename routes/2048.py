import logging
import json

from routes import app

logger = logging.getLogger(__name__)

@app.route('/2048.html', methods=['GET'])
def twoOhFourEight():
    return "HELLO"