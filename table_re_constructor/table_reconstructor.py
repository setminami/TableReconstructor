#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re
import argparse

# local
import xlsx

VERSION = '0.0.1'

class TableReConstructor:
  """ 具象操作に流すための、utility的位置づけ"""
  DEBUG = True
  # DEBUG出力用 jsonは別扱い
  output_formats = ['csv','tsv']

  def __init__(self):
    if __name__ == '__main__':
      self.ARGS = TableReConstructor.ArgParser()
      pass

  def test(self):
    args = self.ARGS
    argvs = sys.argv
    if '-gx' in argvs or '--generate_template_xlsx' in argvs:
      # 初期化モード
      tmp = 'template.xlsx' if args.generate_template_xlsx == None else args.generate_template_xlsx
      print(tmp)
    else:
      fileloc = os.path.abspath(os.path.expanduser(args.file))
      # ToDo: openpyxlでecodeが取れるか確認
      enc = 'utf-8'
      x = xlsx.XLSX(fileloc, args.output, args.output_format)
      # sys.setrecursionlimit(1024 * 8)
      j = x.generateJSON(sheet_name=args.root_sheet)
      _file, _ = os.path.splitext(fileloc)
      with open(fr'{_file}.json', 'w', encoding=enc) as f:
        f.write(json.dumps(j, sort_keys=True, indent=args.human_readable) \
                                    if args.human_readable > 0 else json.dumps(j))
    pass

  @staticmethod
  def ArgParser():
    progname = os.path.basename(__file__)
    argParser = argparse.ArgumentParser(prog=__file__, description='',
                                        usage=f'{progname} [options]')
    outs = '[ csv | tsv ]'
    # Version desctiprtion
    argParser.add_argument('-v', '--version',
                        action='version', version=f'{progname} {VERSION}')
    argParser.add_argument('-f', '--file',
                            nargs='?', type=str, default='./Samples/cheatsheet.xlsx',
                            help='Set path/to/xlsx filename.')
    argParser.add_argument('-of', '--output_format',
                            nargs='?', type=str, default='',
                            help='-of %s \nOutput with the format, If you set, output formfiles to /path/to/output/%s This IS DEBUG feature'%(outs, outs))
    argParser.add_argument('-o', '--output',
                            nargs='?', type=str, default='output',
                            help='-o /path/to/output \nOutput interpreted json files.')
    # Memo: command形式の方が素直か？
    argParser.add_argument('-gx', '--generate_template_xlsx',
                            nargs='?', type=str, default='',
                            help='-gx filename(.xlsx) \nThis is an initialize helper option.\n\
                            Generate template xlsx file based on same filename.yaml.\
                            \nAnd if you set this, other options are ignored.')
    argParser.add_argument('-hr', '--human_readable',
                            type=int, default=0,
                            help='set indent size by numeric value, Output humanreadable json files.')
    argParser.add_argument('-r', '--root_sheet',
                            nargs='?', type=str, default='root',
                            help='set a sheetname in xlsx book have. \nconstruct json tree from the sheet as root item. "root" is Default root sheet name.')
    return argParser.parse_args()

def __print(str, flag=TableReConstructor.DEBUG):
  if flag:
    print(str)
  pass

if __name__ == '__main__':
  ins = TableReConstructor()
  ins.test()
