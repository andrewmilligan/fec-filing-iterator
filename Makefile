VERSION := $(shell python -c 'import fec_crawler; print(fec_crawler.__version__)')

all: lint test

test:
	coverage run --source fec_crawler -m py.test --disable-warnings
	coverage report -m

lint:
	flake8 fec_crawler/
	flake8 tests/

release:
	@echo "Releasing fec-crawler $(VERSION)"
	python setup.py sdist upload -r local

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -empty -delete
	rm -rf .pytest_cache
	rm -f .coverage
