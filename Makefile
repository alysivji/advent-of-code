shell-dev:
	ipython

requirements:
	pip-compile --output-file requirements.txt requirements.in

install:
	pip install -r requirements_dev.txt

run-ts:
	npx ts-node $(file)

current:
	make run-ts file="2021/day01_puzzle.ts"
