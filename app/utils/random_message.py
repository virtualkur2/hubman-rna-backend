import random

# Next piece of code is inspired on Miguel Grinberg's Post:
# Using Celery with Flask:
# https://blog.miguelgrinberg.com/post/using-celery-with-flask

verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking', 'Entering']
adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast', 'dark']
noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit', 'arctifact']

def random_message():
  return '{0} {1} {2}'.format( random.choice(verb), random.choice(adjective), random.choice(noun))
