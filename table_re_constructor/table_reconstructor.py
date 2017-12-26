#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json
import argparse

# local
import xlsx

VERSION = '0.0.1'

class TableReConstructor:
  """ """
  DEBUG = True
  # DEBUG出力用 jsonは別扱い
  output_formats = ['csv','tsv']

  def __init__(self):
    if __name__ == '__main__':
      self.ARGS = TableReConstructor.ArgParser()
      pass

  def test(self):
    args = self.ARGS
    fileloc = os.path.abspath(os.path.expanduser(args.file))
    x = xlsx.XLSX(fileloc, args.output, args.output_format)
    x.generateCSVs()
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
    return argParser.parse_args()

def __print(str, flag=TableReConstructor.DEBUG):
  if flag:
    print(str)
  pass

if __name__ == '__main__':
  ins = TableReConstructor()
  ins.test()
