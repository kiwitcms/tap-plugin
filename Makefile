.PHONY: flake8
flake8:
	@flake8 *.py tcms_tap_plugin tests


.PHONY: pylint
pylint:
	pylint -d missing-docstring *.py tcms_tap_plugin/
	pylint -d missing-docstring -d invalid-name -d too-few-public-methods \
	    -d protected-access -d duplicate-code tests/


.PHONY: test
test:
	nosetests --with-coverage --cover-erase --cover-package=tcms_tap_plugin --with-tap --tap-stream


.PHONY: ci
ci: flake8 pylint test
