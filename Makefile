.DELETE_ON_ERROR:

all:
	echo >&2 "Must specify target."

test:
	tox

testpdb:
	tox -e pdb

develop:
	tox -e develop

prod:
	tox -e venv

clean:
	rm -rf build/ dist/ *.egg-info/ .tox/ _static/ _templates/ _build/
	find . -name .coverage -delete
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -name '*.log' -delete

.PHONY: all test testpdb prod clean develop
