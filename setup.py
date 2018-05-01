from setuptools import setup
import sys

# build dependency list
reqs = ['altair>=2.0.0rc2', 'vega3', 'ipywidgets', 'IPython', 'ipywidgets']

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='autovega.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

with open('README.md') as f:
    readme = f.read()

setup(name='autovega',
      version=verstr,
      description='An IPython/Jupyter notebook widget'
      ' for quick visualization of Pandas dataframes',
      long_description=readme,
      url='https://github.com/baldwint/autovega',
      author='Tom Baldwin',
      author_email='baldwint@baldwint.com',
      license='BSD 3-clause',
      classifiers=(
          'Development Status :: 3 - Alpha',
          'Framework :: Jupyter',
          'Framework :: IPython',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Visualization',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ),
      install_requires=reqs,
      py_modules=['autovega'],
      )
