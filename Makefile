# Config
OSNAME			:= $(shell uname)

DEBIAN_FRONTEND		:= noninteractive
PYTHONUNBUFFERED	:= true

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
OSDEPS			:= sudo apt-get update && sudo apt-get -y install python-dev libtool build-essential libgpg11-dev pandoc
else
OPEN_COMMAND		:= open
OSDEPS			:= brew install gpgme pandoc
endif

ui.pending=@printf "\033[1;30m$(1)...\033[0m"
ui.ok=@printf "\033[1;32m OK\033[0m\r\n"
# all: tests html-docs

TZ				:= UTC
PYTHONPATH			:= $(shell pwd)
CRYPTONITE_LOGLEVEL		:= DEBUG
PATH				:= $(PATH):$(shell pwd)
CRYPTONITE_CONFIG_PATH		:= $(shell pwd)/tests/cryptonite.yml
executable			:= cryptonite
export TZ
export PATH
export PYTHONPATH
export CRYPTONITE_LOGLEVEL
export DEBIAN_FRONTEND
export PYTHONUNBUFFERED
export CRYPTONITE_CONFIG_PATH

all: setup tests

tests: lint unit functional integration

setup: remove clean os-dependencies deps

os-dependencies:
	-@$(OSDEPS)

lint:
	$(call ui.pending,"python\ lint\ check")
	@find cryptonite -name '*.py' | grep -v node | xargs flake8 --ignore=E501
	$(call ui.ok)
clean:
	$(call ui.pending,"cleaning\ garbage\ files")
	@rm -rf '*.egg-info' 'dist'
	@find . -name '*.pyc' -exec rm -f {} \;
	$(call ui.ok)

unit:
	nosetests --rednose --cover-erase tests/unit

functional:
	nosetests --with-spec --spec-color tests/functional/

integration:
	cryptonite-gpg wipe --no-backup --force
	cryptonite-gpg quickstart --force tests/cryptonite.yml
	cryptonite-gpg create "Maya Cyfer" maya@cyfer.io --no-secret
	cryptonite-gpg import "$$(curl -q https://keybase.io/d4v1ncy/key.asc)"
	test "$$(cryptonite-gpg keyid d4v1ncy@protonmail.ch)" == "XXXX"
	cryptonite-gpg encrypt john@doe.com 'A Private Hello'
	$(cryptonite-gpg decrypt -n "$$(cryptonite-gpg encrypt --no-secret john@doe.com 'A Private Hello')"
	cryptonite-gpg list
	cryptonite-gpg backup > backup.cryptonite
	cryptonite-gpg wipe --no-backup --force
	cryptonite-gpg recover --force backup.cryptonite
	cryptonite-gpg list
	cryptonite-gpg private john@doe.com
	cryptonite-gpg public XXXXXXXXX
	cryptonite-gpg wipe --no-backup --force


tests: unit functional integration

remove:
	-@pip uninstall -y cryptonite

pip:
	@pip install -U pip
	@CFLAGS='-std=c99' pip install -r development.txt

deps:

pythonpath:
	@CFLAGS='-std=c99' python setup.py develop

release:
	@./.release
	@python setup.py sdist register upload

list:
	@$(executable) list

.PHONY: html-docs docs

html-docs:
	cd docs && make html

docs: html-docs
	$(OPEN_COMMAND) docs/build/html/index.html
