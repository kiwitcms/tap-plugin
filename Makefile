.PHONY: ci
ci:
	nosetests --with-coverage --cover-erase --cover-package=tap_plugin
