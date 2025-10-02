./clean.sh
pip install twine
pip install setuptools
python3 setup.py sdist
python3 -m twine upload dist/*
