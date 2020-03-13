def check_properties(object, **props):
  for prop, expected in props.items():
    if not hasattr(object, prop):
      return False, "No {} received".format(prop)
    value = getattr(object, prop)
    if not value: # The value is empty
      return False, "The {} is empty".format(prop)
    if expected and expected not in value:
      return False, "The {} does not contain {}".format(prop, expected)
  return True, "Ok"
