#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, enum, re
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
      x = xlsx.XLSX(fileloc, args.output, args.output_format)
      x.generateJSON()
    pass

  @staticmethod
  def ArgParser():
    argParser = argparse.ArgumentParser(prog=__file__, description='',
                                        usage='table_reconstructor [options]')
    outs = '[ csv | tsv ]'
    # Version desctiprtion
    argParser.add_argument('-v', '--version',
                        action='version', version='TableReConstructor %s'%VERSION)
    argParser.add_argument('-f', '--file',
                            nargs='?', type=str, default='./Samples/cheatsheet.xlsx',
                            help='')
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
    return argParser.parse_args()

def __print(str, flag=TableReConstructor.DEBUG):
  if flag:
    print(str)
  pass

class Validator(str, enum.Enum):
  """ 対応validator """
  jsonschema = 'jsonschema'

class TypeSign(str, enum.Enum):
  """ Type adhoc """
  # https://tools.ietf.org/html/draft-zyp-json-schema-04
  # RFC 4627#2.1 https://tools.ietf.org/html/rfc4627
  OBJ = 'object'
  ARRAY = 'array'

  STRING = 'string'
  NUM = 'number'

  FALSE = 'false'
  TRUE = 'true'

  JSON_NULL = 'null'


if __name__ == '__main__':
  ins = TableReConstructor()
  ins.test()
