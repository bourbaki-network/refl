#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import subprocess
import tempfile
from os import path
from typing import *

from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, WordCompleter
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from cmd_args import *
from config import *
from util.log import Logging

log = Logging(LOGLEVEL)()


class Repl:
  def __init__(self):
    self.commands = [
      'compile', 'load', 'constraints', 'metas', 'show_module_contents_toplevel',
      'search_about_toplevel', 'solveAll', 'solveOne', 'autoAll', 'autoOne', 'auto',
      'infer_toplevel', 'compute_toplevel', 'load_highlighting_info', 'tokenHighlighting',
      'highlight', 'give', 'refine', 'intro', 'refine_or_intro', 'context', 'helper_function',
      'infer', 'goal_type', 'elaborate_give', 'goal_type_context', 'goal_type_context_infer',
      'goal_type_context_check', 'show_module_contents', 'make_case', 'why_in_scope', 'compute',
      'why_in_scope_toplevel', 'show_version', 'abort'
    ]

    self.arguments = [
      '--file', '--backend', '--cmds', '--rewrite', '--expr', '--interactionId', '--where',
      '--computeMode', '--remove', '--whether'
    ]

    self.static = [
      "GHC", "GHCNoMain", "LaTeX", "QuickLaTeX", "AsIs", "Instantiated", "HeadNormal",
      "Simplified", "Normalised", "DefaultCompute", "IgnoreAbstract", "UseShowInstance", "Remove",
      "Keep", "WithForce", "WithoutForce"
    ]

    self.style = Style.from_dict({
      'pygments.comment': '#888888 bold',
      'pygments.keyword': '#ff88ff bold',
      'bottom-toolbar': '#222 bg:#ccc'
    })

    self.session = None
    self.temp = None

  def get_local_files(self) -> List[str]:
    return os.listdir(os.getcwd())

  def other(self):
    now = datetime.datetime.now()
    return path.split(os.getcwd())[-1] + ' - ' + ':'.join(
      [format(now.hour, '02'),
       format(now.minute, '02'),
       format(now.second, '02')])

  def run(self, history='~/.refl_history'):
    history = path.abspath(path.expanduser(history))

    if not path.exists(history):
      os.mknod(history)

    self.session = self.session if self.session is not None else PromptSession(
      history=FileHistory(history))
    self.temp = self.temp if self.temp is not None else tempfile.NamedTemporaryFile(suffix='.agda',
                                                                                    mode='a+').name

    header = 'module {name} where'.format(name=path.basename(self.temp)[:-5])

    with open(self.temp, 'a+') as temp:
      temp.write(header + '\n\n')

    while 1:
      user_input = self.session.prompt(
        HTML(
          '  <b><style fg="hotpink">refl ♠</style></b> <b><style fg="#666">{date}</style></b> <b><style fg="hotpink">⟹</style></b>  '
          .format(date=self.other())),
        auto_suggest=AutoSuggestFromHistory(),
        completer=WordCompleter(self.commands + self.get_local_files() + self.static
                                + self.arguments,
                                ignore_case=True),
        style=self.style,
        bottom_toolbar=HTML(
          '  <b><style bg="hotpink">Refl ♠</style></b> the Agda REPL. Docs: http://monoid.space/refl.html'
        ))

      user_input = user_input.strip()

      # input not empty
      if user_input != '':
        # agda command
        if user_input[0] == ':':
          user_input = user_input[1:]
          print(user_input)

        # shell command
        elif user_input[0] == '!':
          user_input = user_input[1:]
          subprocess.call(user_input, shell=True)
        # clear shell
        elif user_input == 'clear' or user_input == 'c':
          subprocess.call('clear', shell=True)
        # clear repl history
        elif user_input == 'new':
          with open(self.temp, 'w') as temp:
            temp.write(header + '\n\n')
        # agda code
        else:
          with open(self.temp, 'a+') as temp:
            temp.write('''{input}\n\n'''.format(input=str(user_input)))
            temp.close()

          subprocess.call(['agda', '--no-main', '--compile', self.temp], cwd='/tmp')
