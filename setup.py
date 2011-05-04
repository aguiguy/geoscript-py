import os
import shutil
from distutils.core import setup
from distutils.archive_util import make_tarball
from setuptools import find_packages

ver='1.1-20110504'
jars = ['jars/%s' % (f) for f in os.listdir('jars')]
setup(name='geoscript',
      version=ver,
      description='GeoScript Python',
      author='Justin Deoliveira',
      author_email='jdeolive@opengeo.org',
      url='http://geoscript.org',
      packages=find_packages(),
      data_files=[('jars', jars)],
      scripts=['bin/geoscript-classpath', 'bin/geoscript']
     )

shutil.move(make_tarball('geoscript-%s-src' % ver, 'geoscript'), 'dist')

