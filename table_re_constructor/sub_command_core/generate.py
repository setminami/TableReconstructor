# -*- coding: utf-8 -*-
from . import SubCommands
from table_reconstructor import output_formats, output_delimiters, errorout
import os, json, argparse

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
    args = kwargs['args']
    fileloc = os.path.abspath(os.path.expanduser(args.file))
    # Memo: @property 使う
    o = output_formats.index(args.output_format)
    out = (output_formats[o], output_delimiters[o])
    from xlsx import XLSX
    print(f'Analyzing... {fileloc}')
    x = XLSX(fileloc, args.output, args.encoding, out)
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
    myparser.add_argument('-f', '--file',
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
                            nargs='?', type=str, default='output/', # action=AnalyzeJSONOutPath,
                            metavar='path/to/outputfile(.json)',
                            help='Output interpreted json files. If not set, output to ./output/[source_Exel_name].json')
    pass

  def __analyzeJSONOutPath(self, fileloc, path):
    """ 正当な出力json名を推測する """
    if path.endswith('/'): # default含む
      print('*'*2)
      p = os.path.expanduser(path)
      # Excelと同名
      fname = os.path.splitext(os.path.basename(fileloc))[0]
      jsonfilename = fr'{p}{fname}.json'
    elif path.endswith('.json'):
      print('*'*3)
      # 指定されたファイル名まま
      jsonfilename = os.path.expanduser(path)
    else: # '/'で終わらず、json拡張子無し文字列で終わっている
      print('*'*4)
      p = os.path.expanduser(path)
      jsonfilename = fr'{p}.json'
    return jsonfilename

# argparse actions
# -o を指定しないとcallされないため、pending
# class AnalyzeJSONOutPath(argparse.Action):
#  """ 正当な出力json名を推測する """
#  def __call__(self, parser, namespace, values, option_string=None):
#    print(parser)
#    print(namespace)
#    print(values)
#    print(option_string)
