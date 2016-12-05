from app import app
import logging 
from logging.handlers import RotatingFileHandler


if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    app.run(threaded=True)
