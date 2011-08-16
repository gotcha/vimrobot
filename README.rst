vimrobot
========

``vimrobot`` is a Python package to write functional tests of Vim with
``robotframework`` Python library.

Development
===========

``vimrobot`` source code and tracker are at https://github.com/gotcha/vimrobot.

How to develop ``vimrobot`` from github::

  git clone git@github.com:gotcha/vimrobot.git
  cd vimrobot/
  virtualenv-2.6 .
  bin/python bootstrap.py
  bin/buildout -Nvt 5
  bin/pybot vim.txt
