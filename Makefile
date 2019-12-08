PACKAGE := 'fec-filing-iterator'
MODULE  := 'fec_filing_iterator'
VERSION := $(shell python -c 'import $(MODULE); print($(MODULE).__version__)')

.PHONY: docs

all: lint test

test:
	coverage run --source $(MODULE) -m py.test --disable-warnings
	coverage report -m

lint:
	flake8 $(MODULE)/
	flake8 tests/

docs:
	cd docs && make html

release: clean
	@echo "Releasing $(PACKAGE) $(VERSION)"
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -empty -delete
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf build/ dist/ $(MODULE).egg-info/
