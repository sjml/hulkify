#! /bin/sh

rm -rf ./dist

npm publish

python setup.py sdist
twine upload dist/*

