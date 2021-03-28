#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import *

import click

from install import VersionSwitcher
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
  pass


@pkg.command('switch')
@click.option(
  '-v',
  '--version',
  'version',
  type=str,
  multiple=False,
  help='Version of Agda to install',
)
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
def switch(version: str, globally: bool, user: bool):
  """Install new Agda version or switch between versions
  """
  location: str = os.getcwd()
  install_root: str = path.join(path.expanduser('~'), 'bin')
  if globally:
    location = path.join(path.expanduser('~'), '.refl')
    install_root = '/usr/bin'
  elif user:
    location = path.join(path.expanduser('~'), '.refl')
    if not path.exists(location):
      os.mkdir(location)

  v = VersionSwitcher(location, install_root)
  v.install()
  return None


@pkg.command('list')
def list_versions():
  """List available Agda versions
  """
  v = VersionSwitcher('.')
  versions = v.get_available_versions()
  print('Versions available:')
  [print(v.replace('.deb', '')) for v in versions]
  return None


# TODO: cleanup
# @pkg.command('uninstall')
# @click.option('-v',
#               '--version',
#               'version',
#               type=str,
#               multiple=False,
#               help='Version of Agda to uninstall')
# def uninstall(prelude: str, includes: list[str], library: str):
#   """Uninstall Agda locally
#   """
#   return None
