import chevrons
from setuptools import setup, find_packages

setup(
  name = 'chevrons',
  packages = find_packages(), 
  version = '0.1.3',
  description = 'Rapidly build pipelines for out-of-core data processing using higher order functions.',
  author = 'Louis Cialdella',
  author_email = 'louiscialdella@gmail.com',
  classifiers = ['Programming Language :: Python :: 3 :: Only'],
  url = 'https://github.com/lmc2179/chevrons',
  keywords = ['parallel', 'functional', 'map', 'reduce', 'fold', 'pipeline', 'stream']
)
