#!/usr/bin/env python3

from typing import *
from typing import IO
from os import path
from functools import update_wrapper

import click

from .commands import *


@click.group(chain=True, invoke_without_command=True)
def cli():
  pass

@cli.resultcallback()
def process_commands(processors):
  """This result callback is invoked with an iterable of all the chained
  subcommands.  As in this example each subcommand returns a function
  we can chain them together to feed one into the other, similar to how
  a pipe on unix works.
  """
  # Start with an empty iterable.
  stream = ()

  # Pipe it through all stream processors.
  for processor in processors:
      stream = processor(stream)

  # Evaluate the stream and throw away the items.
  for _ in stream:
    pass

def processor(f):
  """Helper decorator to rewrite a function so that it returns another
  function from it.
  """
  def new_func(*args, **kwargs):
      def processor(stream):
          return f(stream, *args, **kwargs)
      return processor
  return update_wrapper(new_func, f)


def generator(f):
  """Similar to the :func:`processor` but passes through old values
  unchanged and does not pass through the values as parameter.
  """
  @processor
  def new_func(stream, *args, **kwargs):
      for item in stream:
          yield item
      for item in f(*args, **kwargs):
          yield item
  return update_wrapper(new_func, f)


@cli.command('done')
@processor
def done_cmd(ctx, filename):
  """Saves all processed images to a series of files."""
  print(ctx)
  # cmd = Command()
  # getattr(cmd, )


@cli.command('compile')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-b', '--backend', 'backend', type=str, help='Backend to use, can be one of GHC, GHCNoMain, LaTeX, QuickLaTeX, if in doubt use GHCNoMain')
@click.option('-c', '--cmds', 'cmds', type=str, help='Commands, comma-separated')
def compile_cmd(file:IO[str], backend:str, cmds:str):
  """Compile agda code in a file.
  """
  cmds = cmds.strip().split(',')
  return ('compile', {'backend': backend, 'file': file, 'cmds': cmds})

@cli.command('load')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-p', '--paths', default=None, type=click.Path(), multiple=True, help='Paths to include, comma-separated.')
@generator
def load_cmd(file:IO[str], cmds:str):
  """Load a file and type check it.
  """
  cmds = cmds.strip().split(',')
  return ('load', {'file': file, 'cmds': cmds})

@cli.command('constraints')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
def constraints_cmd(file:IO[str]):
  """Check constraints.
  """
  return ('constraints', {'file': file})

@cli.command('metas')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
def metas_cmd():
  """Show all goals in a file.
  """
  return ('metas', {'file': file})

