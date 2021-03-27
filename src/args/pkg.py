#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import *

import click

from interpret import *

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


# REPL commands
@click.group(chain=True, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
def pkg():
  """Manage Agda installation and packages
  """
  pass


@pkg.resultcallback()
def process_commands(processors):
  # if 'repl' in [p for p, _ in processors]:
  #   args = [a for p, a in processors if p == 'repl'][0]
  #   Repl(args).run()
  pass


@pkg.command('install')
@click.option('-v',
              '--version',
              'version',
              type=str,
              multiple=False,
              help='Version of Agda to install')
@click.option('-g',
              '--global',
              'globally',
              type=bool,
              is_flag=True,
              multiple=False,
              help='Install Agda globally')
@click.option('-u',
              '--user',
              'user',
              type=bool,
              is_flag=True,
              multiple=False,
              help='Install Agda for current user')
def install(prelude: str, version: str, globally: bool, user: bool):
  """Install Agda
  """
  location: str = os.getcwd()
  if globally:
    location = '/usr/share/'
  elif user:
    location = path.expanduser('~')
  print(location, "++++++++++++++++++++++++++++++++++")

  return ('repl', {'prelude': prelude, 'includes': includes, 'library': library})


@pkg.command('list')
def list_versions(prelude: str, includes: list[str], library: str):
  """List available Agda versions
  """
  return ('repl', {'prelude': prelude, 'includes': includes, 'library': library})


@pkg.command('switch')
def switch(prelude: str, includes: list[str], library: str):
  """Switch between installed Agda versions
  """
  return ('repl', {'prelude': prelude, 'includes': includes, 'library': library})


@pkg.command('uninstall')
@click.option('-v',
              '--version',
              'version',
              type=str,
              multiple=False,
              help='Version of Agda to uninstall')
def uninstall(prelude: str, includes: list[str], library: str):
  """Uninstall Agda locally
  """
  return ('repl', {'prelude': prelude, 'includes': includes, 'library': library})
