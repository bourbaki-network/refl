#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from args.agda import agda
from args.repl import repl

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}


@click.group(chain=False, invoke_without_command=False, context_settings=CONTEXT_SETTINGS)
def cli():
  pass


cli.add_command(repl)
cli.add_command(agda)