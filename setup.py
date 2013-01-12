from setuptools import setup, find_packages

version = '0.2'

long_description = (
    open('README.txt').read()
    + '\n\n' +
    'History\n'
    '=======\n'
    + '\n\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective.noticeboard',
      version=version,
      description="A fancy noticeboard for Plone",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
        ],
      keywords='Plone javascript',
      author='Philip Bauer',
      author_email='bauer@starzel.de',
      url='http://github.com/starzel/collective.noticeboard',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'collective.js.backbone',
          'collective.js.underscore',
          'collective.js.jqueryui',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
  	  [z3c.autoinclude.plugin]
  	  target = plone
      """,
      )
