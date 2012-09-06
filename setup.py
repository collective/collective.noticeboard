from setuptools import setup, find_packages

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n\n' +
    'History\n'
    '=======\n'
    + '\n\n' +
    open('CHANGES.txt').read()
    + '\n\n' +
    'Contributors\n'
    '============\n'
    + '\n\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n')

setup(name='collective.noticeboard',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://github.com/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.js.backbone',
          'collective.js.underscore',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
