.PHONY: flake8
flake8:
	@flake8 *.py tap_plugin tests


.PHONY: pylint
pylint:
	pylint -d missing-docstring *.py tap_plugin/
	pylint -d missing-docstring -d invalid-name -d too-few-public-methods tests/


.PHONY: test
test:
	nosetests --with-coverage --cover-erase --cover-package=tap_plugin --with-tap --tap-stream


.PHONY: ci
ci: flake8 pylint test
