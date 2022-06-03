.PHONY: test guesses

init:
	python3 -m pip install -r requirements.txt

test:
	pytest

guesses:
	python3 main.py -log=DEBUG 2>&1 | grep Guessing | sort | uniq > guesses 

verbose:
	python3 main.py -log=DEBUG 2>&1

typecheck:
	mypy --namespace-packages **/*.py

lint:
	pylint ./bot main.py

lint-fix:
	autopep8 --in-place -a -a -a -a -a **/*.py

run:
	python3 main.py

verbose:
	python3 main.py -log=debug

precommit : typecheck test lint-fix lint