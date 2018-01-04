# -*- coding: utf-8 -*-
from . import SubCommands

class Initialize(SubCommands):
  """ initialize command """
  VERSION = '0.0.1'

  __aliases = ['init', 'i']
  __help = 'create formated workbook template.'

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
    pass

  def makeArgparse(self, subparser):
    myparser = super().makeArgparse(subparser)
    myparser.add_argument('-tx', '--template_xlsx',
                            nargs='?', type=str, default='', metavar='path/to/outputfile(.xlsx)',
                            help='This is an initialize helper option.\n\
                            Generate template xlsx file based on same filename.yaml.\
                            \n**And if you set this, other options are ignored.** will be subcommand.')
    pass
