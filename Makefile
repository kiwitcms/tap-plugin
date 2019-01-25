.PHONY: flake8
flake8:
	@flake8 *.py tap_plugin tests


.PHONY: pylint
pylint:
	pylint -d missing-docstring *.py tap_plugin/ tests/


.PHONY: test
test:
	nosetests --with-coverage --cover-erase --cover-package=tap_plugin


.PHONY: ci
ci: flake8 pylint test
