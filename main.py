from flask import Flask, jsonify, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from statics import StaticManager
from auth import TOTPctl

print("theSunset backend initializing...")

app = Flask(__name__)

content_bp = Blueprint('content', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wines.db'
db = SQLAlchemy(app)

sm = StaticManager()
auth = TOTPctl()

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


# --------======= Маршруты API =======--------

@api_bp.route('/wines', methods=['GET'])
def get_wines():
    wines = Wine.query.all()
    return jsonify([wine.to_dict() for wine in wines])


app.register_blueprint(content_bp)
app.register_blueprint(api_bp)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)