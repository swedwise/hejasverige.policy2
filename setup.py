from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='hejasverige.policy2',
      version=version,
      description="Heja Sverige Site Policy",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
      ],
      keywords='',
      author='Daniel Grindelid',
      author_email='daniel.grindelid@swedwise.se',
      url='http://www.swedwise.se/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hejasverige'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'webcouturier.dropdownmenu',
          'hejasverige.megabank',
          'hejasverige.theme2',
          'hejasverige.content',
          'hejasverige.kollkoll',
          'hejasverige.api',
          'hejasverige.invitation',
          'hejasverige.wizard',
          'collective.cover',
          'collective.onlogin',
          'collective.monkeypatcher',
          #'hejasverige.wizard2',
          #'Products.Doormat',
          # -*- Extra requirements: -*-
      ],
      extras_require={
        'test': ['plone.app.testing',]
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
