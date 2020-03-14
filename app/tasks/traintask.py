from app import celery
from datetime import datetime
from app.models import TrainData
from app.utils.save_results import save_results
from inspect import getmembers, isfunction

import app.scripts as scripts

script_directory = { script_name: script_function
   for script_name, script_function in getmembers(scripts)
   if isfunction(script_function) }

@celery.task(bind = True, name='train_task')
def train_task(self, trainFile, testFile, dataset_id, script_name):
  script = script_directory.get(script_name)
  if not script:
    self.update_state(state='FAILURE')
    return { 'status': 'Task failed. Unknown script {}.'.format(script_name) }
  if not dataset_id:
    self.update_state(state='FAILURE')
    return { 'status': 'Task failed. No dataset_id provided.' }

  self.update_state(state='WORKING')
  traindata = TrainData(trainFile, testFile, dataset_id)

  results = script(traindata)
  data = {'status': 'Task completed.'}
  if save_results(results):
    data['results'] = results
  return data

