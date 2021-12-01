shell-dev:
	ipython

requirements:
	pip-compile --output-file requirements.txt requirements.in

install:
	pip install -r requirements_dev.txt

run-ts:
	npx ts-node $(file)
