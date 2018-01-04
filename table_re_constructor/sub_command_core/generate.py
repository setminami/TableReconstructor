# -*- coding: utf-8 -*-
from . import SubCommands
from table_reconstructor import errorout
import os, json, argparse
from functools import reduce

output_formats = ['csv', 'tsv']
output_delimiters = [',', '\t']

class Generate(SubCommands):
  """ generate command """
  VERSION = '0.1.0'

  __aliases = ['gen', 'g']
  __help = 'generate analyzed files as TEXT from META descritor file. (e.g., Excel)'

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
    args = kwargs['args']
    fileloc = os.path.abspath(os.path.expanduser(args.input))
    # Memo: @property 使う
    o = output_formats.index(args.output_format)
    out = (output_formats[o], output_delimiters[o])
    workpath = self.__treatFileTypes(fileloc)
    from xlsx import XLSX
    print(f'Analyzing... {fileloc}')
    x = XLSX(workpath, args.output, args.encoding, out)
    # sys.setrecursionlimit(1024 * 8)
    j = x.generateJSON(sheet_name=args.root_sheet)
    jsonfilename = self.__analyzeJSONOutPath(fileloc, args.output)
    with open(jsonfilename, 'w', encoding=args.encoding) as f:
      try:
        f.write(json.dumps(j, sort_keys=True, indent=args.human_readable) \
                                      if args.human_readable > 0 else json.dumps(j))
      except:
        errorout(6, jsonfilename)
      else:
        print(f'Output json Success -> {jsonfilename}')
    pass

  def makeArgparse(self, subparser):
    myparser = super().makeArgparse(subparser)
    outs = reduce(lambda l, r: f'{l} | {r}', output_formats)
    myparser.add_argument('-i', '--input',
                            nargs='?', type=str, default='./Samples/cheatsheet.xlsx',
                            metavar='path/to/inputfile',
                            help='Set path/to/input xlsx filename.')
    myparser.add_argument('-hr', '--human_readable',
                            type=int, default=0, metavar='tabsize',
                            help='set indent size by numeric value, Output humanreadable json files.')
    myparser.add_argument('-r', '--root_sheet',
                            nargs='?', type=str, default='root', # Default root sheet name
                            metavar='sheetname',
                            help='set a sheetname in xlsx book have. \nconstruct json tree from the sheet as root item. "root" is Default root sheet name.')
    myparser.add_argument('-o', '--output',
                            nargs='?', type=str, default='./output/', # action=AnalyzeJSONOutPath,
                            metavar='path/to/outputfile(.json)',
                            help='Output interpreted json and text formated sheet files. If not set, output to ./output/[source_METAFile_name].json and ./output/[source_METAFile_name].xlsx/[sheet_name.?sv]s')
    myparser.add_argument('-of', '--output_format',
                            nargs='?', type=str, default=output_formats[1],
                            metavar=f'{outs}',
                            help=f'''Output with the format, If you set, output formfiles to path/to/output/METAFile/sheetname.({outs}) \n(It\'ll be recommended, \
                            if you want to have communication with non Tech team without any gitconfiging.)''')
    pass

  def __analyzeJSONOutPath(self, fileloc, path):
    """ 正当な出力json名を推測する """
    # ToDo: 文字列ケース
    if path.endswith('/') or path == '.': # default含む
      if path == '.': path = './'
      p = os.path.expanduser(path)
      # Excelと同名
      fname = os.path.splitext(os.path.basename(fileloc))[0]
      jsonfilename = fr'{p}{fname}.json'
    elif path.endswith('.json'):
      # 指定されたファイル名まま
      jsonfilename = os.path.expanduser(path)
    else: # '/'で終わらず、json拡張子無し文字列で終わっている
      p = os.path.expanduser(path)
      jsonfilename = fr'{p}.json'
    return jsonfilename

  def __treatFileTypes(self, file):
    if file.endswith('.xlsx'):
      return file
    else:
      errorout(7, f'{file} format is not supported yet.')

# argparse actions
# -o を指定しないとcallされないため、pending
# class AnalyzeJSONOutPath(argparse.Action):
#  """ 正当な出力json名を推測する """
#  def __call__(self, parser, namespace, values, option_string=None):
#    print(parser)
#    print(namespace)
#    print(values)
#    print(option_string)
