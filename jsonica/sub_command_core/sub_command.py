# -*- coding: utf-8 -*-

''' class snnipets
# -*- coding: utf-8 -*-
from sub_commands import SubCommands
from jsonica import errorout
import argparse

class Generate(SubCommands):
  """ generate command """
  VERSION = '0.0.1'

  __aliases = ['gen', 'g']
  __help = 'generate help'

  def __init__(self):
    super().__init__()
    pass

  @property
  def command_names(self): return [self.command_name] + self.aliases
  @property
  def aliases(self): return self.__aliases
  @property
  def help(self): return self.__help

  def run(self, **kwargs):
    # each process brabrabra
    pass

  def makeArgparse(self, subparser):
    myparser = super().makeArgparse(subparser)
    # write each subcommand arg processor here
    myparser.add_argument('-v', '--version',
                        action='version', version='{} {}'.format(self.command_name, VERSION))
    pass
'''
import os, argparse
from jsonica import PROGNAME

class SubCommands:
  """
  jsonica subcommands abstract class
  concretes class rules:
  - class名を全小文字化したものがsubcommand名になる
  - git commandのように、entryをまるごと渡すことはしない、少なくともwrapperはpythonで書く
  """
  __name = ''
  # 各継承先で実装
  __aliases = []
  __help = '---'

  # children classes must have ...
  # 基底クラス管理
  @property
  def command_name(self):
    if self.__name == '':
      # subcommand名はクラス名小文字
      self.__name = self.__class__.__name__.lower()
    return self.__name

  # 継承先で設定されているため、readonly
  @property
  def command_names(self): assert True
  @property
  def aliases(self): assert True
  @property
  def help(self): assert True

  def __init__(self):
    pass

  @classmethod
  def regist_command(cls, exchanger):
    """
    subcommand 登録
    **dont call from exchanger.__init__()**
    """
    command = cls.__init__()
    from jsonica import Jsonica
    assert isinstance(exchanger, Jsonica)
    exchanger.regist_command(command)

  def __run__(self, **kwargs): assert True

  def makeArgparse(self, subparser):
    """ 個別optionを登録したargparseをsubparseにして返す """
    parser = subparser.add_parser(self.command_name, aliases=self.aliases, help=self.help)
    parser.add_argument('-v', '--version',
                        action='version', version='%s %s v%s'.%(PROGNAME, self.command_name, self.VERSION))
    return parser
