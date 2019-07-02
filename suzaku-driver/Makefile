.PHONY: clean-pyc clean-build clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "install - install the package to the active Python's site-packages"
	@echo "develop - build the package to the develop Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.log' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

test:
	python setup.py test

ubuntu:
	apt install -y build-essential
	apt install -y biosdevname
	apt install -y python-dev
	apt install -y libyaml-dev
	apt install -y ipmitool

centos:
	yum install -y gcc
	yum install -y make
	yum install -y automake
	yum install -y autoconf
	yum install -y libtool
	yum install -y python-devel
	yum install -y libyaml-devel
	yum install -y ipmitool

install: clean
	python setup.py install

develop: clean
	python setup.py develop

deploy: install
	cp -f suzaku-driver.service /usr/lib/systemd/system/
	sed -i 's/SUZAKU_DRIVER_ENV/${SUZAKU_DRIVER_ENV}/g' /usr/lib/systemd/system/suzaku-driver.service
	cat /usr/lib/systemd/system/suzaku-driver.service
	systemctl daemon-reload
	systemctl stop suzaku-driver
	sleep 3
	systemctl start suzaku-driver
