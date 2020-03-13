from app import db
from datetime import datetime

class DataFile(db.Model):
  __tablename__ = 'datafiles'
  id = db.Column(db.Integer, primary_key = True)
  originalfilename = db.Column(db.String(128), nullable = False)
  actualfilename = db.Column(db.String(128), index = True, unique = True)
  actualfilepath = db.Column(db.String(128), nullable = False)
  mimetype = db.Column(db.String(32), index= True, nullable = False)
  filesize = db.Column(db.Integer, index = True)
  created = db.Column(db.DateTime, index = True, default = datetime.utcnow)
  fileprototype = db.Column(db.String(32), index = True, nullable = False)
  dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'), nullable = False)
  dataset = db.relationship('DataSet', back_populates = 'files')
  
  def __repr__(self):
    return '<id: {}, actualfilename: {}, mimetype: {}>, filesize: {}'.format(self.id, self.actualfilename, self.mimetype, self.filesize)