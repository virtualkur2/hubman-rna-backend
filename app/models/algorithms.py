from app import db

class Algorithm(db.Model):
  __tablename__ = "algorithms"
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(5), index = True)
  description = db.Column(db.String(64))
  script_name = db.Column(db.String(32))
  
  def __repr__(self):
    return '<id: {}, name: {}, description: {}, script_name: {}>'.format(self.id, self.name, self.description, self.script_name)