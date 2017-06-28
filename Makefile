VENV_NAME=test-venv

all: test

clean:
	rm -rf ${VENV_NAME}

venv:
	test -d ${VENV_NAME} || virtualenv ${VENV_NAME}
	. ${VENV_NAME}/bin/activate && pip install -r requirements.txt

pycodestyle: venv
	. ${VENV_NAME}/bin/activate && pycodestyle *.py

build: venv pycodestyle

test: build
	. ${VENV_NAME}/bin/activate && pip install -r requirements-tests.txt
	. ${VENV_NAME}/bin/activate && pytest *.py

