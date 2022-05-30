from flask import Flask
from api.controllers import api_bp
import conf.settings as settings
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {
            'default': {
                'format': '[%(asctime)s] - %(levelname)s - %(message)s',
            }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'log_file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'logs/LastfmLovedTracksToSpotifyPlaylist.log',
            'level': 'DEBUG'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi', 'log_file_handler']
    }
})

app = Flask(__name__)
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run("127.0.0.1", debug=settings.APP_DEBUG)
