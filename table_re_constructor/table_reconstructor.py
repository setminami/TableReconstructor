#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, re
import argparse

VERSION = '0.1.0'

class TableReConstructor:
  """ 具象操作に流すための、utility的位置づけ"""
  DEBUG = True
  # DEBUG出力用 jsonは別扱い
  output_formats = ['csv', 'tsv']

  def __init__(self):
    if __name__ == '__main__':
      self.ARGS = TableReConstructor.ArgParser()
      pass

  def test(self):
    args = self.ARGS
    argvs = sys.argv
    enc = args.encode
    from xlsx import XLSX
    if '-gx' in argvs or '--generate_template_xlsx' in argvs:
      # 初期化モード
      tmp = 'template.xlsx' if args.generate_template_xlsx == None else args.generate_template_xlsx
      print(tmp)
    else:
      fileloc = os.path.abspath(os.path.expanduser(args.file))
      # ToDo: openpyxlでecodeが取れるか確認
      x = XLSX(fileloc, args.output, enc, args.output_format)
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
    outs = 'csv | tsv'
    # Version desctiprtion
    argParser.add_argument('-v', '--version',
                        action='version', version=f'{progname} {VERSION}')
    argParser.add_argument('-f', '--file',
                            nargs='?', type=str, default='./Samples/cheatsheet.xlsx',
                            metavar='path/to/inputfile',
                            help='Set path/to/input xlsx filename.')
    argParser.add_argument('-of', '--output_format',
                            nargs='?', type=str, default='', metavar=f'{outs}',
                            help=f'-of [{outs}] \nOutput with the format, If you set, output formfiles to /path/to/output/Excelfilename/sheetname[{outs}] \nThis IS DEBUG feature')
    argParser.add_argument('-o', '--output',
                            nargs='?', type=str, default='output', metavar='path/to/outputfile(.json)',
                            help='-o path/to/outputfile \nOutput interpreted json files.')
    # Memo: command形式の方が素直か？
    argParser.add_argument('-gx', '--generate_template_xlsx',
                            nargs='?', type=str, default='', metavar='path/to/outputfile(.xlsx)',
                            help='This is an initialize helper option.\n\
                            Generate template xlsx file based on same filename.yaml.\
                            \n**And if you set this, other options are ignored.** will be subcommand.')
    argParser.add_argument('-hr', '--human_readable',
                            type=int, default=0, metavar='tabsize',
                            help='set indent size by numeric value, Output humanreadable json files.')
    argParser.add_argument('-e', '--encode',
                            type=str, default='utf-8', metavar='"python codec sign"',
                            help='set default charactor code. When not set this, it treated with "utf-8"')
    argParser.add_argument('-r', '--root_sheet',
                            nargs='?', type=str, default='root', # Default root sheet name
                            metavar='sheetname',
                            help='set a sheetname in xlsx book have. \nconstruct json tree from the sheet as root item. "root" is Default root sheet name.')
    return argParser.parse_args()

def __print(str, flag=TableReConstructor.DEBUG):
  if flag:
    print(str)
  pass

def errorout(e, additonal=''):
  """ 出力細部はあとで調整すること """
  errors = ['OK', 'sheets link not found.', 'schema not found.',
              'root sheet not found.', 'Unrecognized type were found.', 'Unknown accumulator!']
  assert e < len(errors) and e >= 0
  print(f'{errors[e]} : {additonal}')
  sys.exit(e)

if __name__ == '__main__':
  ins = TableReConstructor()
  ins.test()
