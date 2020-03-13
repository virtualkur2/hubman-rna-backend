def make_message(isError, **props):
  message = {}
  message['error'] = isError
  for prop, expected in props.items():
    message[prop] = expected
  return message