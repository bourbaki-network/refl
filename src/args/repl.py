#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
def repl():
  """Start a REPL
  """
  pass


@repl.resultcallback()
def repl_process_commands(processors):
  if 'repl' in [p for p, _ in processors]:
    args = [a for p, a in processors if p == 'repl'][0]
    Repl(args).run()


@repl.command('agda')
@click.option('-p', '--prelude', 'prelude', type=str, multiple=False, help='File to load as prelude to the REPL')
@click.option('-i',
              '--include-path',
              'includes',
              type=list[str],
              multiple=True,
              help='Directories to look for including modules')
@click.option('-l', '--library', 'library', type=str, multiple=False, help='Use library in directory')
def agda(prelude: str, includes: list[str], library: str):
  """Start an Agda REPL.
  """
  return ('repl', {'prelude': prelude, 'includes': includes, 'library': library})
