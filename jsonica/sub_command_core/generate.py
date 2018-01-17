# -*- coding: utf-8 -*-
from . import SubCommands
from jsonica import errorout, refactorCheck
import os, sys, json, argparse, contextlib
from functools import reduce

output_formats = ['csv', 'tsv']
output_delimiters = [',', '\t']

SP_FILE = '-'

class Generate(SubCommands):
  """ generate command """
  VERSION = '0.0.9'

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

  def __run__(self, **kwargs):
    args = kwargs['args']
    # default option 対策 seelaso AnalyzeXSeparatedOutPath
    # https://github.com/setminami/Jsonica/issues/47
    refactorCheck(args.__class__.__name__ == 'Namespace')
    if not args.output_format:
      args.output_format = ('tsv', output_delimiters[1], './output/')
    self.args = args
    fileloc = os.path.abspath(os.path.expanduser(args.input))
    workpath = self.__treatFileTypes(fileloc)
    from xlsx import XLSX
    self.__print('Analyzing... %s'%fileloc)
    x = XLSX(workpath, args.encoding, args.output_format)
    # sys.setrecursionlimit(1024 * 8)
    j = x.generateJSON(sheet_name=args.root_sheet)
    with wild_open(args.output, encoding=args.encoding) as f:
      try:
        print(json.dumps(j, sort_keys=True, indent=args.human_readable) \
                    if args.human_readable > 0 else json.dumps(j), file=f)
      except:
        errorout(6, args.output)
      else:
        self.__print('Output json Success ➡️  %s'%args.output)
    pass

  def makeArgparse(self, subparser):
    myparser = super().makeArgparse(subparser)
    outs = reduce(lambda l, r: '{} | {}'.format(l, r), output_formats)
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
                            nargs='?', type=str, action=AnalyzeJSONOutPath,
                            metavar='path/to/outputfile(.json)',
                            help=f'Output interpreted json. If this set which endswith ".json" as set full filename, output jsonfile treated as the name. But when not set ".json", adopt original xlsx filename, like path/to/outputfile/[source_METAFile_name].json\
                            (-o has special filename "{SP_FILE}" as STDOUT, and when set like "-o {SP_FILE}", all other stdout messages were masked.)')
    myparser.add_argument('-of', '--output_format',
                            nargs='?', type=str, action=AnalyzeXSeparatedOutPath, # (xsv, path)になるので注意
                            metavar='(%s):path/to/outputdir'%outs,
                            help='''Output with the format, If you set this, output formfiles to path/to/[source_METAFile_name].xlsx/[sheetname.?sv]s It\'ll be recommended,
                            if you want to have communication with non Tech team without any gitconfiging.''')
    pass

  def __treatFileTypes(self, file):
    if file.endswith('.xlsx'):
      return file
    else:
      errorout(7, '%s format is not supported yet.'%file)

  def __print(self, msg):
    if not (self.args.output == SP_FILE):
      print(msg)

# argparse actions
class AnalyzeJSONOutPath(argparse.Action):
  """ 正当な出力json名を推測する """
  def __call__(self, parser, namespace, values, option_string=None):
    path, fileloc = values, namespace.input
    if path.endswith('.json'):
      # 指定されたファイル名まま
      jsonfilename = os.path.expanduser(path)
    elif path == SP_FILE:
      jsonfilename = path
    else:
      p = os.path.expanduser(path)
      if not os.path.isdir(p):
        os.path.makedirs(p, exist_ok=True)
      # Excelと同名
      fname = os.path.splitext(os.path.basename(fileloc))[0]
      jsonfilename = os.path.join(p, r'%s.json'%fname)
    namespace.output = jsonfilename

class AnalyzeXSeparatedOutPath(argparse.Action):
  """ sv出力先と形式を解析する """
  DEBUG = False
  def __call__(self, parser, namespace, values, option_string=None):
    if self.DEBUG:
        print('{} called: {}'.format(self.__class__.__name__, values))
    args = values.split(':')
    if len(args) != 2:
      raise argparse.ArgumentTypeError('''{} {} have to separate ?sv and outputpath with ":"
                                            e.g., tsv:path/to/output'''.format(option_string ,values))
    elif not (args[0] in output_formats):
      raise argparse.ArgumentTypeError('%s %s have to be picked from %s'%(option_string, args[0], output_formats))
    o = output_formats.index(args[0])
    namespace.output_format = (args[0], output_delimiters[o], args[1])

@contextlib.contextmanager
def wild_open(filename=None, encoding='utf-8'):
  if filename and filename != SP_FILE:
    fh = open(filename, 'w', encoding=encoding)
  else:
    fh = sys.stdout
  try:
    yield fh
  finally:
    if fh is not sys.stdout:
      fh.close()
