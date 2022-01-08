# Copyright 2017, 2018, 2019 Alexander L. Hayes

.PHONY : clean test style lint distribution

# Rules for testing, code style, and linting
test:
	python -c 'from srlearn.system_manager import reset; reset(soft=False)'
	pytest --cov=srlearn srlearn/
	coverage html
	@echo "Generating coverage report: htmlcov/index.html"

lint:
	pylint srlearn/

style:
	black srlearn/

# Distribution
distribution:
	pip install --upgrade setuptools wheel twine
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*
