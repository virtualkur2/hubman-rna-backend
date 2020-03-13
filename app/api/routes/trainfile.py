import os
import uuid
from app import db
from app.api import bp
from app import uploadFolder
from datetime import datetime
from app.tasks import train_task
from flask import jsonify, request, make_response, url_for
from app.utils import make_message
from app.utils import check_properties
from app.models import Algorithm, DataFile, DataSet, DataResult
from inspect import getmembers, isfunction


expectedContentType = "multipart/form-data"

@bp.route('train/file', methods = ['POST'])
def train_file():
  ok, msg = check_properties(request, form = None, files = None, content_type = expectedContentType)
  if not ok:
    return jsonify(make_message(True, message = msg))
  
  form  = request.form.to_dict()
  files = request.files.to_dict()

  originalTrainFileName = files.get('trainFile').filename
  originalTestFileName  = files.get('testFile').filename

  trainFileExt  = os.path.splitext(originalTrainFileName)[1]
  testFileExt   = os.path.splitext(originalTestFileName)[1]
  trainMimeType = files.get('trainFile').mimetype
  testMimeType  = files.get('testFile').mimetype
  trainFileName = uuid.uuid1().hex + trainFileExt
  testFileName  = uuid.uuid1().hex + testFileExt
  
  try:
    files.get('trainFile').save(os.path.join(uploadFolder, trainFileName))
    files.get('testFile').save(os.path.join(uploadFolder, testFileName))
  except IOError as ioe:
    saveFileErrorMessage = 'I/O error during write of files: {}'.format(repr(ioe))
    print(saveFileErrorMessage)
    return jsonify(make_message(True, message = saveFileErrorMessage))
  except Exception as e:
    exceptionErrorMessage = 'Exception during file processing: {}'.format(repr(e))
    print(exceptionErrorMessage)
    return jsonify(make_message(True, message = exceptionErrorMessage))

  trainStats = os.stat(os.path.join(uploadFolder, trainFileName))
  testStats  = os.stat(os.path.join(uploadFolder, testFileName))

  trainFileCreated = datetime.utcfromtimestamp(trainStats.st_ctime)
  testFileCreated  = datetime.utcfromtimestamp(testStats.st_ctime)

  trainFileSize = trainStats.st_size
  testFileSize  = testStats.st_size

  try:
    algorithm = db.session.query(Algorithm).filter_by(name = form['algorithmName']).one()
  except Exception as e:
    exceptionErrorMessage = 'Exception during algorithm search: {}. On searching for: {}'.format(repr(e), form['algorithmName'])
    print(exceptionErrorMessage)
    return jsonify(make_message(True, message = exceptionErrorMessage))
  
  trainFile = DataFile(
    originalfilename = originalTrainFileName,
    actualfilename   = trainFileName,
    actualfilepath   = uploadFolder,
    mimetype         = trainMimeType,
    filesize         = trainFileSize,
    created          = datetime.utcnow(),
    fileprototype    = "train")

  testFile = DataFile(
    originalfilename = originalTestFileName,
    actualfilename   = testFileName,
    actualfilepath   = uploadFolder,
    mimetype         = testMimeType,
    filesize         = testFileSize,
    created          = datetime.utcnow(),
    fileprototype = "test")

  dataset = DataSet(
    name         = form.get('dataName'),
    date         = datetime.utcnow(),
    datatype     = 'training',
    algorithm_id = algorithm.id)

  dataset.files = [trainFile, testFile]
  
  db.session.add(dataset)
  db.session.commit()

  task = train_task.apply_async(
    args = [
      os.path.join(uploadFolder, trainFileName),
      os.path.join(uploadFolder, testFileName),
      dataset.id, algorithm.script_name
    ]
  )
  message = make_message(False, taskstatusurl = url_for('api.task_status', task_name='train_task', task_id = task.id))

  return make_response(jsonify(message), 202)

