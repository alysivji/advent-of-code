python-shell:
	ipython

python-requirements:
	pip-compile --output-file requirements.txt requirements.in

python-requirements-dev:
	pip-compile --output-file requirements-dev.txt requirements-dev.in

python-install:
	pip install -r requirements-dev.txt -r requirements.txt

run-ts:
	npx ts-node $(file)

node-install:
	npm install
