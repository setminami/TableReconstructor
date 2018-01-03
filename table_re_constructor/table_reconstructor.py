#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re
from functools import reduce
import argparse

# global settings.
VERSION = '0.1.0'
output_formats = ['csv', 'tsv']
init_command = ['initialize', 'init', 'i']
generate_command = ['generate', 'gen', 'g']

class TableReConstructor:
  """ 具象操作に流すための、utility的位置づけ"""
  DEBUG = True
  # DEBUG出力用 jsonは別扱い
  sub_commands = {}
  output_delimiters = [',', '\t']

  def __init__(self):
    if __name__ == '__main__':
      self.ARGS = TableReConstructor.ArgParser()
      pass

  def regist_subcommands(self, command):
    from sub_commands import SubCommands
    assert issubclass(command, SubCommands)
    sub_commands.update({command.command_name: command})

  def test(self):
    args = self.ARGS
    argvs = sys.argv
    enc = args.encode
    from xlsx import XLSX
    print(args)
    if args.subcmd_name in init_command:
      from settings import SettingProcessor
      # 初期化モード
      tmp = './template.xlsx' if args.template_xlsx == None else args.template_xlsx
      setting_file = fr'{os.path.splitext(os.path.expanduser(tmp))[0]}.yaml'
      print(tmp)
      settings = SettingProcessor(setting_file, enc)
      settings.checkSettingFile()
    elif args.subcmd_name in generate_command:
      fileloc = os.path.abspath(os.path.expanduser(args.file))
      # Memo: @property 使う
      o = self.output_formats.index(args.output_format)
      out = (self.output_formats[o], self.output_delimiters[o])
      x = XLSX(fileloc, args.output, enc, out)
      # sys.setrecursionlimit(1024 * 8)
      j = x.generateJSON(sheet_name=args.root_sheet)
      jsonfilename = fr'{os.path.splitext(fileloc)[0]}.json'
      with open(jsonfilename, 'w', encoding=enc) as f:
        try:
          f.write(json.dumps(j, sort_keys=True, indent=args.human_readable) \
                                        if args.human_readable > 0 else json.dumps(j))
        except:
          errorout(6, jsonfilename)
        else:
          print(f'Output json Success -> {jsonfilename}')
    else:
      pass
    pass

  def ArgParser(self):
    progname = os.path.basename(__file__)
    argParser = argparse.ArgumentParser(prog=__file__, description='',
                                        usage=f'{progname} sub-command [options]')
    # ToDo: 一般化
    outs = reduce(lambda l, r: f'{l} | {r}', output_formats)
    # Version desctiprtion
    argParser.add_argument('-v', '--version',
                        action='version', version=f'{progname} {VERSION}')
    # see. https://docs.python.org/3/library/argparse.html
    subParsers = argParser.add_subparsers(dest='subcmd_name', metavar='', help='sub-commands')
    init_parser = subParsers.add_parser(init_command[0], aliases=init_command[1:], help='init help')
    gen_parser = subParsers.add_parser(generate_command[0], aliases=generate_command[1:], help='generate help')
    # Memo: command形式の方が素直か？
    init_parser.add_argument('-tx', '--template_xlsx',
                            nargs='?', type=str, default='', metavar='path/to/outputfile(.xlsx)',
                            help='This is an initialize helper option.\n\
                            Generate template xlsx file based on same filename.yaml.\
                            \n**And if you set this, other options are ignored.** will be subcommand.')

    gen_parser.add_argument('-f', '--file',
                            nargs='?', type=str, default='./Samples/cheatsheet.xlsx',
                            metavar='path/to/inputfile',
                            help='Set path/to/input xlsx filename.')
    gen_parser.add_argument('-hr', '--human_readable',
                            type=int, default=0, metavar='tabsize',
                            help='set indent size by numeric value, Output humanreadable json files.')
    gen_parser.add_argument('-r', '--root_sheet',
                            nargs='?', type=str, default='root', # Default root sheet name
                            metavar='sheetname',
                            help='set a sheetname in xlsx book have. \nconstruct json tree from the sheet as root item. "root" is Default root sheet name.')
    argParser.add_argument('-e', '--encode',
                            type=str, default='utf-8', metavar='"python codec sign"',
                            help='set default charactor code. When not set this, it treated with "utf-8"')
    argParser.add_argument('-of', '--output_format',
                            nargs='?', type=str, default=output_formats[1],
                            metavar=f'{outs}',
                            help=f'-of [{outs}] \nOutput with the format, If you set, output formfiles to /path/to/output/Excelfilename/sheetname[{outs}] \nThis IS DEBUG feature')
    argParser.add_argument('-o', '--output',
                            nargs='?', type=str, default='output', metavar='path/to/outputfile(.json)',
                            help='-o path/to/outputfile \nOutput interpreted json files.')
    return argParser.parse_args()

def errorout(e, additonal=''):
  """ 強制的に止める sys.stderr へ出力 """
  errors = ['OK', 'sheets link not found.', 'schema not found.',
              'root sheet not found.', 'Unrecognized type were found.', 'Unknown accumulator!',
              'Output json has failed.']
  assert e < len(errors) and e >= 0
  print(f'{errors[e]} : {additonal}', file=sys.stderr)
  sys.exit(e)

if __name__ == '__main__':
  ins = TableReConstructor()
  ins.test()
