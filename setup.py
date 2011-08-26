try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name = "gitjobs",
      version = "0.0.1",
      description = "Python binding for github jobs API",
      author = "Vasyl Dizhak",
      author_email = 'vasyl.dizhak@djangostars.com',
      license = 'MIT',
      packages = ['gitjobs'],
      classifiers=['License :: OSI Approved :: MIT License',
                   'Development Status :: 2 - Pre-Alpha',
                   'Topic :: Software Development :: Libraries ' +
                   ':: Python Modules'
                   'Programming Language :: Python',
                   ])
