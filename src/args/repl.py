#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import *

import click

from commands import *
from interpret import *

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


# REPL commands
@click.group(chain=True, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
def repl():
  """Start a REPL
  """
  pass


@repl.resultcallback()
def repl_process_commands(processors):
  if 'repl' in [p for p, _ in processors]:
    Repl().run()


@repl.command('agda')
def agda():
  """Start an Agda REPL.
  """
  return ('repl', {})
