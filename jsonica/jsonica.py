#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import argparse
from util import Hoare

# global settings.
VERSION = '0.0.9'
PROGNAME = os.path.basename(__file__)

codec_help_url = 'https://docs.python.org/3.6/library/codecs.html#standard-encodings'

class Jsonica:
  """ 具象操作に流すための、utility的位置づけ"""
  DEBUG = True
  # DEBUG出力用 jsonは別扱い
  # 簡単なので、仮実装　vs. 素直にargparse actionに直接__run__()を割り当てるか、その場合前処理をどうするか。
  sub_commands = {}

  def __init__(self):
    pass

  def regist_subcommand(self, command):
    """
    sub_commandsの型に依存させないためのIF
    型変更の必要がでたら、局所的に操作を書き換える
    """
    from sub_command_core.sub_command import SubCommands
    Hoare.P(issubclass(command.__class__, SubCommands))
    # 衝突注意
    for name in command.command_names:
      Hoare.P(not (name in self.sub_commands.keys()),\
        '"{}" collision were detected in {}'.format(name, self.sub_commands.keys()))
      # NOTE: commandは参照であること。tupleへのrefactoring注意
      self.sub_commands.update({name: command})

  @property
  def sub_command_names(self):
    return self.sub_commands.keys()

  def test(self):
    args = self.ARGS
    subcommand = self.sub_commands[args.subcmd_name]
    subcommand.__run__(args=args)

  def prepareArgParser(self):
    argParser = argparse.ArgumentParser(prog=PROGNAME,
                                        description='generate complex JSON structure with analyzing META descripted file like xlsx.')
    # Version desctiprtion
    argParser.add_argument('-v', '--version',
                        action='version', version='%s %s'%(PROGNAME, VERSION))

    # see. https://docs.python.org/3/library/argparse.html
    subParsers = argParser.add_subparsers(dest='subcmd_name', metavar='', help='sub-commands')
    for name, command in self.sub_commands.items():
      if name == command.command_name:
        command.makeArgparse(subParsers)
    argParser.add_argument('-e', '--encoding',
                            type=str, default='utf-8', metavar='{python built-in codec}',
                            help='Set default charactor encode. When not set this, it is treated as "utf-8".\
                            see also. %s'%codec_help_url)
    self.ARGS = argParser.parse_args()

def errorout(e, additonal=''):
  """ 強制的に止める sys.stderr へ出力 """
  errors = ['OK',
            'sheets link not found.', 'schema not found.', # 1, 2
            'root sheet not found.', 'Unrecognized item type were found.', # 3, 4
            'Unknown accumulator!', 'Output json has failed.', # 5, 6
            'Unsupported table filetype found.', 'setting yaml file not found']
  Hoare.P(e < len(errors) and e >= 0)
  print('%s : %s'%(errors[e], additonal), file=sys.stderr)
  sys.exit(e)

def refactorCheck(validation): Hoare.P(validation, 'Have you made refactor??')

if __name__ == '__main__':
  ins = Jsonica()
  # NOTE: subcommand 設定 https://github.com/setminami/Jsonica/issues/31
  from sub_command_core import (Initialize, Generate)
  # FIXME: とりあえず仮実装 Plugin実装する際に再考
  for x in [Initialize(), Generate()]:
    ins.regist_subcommand(x)
  ins.prepareArgParser()
  ins.test()
