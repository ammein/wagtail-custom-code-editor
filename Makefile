.PHONY: help init start test clean-pyc publish static
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

start: ## Starts the development server.
	python3 ./tests/testapp/manage.py runserver

test: ## Test the project.
	cd ./tests/testapp && python3 manage.py test

superuser: ## Create super user
	DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=mail@example.com DJANGO_SUPERUSER_PASSWORD=admin python3 ./tests/testapp/manage.py createsuperuser --noinput

init: clean-pyc ## Install dependencies and initialise for development.
	pip3 install -e .[testing]; \
	if python -c "import setuptools" &>/dev/null; then \
	  	echo "Skipped setuptools" \
	else \
	  	pip install setuptools; \
  	fi; \
	python3 ./tests/testapp/manage.py migrate --noinput

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

publish: ## Publishes a new version to pypi. See: https://docs.djangoproject.com/en/5.2/intro/reusable-apps/
	@if [[ -d "./dist/" ]]; then \
  		rm dist/*; \
  	fi; \
	python3 setup.py sdist; \
	if which twine &> /dev/null; then \
  		twine upload dist/*; \
  	else \
  	  	pip install twine; \
  	  	twine upload dist/*; \
  	fi; \
	echo 'Success! Go to https://pypi.python.org/pypi/wagtail-custom-code-editor and check that all is well.'

static: ## Push Static Files to test
	python3 ./tests/testapp/manage.py collectstatic --noinput

getfiles: ## Collect All Ace Files and insert them into `files.py`
	python3 ./getfiles.py