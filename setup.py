from distutils.core import setup

setup(name='jtop_to_prometheus_exporter',
      version='1.0',
      description='Collect prometheus metrics on jetson .',
      author='Orlov',
      packages=['jtop_to_prometheus_exporter'],
      install_requires=open('requirements.txt', 'r').read().splitlines(),
     )