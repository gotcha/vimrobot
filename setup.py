from setuptools import setup, find_packages

version = '0.1dev'

long_description = (file('README.rst').read() +
    '\n\n' + file('HISTORY.txt').read())


setup(name='vimfunctional',
      version=version,
      description="Vim functional tests support",
      long_description=long_description,
      author="Godefroid Chapelle",
      author_email="gotcha@bubblenet.be",
      url="https://github.com/gotcha/vimfunctional",
      license="GPL",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'TermEmulator',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
