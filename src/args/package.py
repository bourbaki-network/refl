#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os

import click

# from typing import *

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


@click.group(chain=True, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
def pkg():
  """Manage Agda packages
  """
  pass


@pkg.command('install')
@click.option('-g', '--git', 'git', type=str, help='Git repository of package')
def install():
  """Install dependency
  """
  pass


@pkg.command('uninstall')
@click.option('-n', '--name', 'name', type=str, help='Package name')
def uninstall():
  """Uninstall dependency
  """
  pass


@pkg.command('search')
@click.option('-n', '--name', 'name', type=str, help='Package name')
def search():
  """Uninstall dependency
  """
  pass
