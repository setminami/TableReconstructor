# -*- coding: utf-8 -*-

''' class snnipets
# -*- coding: utf-8 -*-
from sub_commands import SubCommands
import argparse

class Generate(SubCommands):
  """ generate command """
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
    pass
'''
import os, argparse

class SubCommands:
  """
  table_reconstructor subcommands abstract class
  concretes class rules:
  - class名を全小文字化したものがsubcommand名になる
  - git commandのように、entryをまるごと渡すことはしない、少なくともwrapperはpythonで書く
  """
  # 各継承先で実装
  __name = ''
  __aliases = []
  __help = 'AAA'

  # children classes must have ...
  # 継承先で設定されているため、readonly
  @property
  def command_name(self):
    if self.__name == '':
      self.__name = self.__class__.__name__.lower()
    return self.__name

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
    dont call from exchanger.__init__()
    """
    command = cls.__init__()
    from table_reconstructor import TableReconstructor
    assert isinstance(exchanger, TableReconstructor)
    exchanger.regist_command(command)

  def run(self, **kwargs): assert True

  def makeArgparse(self, subparser):
    """ 個別optionを登録したargparseをsubparseにして返す """
    return subparser.add_parser(self.command_name, aliases=self.aliases, help=self.help)
