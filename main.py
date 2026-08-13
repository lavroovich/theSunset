from flask import Flask, jsonify, Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import cli
import werkzeug.serving

from pyfiglet import figlet_format
import logging

from statics import StaticManager
from auth import TOTPctl

print("theSunset backend initializing...")

# -------======= Косметика =======--------

original_log = werkzeug.serving._log

def quiet_startup(log_type, message, *args):
    hidden = (
        "WARNING: This is a development server.",
        " * Running on",
        "Press CTRL+C to quit",
    )

    if any(text in message for text in hidden):
        return

    original_log(log_type, message, *args)

werkzeug.serving._log = quiet_startup

class HidePongFilter(logging.Filter):
    def filter(self, record):
        return "/api/pong" not in record.getMessage()


werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.addFilter(HidePongFilter())
# -------======= Flask и SQLAlchemy =======--------

app = Flask(__name__)

content_bp = Blueprint('content', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wines.db'
db = SQLAlchemy(app)

# --------======= Модель данных =======--------

class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    color = db.Column(db.String(50), nullable=False)
    sparkling = db.Column(db.Boolean, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    grape = db.Column(db.String(100), nullable=False)
    sugar = db.Column(db.String(50), nullable=False)

    price = db.Column(db.Integer, nullable=False)
    price_per_bokal = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'sparkling': self.sparkling,
            'country': self.country,
            'region': self.region,
            'grape': self.grape,
            'sugar': self.sugar,
            'price': self.price,
            'price_per_bokal': self.price_per_bokal
        }


# --------======= Маршруты фронтенда =======--------

@content_bp.route('/')
def home():
    return render_template('index.html')


@content_bp.route('/cellar')
def cellar():
    return render_template('cellar.html')

@content_bp.route('/wine/<int:wine_id>')
def wine_detail(wine_id):
    return render_template('wine_detail.html',wine_id=wine_id)

# --------======= Маршруты API =======--------

@api_bp.route('/pong')
def pong():
    return jsonify({"ok":True,"one_detail":"если я ответил, фактически я жив"})

@api_bp.route('/wines/<int:wID>')
def onewine(wID):
    wine = Wine.query.get_or_404(wID).to_dict()
    return jsonify(wine)
    
@api_bp.route('/wines', methods=['GET'])
def get_wines():
    wines = Wine.query.all()
    return jsonify([wine.to_dict() for wine in wines])

@api_bp.route('/assets/info/<int:wID>')
def assets_info(wID):
    x = sm.has_description(wID)
    y = sm.has_bottle(wID)
    return jsonify(
        {"assets":{
            "bottle":{
                "exist":y,
                "url": f"/static/bottles/{wID}.jpg" if y else None
            },
            "description":{
                "exist":x,
                "url": f"/static/descriptions/{wID}.webp" if x else None
            }
        }}
    )

app.register_blueprint(content_bp)
app.register_blueprint(api_bp)


with app.app_context():
    db.create_all()

def prepare_modules():
    sm = StaticManager()
    auth = TOTPctl()
    
    return sm , auth

sm, auth = prepare_modules()

if __name__ == '__main__':
    cli.show_server_banner = lambda *args, **kwargs: None
    
    print(figlet_format("theSunset", font="larry3d"))
    print("theSunset indev 0.2 | whole project 5.0")
    print("Written by CPWB Ltd. (Lavroovich) | Licensed under GPLv3")
    print()
    print("server: http://127.0.0.1:5000")
    print()
    app.run()

    