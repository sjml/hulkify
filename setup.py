from setuptools import setup
import json

package_info = json.load(open("./package.json", "r"))

setup(name='hulkify',
    version=package_info['version'],
    description=package_info['description'],
    url=package_info['homepage'],
    author=package_info['author']['name'],
    author_email=package_info['author']['email'],
    license=package_info['license'],
    keywords=package_info['keywords'],
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