@cli.command('show_module_contents_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
def show_module_contents_toplevel_cmd(file:IO[str], rewrite:str='Simplified', expr:str=''):
  """List all module contents.
  """
  return ('', {'file': file, 'rewrite': rewrite, 'expr': expr})

@cli.command('search_about_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
def search_about_toplevel_cmd(file:IO[str], rewrite:str='Simplified', expr:str=''):
  """Search about a keyword.
  """
  return ('', {'file': file, 'rewrite': rewrite, 'expr': expr})

@cli.command('solveAll')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
def solveAll_cmd(file:IO[str], rewrite:str='Simplified'):
  """Solve all constraints in a file.
  """
  return ('', {'file': file, 'rewrite': rewrite, 'expr': expr})

@cli.command('solveOne')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def solveOne_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Solve one constraint in a given expression.
  """
  return ('solveOne', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('autoAll')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
def autoAll_cmd(file:IO[str]):
  """Automatic proof search, find proofs, entire file.
  """
  return ('autoAll', {'file': file})

@cli.command('autoOne')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def autoOne_cmd(file:IO[str], interactionId:int=0, where:Range=None, expr:str=''):
  """Automatic proof search, find proofs, specific hole.
  """
  return ('autoOne', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('auto')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def auto_cmd(file:IO[str], interactionId:int=0, where:Range=None, expr:str=''):
  """Automatic proof search, find proofs, specific hole.
  """
  return ('autoOne', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('infer_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
def infer_toplevel_cmd(file:IO[str], rewrite:str='Simplified', expr:str=''):
  """Infer all types in file.
  """
  return ('infer_toplevel', {'file': file, 'rewrite': rewrite, 'expr': expr})

@cli.command('compute_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-c', '--computeMode', 'computeMode', type=str, default='DefaultCompute', help='Computation mode, can be one of DefaultCompute, IgnoreAbstract, UseShowInstance, defaults to DefaultCompute')
def compute_toplevel_cmd(computeMode:str='DefaultCompute', expr:str=''):
  """Compute the normal form, whole file.
  """
  return ('compute_toplevel', {'file': file, 'expr': expr, 'computeMode': computeMode})

@cli.command('load_highlighting_info')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
def load_highlighting_info_cmd(file:IO[str]):
  """Load highlighting info for agda file.
  """
  return ('load_highlighting_info', {'file': file})

@cli.command('tokenHighlighting')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--remove', 'remove', type=str, help='`Remove` or `Keep`, defaults to Keep')
def tokenHighlighting_cmd(file:IO[str], remove:str):
  """Highlight token.
  """
  return ('tokenHighlighting', {'file': file, 'remove': remove})

@cli.command('highlight')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=Range(), help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def highlight_cmd(file:IO[str], interactionId:int=0, where:Range=None):
  """Highlight file.
  """
  return ('highlight', {'file': file, 'interactionId': interactionId, 'where': where})

@cli.command('give')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=Range(), help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def give_cmd(file:IO[str], force:str, interactionId:int=0, where:Range=None, expr:str=''):
  """Fill a goal.
  """
  return ('give', {'file': file, 'interactionId': interactionId, 'where': where})

@cli.command('refine')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def refine_cmd(file:IO[str], interactionId:int=0, where:Range=None, expr:str=''):
  """Refine: makes new holes for missing arguments.
  """
  return ('refine', {'file': file, })

@cli.command('intro')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=Range(), help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
@click.option('-w', '--whether', 'whether', type=bool, help='Whether to (?), defaults to false')
def intro_cmd(file:IO[str], whether:bool, interactionId:int=0, where:Range=None, expr:str=''):
  """Give information about holes.
  """
  return ('intro', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where, 'whether': whether})

@cli.command('refine_or_intro')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=Range(), help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
@click.option('-w', '--whether', 'whether', type=bool, help='Whether to (?), defaults to false')
def refine_or_intro_cmd(file:IO[str], whether:bool, interactionId:int=0, where:Range=None, expr:str=''):
  """Refine. Partial give: makes new holes for missing arguments.
  """
  return ('intro', {'file': file, 'expr': expr, 'interactionId': interactionId, 'where': where, 'whether': whether})

@cli.command('context')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def context_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Context of the goal.
  """
  return ('context', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('helper_function')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def helper_function_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Create type of application of new helper function that would solve the goal.
  """
  return ('helper_function', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('infer')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def infer_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Infer type.
  """
  return ('infer', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('goal_type')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def goal_type_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Goal type.
  """
  return ('goal_type', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('elaborate_give')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def elaborate_give_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Grabs the current goal's type and checks the expression in the hole against it. Returns the elaborated term.
  """
  return ('elaborate_give', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('goal_type_context')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def goal_type_context_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Displays the current goal and context.
  """
  return ('goal_type_context', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('goal_type_context_infer')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def goal_type_context_infer_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Displays the current goal and context and infers the type of an expression.
  """
  return ('goal_type_context_infer', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('goal_type_context_check')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def goal_type_context_check_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Grabs the current goal's type and checks the expression in the hole against it.
  """
  return ('goal_type_context_check', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('show_module_contents')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-r', '--rewrite', 'rewrite', type=str, default='Simplified', help='Rewrite modes, can be one of AsIs, Instantiated, HeadNormal, Simplified, Normalised, defaults to Simplified')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def show_module_contents_cmd(file:IO[str], rewrite:str='Simplified', interactionId:int=0, where:Range=None, expr:str=''):
  """Shows all the top-level names in the given module, along with their types. Uses the scope of the given goal.
  """
  return ('show_module_contents', {'file': file, 'rewrite': rewrite, 'expr': expr, 'interactionId': interactionId, 'where': where})

@cli.command('make_case')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def make_case_cmd(file:IO[str], interactionId:int=0, where:Range=None, expr:str=''):
  """Pattern match on variables (case split).
  """
  return ('make_case', {'file': file, 'interactionId': interactionId, 'where': where, 'expr': expr})

@cli.command('why_in_scope')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
def why_in_scope_cmd(file:IO[str], interactionId:int=0, where:Range=None, expr:str=''):
  """Explain why a keyword is in scope.
  """
  return ('why_in_scope', {'file': file, 'interactionId': interactionId, 'where': where, 'expr': expr})

@cli.command('compute')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
@click.option('-i', '--interactionId', 'interactionId', type=int, default=0, help='Interaction id, defaults to 0')
@click.option('-w', '--where', 'where', type=str, default=None, help='Position of file specified as ((start₁, end₁), (start₂, end₂)) or defaults to none. Note: for most commands, in case of no position, an expr needs to be specified')
@click.option('-c', '--computeMode', 'computeMode', type=str, default='DefaultCompute', help='Computation mode, can be one of DefaultCompute, IgnoreAbstract, UseShowInstance, defaults to DefaultCompute')
def compute_cmd(file:IO[str], computeMode:str='DefaultCompute', interactionId:int=0, where:Range=None, expr:str=''):
  """Compute the normal form of either selected code or given expression.
  """
  return ('compute', {'file': file, 'interactionId': interactionId, 'where': where, 'expr': expr, 'computeMode': computeMode})

@cli.command('why_in_scope_toplevel')
@click.option('-f', '--file', 'file', type=click.File('r'), multiple=False, help='Path of file to load (absolute or relative).')
@click.option('-e', '--expr', 'expr', type=str, default='', help='Expression, in case no position (--where) is given')
def why_in_scope_toplevel_cmd(file:IO[str], expr:str=''):
  """Explain why a keyword is in scope, entire file.
  """
  return ('why_in_scope_toplevel', {'file': file, 'expr': expr})

@cli.command('show_version')
def show_version_cmd():
  """Show version.
  """
  return ('show_version', {})

@cli.command('abort')
def abort_cmd():
  """Abort currently ongoing action.
  """
  return ('abort', {})


if __name__ == '__main__':
  cli()

