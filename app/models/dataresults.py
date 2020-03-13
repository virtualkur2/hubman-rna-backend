from app import db
from datetime import datetime

class DataResult(db.Model):
  __tablename__ = 'dataresults'
  id = db.Column(db.Integer, primary_key = True)
  date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
  accuracy = db.Column(db.Float)
  precision = db.Column(db.Float)
  recall = db.Column(db.Float)
  f1score = db.Column(db.Float)
  dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable = False)

  def __repr__(self):
    return '<id: {}, \
            date: {}, \
            accuracy: {}, \
            precision: {}, \
            recall: {}, \
            f1score: {}, \
            dataset_id: {}>' \
            .format(self.id, \
            self.date, \
            '%.3f' %self.accuracy, \
            '%.3f' %self.precision, \
            '%.3f' %self.recall, \
            '%.3f' %self.f1score, \
            self.dataset_id)
