BUILD_DIR=build
VENV_NAME=test-venv

all: clean test

clean:
	rm -fr ${BUILD_DIR}

clean_venv:
	rm -rf ${VENV_NAME}

create_build_dir:
	test -d ${BUILD_DIR} || mkdir ${BUILD_DIR}

venv:
	test -d ${VENV_NAME} || virtualenv ${VENV_NAME}
	pip install -r requirements.txt
	touch ${VENV_NAME}/bin/activate
	echo "virtualenv prepared, please run 'source ${VENV_NAME}/bin/activate' if you wish to use it in your current shell"

pycodestyle: venv
	. ${VENV_NAME}/bin/activate && pycodestyle *.py

build: create_build_dir venv pycodestyle

test: build
	. ${VENV_NAME}/bin/activate && pip install -r requirements-tests.txt
	. ${VENV_NAME}/bin/activate && pytest *.py

