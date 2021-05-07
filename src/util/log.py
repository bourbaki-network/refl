#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from typing import *

import coloredlogs

from config import *


def logger(level: str = 'DEBUG'):

  logFormatter: Any = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
  logger: Any = logging.getLogger(__name__)
  logger.setLevel(getattr(logging, level.upper()))

  return logger


class Logging:
  def __init__(self: Any, level: str = 'DEBUG'):
    self.logger = logger(level)
    coloredlogs.install(logger=self.logger)

  def __call__(self: Any):
    return self.logger
