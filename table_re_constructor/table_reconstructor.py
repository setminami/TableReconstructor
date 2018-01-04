#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re
import argparse
from functools import reduce

# global settings.
VERSION = '0.1.0'
PROGNAME = os.path.basename(__file__)

codec_help_url = 'https://docs.python.org/3.6/library/codecs.html#standard-encodings'

class TableReConstructor:
  """ 具象操作に流すための、utility的位置づけ"""
  DEBUG = True
  # DEBUG出力用 jsonは別扱い
  # 簡単なので、仮実装　vs. 素直にargparse actionに直接run()を割り当てるか、その場合前処理をどうするか。
  sub_commands = {}

  def __init__(self):
    pass

  def regist_subcommand(self, command):
    """
    sub_commandsの型に依存させないためのIF
    型変更の必要がでたら、局所的に操作を書き換える
    """
    from sub_command_core.sub_command import SubCommands
    assert issubclass(command.__class__, SubCommands)
    # 衝突注意
    for name in command.command_names:
      assert not (name in self.sub_commands.keys()),\
                f'"{name}" collision were detected in {self.sub_commands.keys()}'
      # Memo: commandは参照であること。tupleへのrefactoring注意
      self.sub_commands.update({name: command})

  @property
  def sub_command_names(self):
    return self.sub_commands.keys()

  def test(self):
    args = self.ARGS
    enc = args.encoding
    subcommand = self.sub_commands[args.subcmd_name]
    subcommand.run(args=args)
#    if args.subcmd_name in init_command:
#      from settings import SettingProcessor
#      # 初期化モード
#      tmp = './template.xlsx' if args.template_xlsx == None else args.template_xlsx
#      setting_file = fr'{os.path.splitext(os.path.expanduser(tmp))[0]}.yaml'
#      print(tmp)
#      settings = SettingProcessor(setting_file, enc)
#      settings.checkSettingFile()
    pass

  def prepareArgParser(self):
    argParser = argparse.ArgumentParser(prog=PROGNAME,
                                        description='generate complex structed JSON with analyzing META descripted file.')
    # Version desctiprtion
    argParser.add_argument('-v', '--version',
                        action='version', version=f'{PROGNAME} {VERSION}')

    # see. https://docs.python.org/3/library/argparse.html
    subParsers = argParser.add_subparsers(dest='subcmd_name', metavar='', help='sub-commands')
    for name, command in self.sub_commands.items():
      if name == command.command_name:
        subparser = command.makeArgparse(subParsers)
    argParser.add_argument('-e', '--encoding',
                            type=str, default='utf-8', metavar='{python built-in codec}',
                            help=f'Set default charactor encode. When not set this, it is treated as "utf-8".\
                            see also. {codec_help_url}')
    self.ARGS = argParser.parse_args()


def errorout(e, additonal=''):
  """ 強制的に止める sys.stderr へ出力 """
  errors = ['OK',
            'sheets link not found.', 'schema not found.',
            'root sheet not found.', 'Unrecognized item type were found.', 'Unknown accumulator!',
            'Output json has failed.', 'Unsupported table filetype found.']
  assert e < len(errors) and e >= 0
  print(f'{errors[e]} : {additonal}', file=sys.stderr)
  sys.exit(e)

if __name__ == '__main__':
  ins = TableReConstructor()
  # ToDo: subcommand 設定 https://github.com/setminami/TableReconstructor/issues/31
  from sub_command_core import (Initialize, Generate)
  # AdHoc: とりあえず仮実装 Plugin実装する際に再考
  for x in [Initialize(), Generate()]:
    ins.regist_subcommand(x)
  ins.prepareArgParser()
  ins.test()
