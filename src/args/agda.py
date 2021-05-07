#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import *
from typing import IO

import click

from commands import *
from commands import Range
from interpret import *

CONTEXT_SETTINGS = {
  'max_content_width': 200,
  # 'short_help_width':  400,
  'color': True
}

# Help statements
file_help = 'Path of file to load (absolute or relative).'
rewrite_help = 'Rewrite modes, can be one of `AsIs`, `Instantiated`, `HeadNormal`, `Simplified`, `Normalised`, defaults to `Simplified`'
expr_help = 'Expression, in case no position (--where) is given'
range_help = 'Position of file specified as `((start₁, end₁), (start₂, end₂))` or `(position₁, position₂)` or defaults to none. Note: for most commands, in case position is not specified, an expr needs to be specified'
compute_help = 'Computation mode, can be one of `DefaultCompute`, `IgnoreAbstract`, `UseShowInstance`, defaults to `DefaultCompute`'
interaction_help = 'Interaction id, defaults to 0'


# Agda passthrough commands
@click.group(chain=True, invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
def agda():
  """Interact with Agda
  """
  pass


@agda.resultcallback()
def cli_process_commands(processors):
  print("------------------------", processors)

  cmds = Commands(processors[0][1]['file'].name)

  # remove all file arguments
  [p[1].pop('file') if 'file' in p[1] else None for p in processors]

  commands = [p[0] for p in processors]
  args = [p[1] for p in processors]

  cs = [getattr(cmds, c)(**a) if hasattr(cmds, c) else Exception('Wrong command perhaps: ' + c) for c, a in list(zip(commands, args))]

  repl.run(cs)


@agda.command('compile')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-b',
              '--backend',
              'backend',
              type=str,
              help='Backend to use, \
    can be one of `GHC`, `GHCNoMain`, `LaTeX`, `QuickLaTeX`, if in doubt use `GHCNoMain`')
@click.option('-c', '--cmds', 'cmds', type=str, help='Commands, comma-separated')
def compile_cmd(file: IO[str], backend: str, cmds: str):
  """Compile agda code in a file.
  """
  cmds_ = cmds.strip().split(',') if cmds else None
  return ('compile', {'backend': backend, 'file': file, 'cmds': cmds_})


@agda.command('load')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-p', '--cmds', default='', type=str, multiple=False, help='Paths to include, comma-separated.')
def load_cmd(file: IO[str], cmds: str):
  """Load a file and type check it.
  """
  cmds_ = cmds.strip().split(',') if cmds else None
  return ('load', {'file': file, 'cmds': cmds_})


@agda.command('constraints')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
def constraints_cmd(file: IO[str]):
  """Check constraints.
  """
  return ('constraints', {'file': file})


@agda.command('metas')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
def metas_cmd():
  """Show all goals in a file.
  """
  return ('metas', {'file': file})


