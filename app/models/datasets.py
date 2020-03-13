from app import db
from datetime import datetime

class DataSet(db.Model):
  __tablename__ = 'datasets'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), index = True)
  date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
  datatype = db.Column(db.String(32), index = True, nullable = False)
  algorithm_id = db.Column(db.Integer, db.ForeignKey('algorithms.id'), nullable = False)
  files = db.relationship('DataFile', back_populates='dataset')

  def __repr__(self):
    return '<id: {}, name: {}, date: {}>'.format(self.id, self.name, self.date)
