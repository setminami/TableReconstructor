# -*- coding: utf-8 -*-
from . import SubCommands
from table_reconstructor import errorout
import os

class Initialize(SubCommands):
  """ initialize command """
  VERSION = '0.0.9'

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

  def __run__(self, **kwargs):
    args = kwargs['args']
    from settings import SettingProcessor, SettingsError
    # 初期化モード
    setting_file = fr'{os.path.splitext(os.path.expanduser(args.template_xlsx))[0]}.yaml'
    if os.path.exists(setting_file):
      print(fr'Setting file found on {setting_file}')
    else:
      errorout(8, fr'Please make sure [{setting_file}] location?')
    settings = SettingProcessor(setting_file, args.template_xlsx, args.encoding)
    settings.checkSettingFile()
    try:
      settings.createSheets()
    except SettingsError as se:
      print(se)
    else:
      settings.save()
      print(f'Construct xlsx file Success ➡️  {args.template_xlsx}')
    pass

  def makeArgparse(self, subparser):
    myparser = super().makeArgparse(subparser)
    myparser.add_argument('-tx', '--template_xlsx',
                            nargs='?', type=str, default='./template.xlsx', metavar='path/to/outputfile(.xlsx)',
                            help='This is an initialize helper option.\n\
                            Generate template xlsx file based on same filename.yaml.\
                            \n**And if you set this, other options are ignored.** will be subcommand.')
    pass
