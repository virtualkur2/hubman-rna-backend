from app import db
from app.api import bp
from flask import jsonify
from app.utils import make_message
from app.models import Algorithm

algs = db.session.query(Algorithm).all()

@bp.route('algorithms', methods = ['GET'])
def get_algorithms():
  algorithms = []
  for algorithm in algs:
    algorithms.append({ 'name': algorithm.name, 'description': algorithm.description })
  message = make_message(not algorithms, algorithms = algorithms)
  return jsonify(message)
