import logging

from routes import app

logger = logging.getLogger(__name__)


@app.route('/tariffic-axelrod', methods=['POST'])
def evaluate():
    return "HELLO"