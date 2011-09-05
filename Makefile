#!/usr/bin/make
#
all: test

bin/python:
	virtualenv-2.6 --no-site-packages .

bin/buildout: bin/python bootstrap.py buildout.cfg
	./bin/python bootstrap.py

bin/pybot: bin/buildout
	./bin/buildout -vt 5

.PHONY: test
test: bin/pybot
	TERM=vt100; bin/pybot tests/vim.txt

.PHONY: cleanall
cleanall:
	rm -fr bin develop-eggs downloads eggs parts .installed.cfg
