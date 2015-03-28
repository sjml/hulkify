from setuptools import setup, find_packages

# upload with: python setup.py sdist upload -r pypi

setup(name='hulkify',
    version='0.0.3',
    packages=['hulkify'],
    description='Turn normal English into HULK-SPEAK',
    url='http://github.com/sjml/hulkify',
    author='Shane Liesegang',
    author_email='shane@techie.net',
    license='MIT',
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python :: 2 :: Only',
      'Programming Language :: Python :: 2.7',
      'Topic :: Text Processing :: Filters',
    ],
    keywords=['hulk', 'english', 'text', 'filter'],
    install_requires=["Pattern>=2.6"],
)
