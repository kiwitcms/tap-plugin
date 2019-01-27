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
	nosetests -v --with-coverage --cover-erase --cover-package=tcms_tap_plugin


.PHONY: tap
tap:
	nosetests --with-tap --tap-stream 2> output.tap
	./tcms-tap-plugin output.tap


.PHONY: ci
ci: flake8 pylint test
