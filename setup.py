from distutils.core import setup

setup(
  name = 'chevrons',
  packages = ['chevrons'],
  py_modules = ['chevrons.pipeline_base','chevrons.pipeline_hof', 'chevrons.pipeline_extra'],
  version = '0.1.2.2',
  description = 'Rapidly build pipelines for out-of-core data processing using higher order functions.',
  author = 'Louis Cialdella',
  author_email = 'louiscialdella@gmail.com',
  url = 'https://github.com/lmc2179/chevrons',
  download_url = 'https://github.com/lmc2179/chevrons/tarball/0.1.1',
  keywords = ['parallel', 'functional', 'map', 'reduce', 'fold', 'pipeline', 'stream'],
  classifiers = [],
)