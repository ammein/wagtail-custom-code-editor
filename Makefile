.PHONY: help init start test clean-pyc publish static
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

start: ## Starts the development server.
	python3 ./tests/testapp/manage.py runserver

test: ## Test the project.
	python3 ./runtests.py

init: clean-pyc ## Install dependencies and initialise for development.
	pip3 install -e .[testing]
	python3 ./tests/testapp/manage.py migrate --noinput

update-test-fixture: ## Update test fixture from the db.
	python3 ./tests/testapp/manage.py dumpdata --indent=4 -e contenttypes -e auth.permission -e auth.group -e sessions -e wagtailcore.site -e wagtailcore.pagerevision -e wagtailcore.grouppagepermission -e wagtailimages.rendition -e wagtailcore.collection -e wagtailcore.groupcollectionpermission > tests/testapp/core/fixtures/test_data.json

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

publish: ## Publishes a new version to pypi.
	rm dist/* && python3 setup.py sdist && twine upload dist/* && echo 'Success! Go to https://pypi.python.org/pypi/wagtailgmaps and check that all is well.'

static:
	python3 ./tests/testapp/manage.py collectstatic --noinput