from app import db
from app.api import bp
from datetime import datetime
import app.tasks as tasks
from flask import jsonify, request, stream_with_context, Response
from werkzeug.datastructures import Headers
from app.utils import make_message, random_message
from inspect import getmembers
from celery import Task
import json, time

tasks_directory = { task_name: task_function
   for task_name, task_function in getmembers(tasks)
   if isinstance(task_function, Task) }


@bp.route('status/<task_name>/<task_id>')
def task_status(task_name, task_id):
  task_in_exec = tasks_directory.get(task_name)
  if not task_in_exec:
    return jsonify(make_message(not task_in_exec, message = 'No {} task availabale with id: {}'.format(task_name, task_id)))

  def task_status():
    while True:
      task     = task_in_exec.AsyncResult(task_id)
      response = make_message(False, state = task.state)

      if task.state == 'WORKING':
        message = random_message()
        response['status'] = message
        yield 'event: message\ndata: {}\n\n'.format(json.dumps(response))
        time.sleep(1.2)
      elif task.state != 'FAILURE':
        if 'status' in task.info:
          response['status'] = task.info.get('status')
        if 'results' in task.info:
          response['results'] = task.info.get('results')
        yield 'event: message\ndata: {0}\n\n'.format(json.dumps(response))
        time.sleep(1.2)
      else:
        response['error']  = True
        response['status'] = str(task.info)
        yield 'event: message\ndata: {0}\n\n'.format(json.dumps(response))
        time.sleep(1.2)

  headers = Headers()

  headers.add('Content-Type', 'text/event-stream')
  headers.add('Cache-Control', 'no-cache')
  headers.add('Connection', 'keep-alive')

  return Response(stream_with_context(task_status()), status = 200, headers = headers)
