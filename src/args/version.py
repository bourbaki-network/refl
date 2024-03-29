#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os import path

import click
from click_help_colors import HelpColorsGroup

from version import VersionSwitcher

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


@click.group(cls=HelpColorsGroup,
             help_headers_color='magenta',
             help_options_color='cyan',
             chain=True,
             invoke_without_command=True,
             context_settings=CONTEXT_SETTINGS)
def version():
  """Manage Agda installation and switch between versions
  """
  pass


@version.resultcallback()
def process_commands(processors):
  pass


@version.command('switch')
@click.option('-v', '--version', 'version', type=str, help='Version of Agda to install')
@click.option('-g', '--global', 'globally', type=bool, is_flag=True, help='Install Agda globally')
@click.option('-u', '--user', 'user', type=bool, is_flag=True, help='Install Agda for current user')
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


@version.command('uninstall')
@click.option('-v', '--version', 'version', type=str, help='Version of Agda to install')
@click.option('-g', '--global', 'globally', type=bool, is_flag=True, help='Install Agda globally')
@click.option('-u', '--user', 'user', type=bool, is_flag=True, help='Install Agda for current user')
def uninstall(version: str, globally: bool, user: bool):
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
  v.uninstall()
  return None


@version.command('list')
def list_versions():
  """List available Agda versions
  """
  v = VersionSwitcher('.')
  versions = v.get_available_versions()
  print('Versions available:')
  [print(v.replace('.deb', '')) for v in versions]
  return None