@agda.command('show_module_contents_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
def show_module_contents_toplevel_cmd(file: IO[str], rewrite: str = 'Simplified', expr: str = ''):
  """List all module contents.
  """
  return ('', {'file': file, 'rewrite': rewrite, 'expr': expr})


@agda.command('search_about_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
def search_about_toplevel_cmd(file: IO[str], rewrite: str = 'Simplified', expr: str = ''):
  """Search about a keyword.
  """
  return ('', {'file': file, 'rewrite': rewrite, 'expr': expr})


@agda.command('solveAll')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
def solveAll_cmd(file: IO[str], rewrite: str = 'Simplified', expr: str = ''):
  """Solve all constraints in a file.
  """
  return ('', {'file': file, 'rewrite': rewrite, 'expr': expr})


@agda.command('solveOne')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def solveOne_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Solve one constraint in a given expression.
  """
  return ('solveOne', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('autoAll')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
def autoAll_cmd(file: IO[str]):
  """Automatic proof search, find proofs, entire file.
  """
  return ('autoAll', {'file': file})


@agda.command('autoOne')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def autoOne_cmd(file: IO[str], interactionId: int = 0, where: Range = None, expr: str = ''):
  """Automatic proof search, find proofs, specific hole.
  """
  return ('autoOne', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('auto')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def auto_cmd(file: IO[str], interactionId: int = 0, where: Range = None, expr: str = ''):
  """Automatic proof search, find proofs, specific hole.
  """
  return ('autoOne', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('infer_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
def infer_toplevel_cmd(file: IO[str], rewrite: str = 'Simplified', expr: str = ''):
  """Infer all types in file.
  """
  return ('infer_toplevel', {'file': file, 'rewrite': rewrite, 'expr': expr})


@agda.command('compute_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-c', '--computeMode', 'computeMode', type=str, default='DefaultCompute', help=compute_help)
def compute_toplevel_cmd(file: IO[str], computeMode: str = 'DefaultCompute', expr: str = ''):
  """Compute the normal form, whole file.
  """
  return ('compute_toplevel', {'file': file, 'expr': expr, 'computeMode': computeMode})


@agda.command('load_highlighting_info')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
def load_highlighting_info_cmd(file: IO[str]):
  """Load highlighting info for agda file.
  """
  return ('load_highlighting_info', {'file': file})


@agda.command('tokenHighlighting')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--remove', 'remove', type=str, help='`Remove` or `Keep`, defaults to Keep')
def tokenHighlighting_cmd(file: IO[str], remove: str):
  """Highlight token.
  """
  return ('tokenHighlighting', {'file': file, 'remove': remove})


@agda.command('highlight')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=Range(), help=range_help)
def highlight_cmd(file: IO[str], interactionId: int = 0, where: Range = None):
  """Highlight file.
  """
  return ('highlight', {'file': file, 'interactionId': interactionId, 'where': where})


@agda.command('give')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=Range(), help=range_help)
def give_cmd(file: IO[str], force: str, interactionId: int = 0, where: Range = None, expr: str = ''):
  """Fill a goal.
  """
  return ('give', {'file': file, 'interactionId': interactionId, 'where': where})


@agda.command('refine')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def refine_cmd(file: IO[str], interactionId: int = 0, where: Range = None, expr: str = ''):
  """Refine: makes new holes for missing arguments.
  """
  return ('refine', {
    'file': file,
  })


@agda.command('intro')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=Range(), help=range_help)
@click.option('-w', '--whether', 'whether', type=bool, help='Whether to (?), defaults to false')
def intro_cmd(file: IO[str], whether: bool, interactionId: int = 0, where: Range = None, expr: str = ''):
  """Give information about holes.
  """
  return ('intro', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where, 'whether': whether})


@agda.command('refine_or_intro')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=Range(), help=range_help)
@click.option('-w', '--whether', 'whether', type=bool, help='Whether to (?), defaults to false')
def refine_or_intro_cmd(file: IO[str], whether: bool, interactionId: int = 0, where: Range = None, expr: str = ''):
  """Refine. Partial give: makes new holes for missing arguments.
  """
  return ('intro', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where, 'whether': whether})


@agda.command('context')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def context_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Context of the goal.
  """
  return ('context', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('helper_function')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def helper_function_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Create type of application of new helper function that would solve the goal.
  """
  return ('helper_function', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('infer')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def infer_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Infer type.
  """
  return ('infer', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('goal_type')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def goal_type_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Goal type.
  """
  return ('goal_type', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('elaborate_give')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def elaborate_give_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Grabs the current goal's type and checks the expression in the hole against it. Returns the elaborated term.
  """
  return ('elaborate_give', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('goal_type_context')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def goal_type_context_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Displays the current goal and context.
  """
  return ('goal_type_context', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('goal_type_context_infer')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def goal_type_context_infer_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Displays the current goal and context and infers the type of an expression.
  """
  return ('goal_type_context_infer', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('goal_type_context_check')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def goal_type_context_check_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Grabs the current goal's type and checks the expression in the hole against it.
  """
  return ('goal_type_context_check', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('show_module_contents')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help=rewrite_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def show_module_contents_cmd(file: IO[str], rewrite: str = 'Simplified', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Shows all the top-level names in the given module, along with their types. Uses the scope of the given goal.
  """
  return ('show_module_contents', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})


@agda.command('make_case')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def make_case_cmd(file: IO[str], interactionId: int = 0, where: Range = None, expr: str = ''):
  """Pattern match on variables (case split).
  """
  return ('make_case', {'file': file, 'interactionId': interactionId, 'where': where, 'expr': expr})


@agda.command('why_in_scope')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
def why_in_scope_cmd(file: IO[str], interactionId: int = 0, where: Range = None, expr: str = ''):
  """Explain why a keyword is in scope.
  """
  return ('why_in_scope', {'file': file, 'interactionId': interactionId, 'where': where, 'expr': expr})


@agda.command('compute')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help=interaction_help)
@click.option('-w', '--where', 'where', type=str, default=None, help=range_help)
@click.option('-c', '--computeMode', 'computeMode', type=str, default='DefaultCompute', help=compute_help)
def compute_cmd(file: IO[str], computeMode: str = 'DefaultCompute', interactionId: int = 0, where: Range = None, expr: str = ''):
  """Compute the normal form of either selected code or given expression.
  """
  return ('compute', {'file': file, 'interactionId': interactionId, 'where': where, 'expr': expr, 'computeMode': computeMode})


@agda.command('why_in_scope_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help=file_help)
@click.option('-e', '--expr', 'expr', type=str, default='', help=expr_help)
def why_in_scope_toplevel_cmd(file: IO[str], expr: str = ''):
  """Explain why a keyword is in scope, entire file.
  """
  return ('why_in_scope_toplevel', {'file': file, 'expr': expr})


@agda.command('show_version')
def show_version_cmd():
  """Show version.
  """
  return ('show_version', {})


@agda.command('abort')
def abort_cmd():
  """Abort currently ongoing action.
  """
  return ('abort', {})
