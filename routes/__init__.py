from flask import Flask

app = Flask(__name__)

import routes.square
import routes.lazy_developer
import routes.greedy_monkey
import routes.digital_colony