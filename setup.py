from setuptools import setup
import json
import os

setup(name='hulkify',
    version='0.0.7',
    description='Turn normal English into HULK-SPEAK',
    url='https://github.com/sjml/hulkify',
    author='Shane Liesegang',
    author_email='shane@techie.net',
    license='MIT',
    keywords='hulk english text filter',
    packages=['hulkify'],
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python :: 2 :: Only',
      'Programming Language :: Python :: 2.7',
      'Topic :: Text Processing :: Filters',
    ],
    install_requires=["Pattern>=2.6"],
)
