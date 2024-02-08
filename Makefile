.PHONY: install run clean

install:
	pipenv install setuptools
	pipenv run python setup.py install
	pipenv install

run: 
	pipenv run weathertop

clean:
	pipenv --rm
	rm -rf weathertop.egg-info
	rm -rf __pycache_
	rm -rf venv
