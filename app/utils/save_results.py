from app import db
from datetime import datetime
from app.models import DataResult, DataSet

def save_results(results):
  if not results['dataset_id']:
    return False
  dataset = db.session.query(DataSet).filter_by(id = results['dataset_id']).one()
  dataresult = DataResult(
    dataset_id = dataset.id,
    date       = datetime.utcnow(),
    accuracy   = results['accuracy'],
    precision  = results['precision'],
    recall     = results['recall'],
    f1score    = results['f1score'])
  db.session.add(dataresult)
  db.session.commit()
  return True

