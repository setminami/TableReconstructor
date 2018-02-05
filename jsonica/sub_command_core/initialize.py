# -*- coding: utf-8 -*-
from . import SubCommands
from jsonica import errorout
import os

class Initialize(SubCommands):
  """ initialize command """
  VERSION = '0.1.0'

  __aliases = ['init', 'i']
  __help = 'create formated workbook template.'

  def __init__(self):
    super().__init__()

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
    setting_file = r'%s.yaml'%os.path.splitext(os.path.expanduser(args.template_xlsx))[0]
    if os.path.exists(setting_file):
      print(r'Setting file found on %s'%setting_file)
    else:
      errorout(8, r'Please make sure [%s] location?'%setting_file)
    settings = SettingProcessor(setting_file, args.template_xlsx, args.encoding)
    settings.check_settingfile()
    try:
      settings.create_sheets()
    except SettingsError as se:
      print(se)
    else:
      settings.save()
      print('Construct xlsx file Success ➡️  %s'%args.template_xlsx)

  def make_argparse(self, subparser):
    myparser = super().make_argparse(subparser)
    myparser.add_argument('-tx', '--template_xlsx',
                            nargs='?', type=str, default='./template.xlsx', metavar='path/to/outputfile(.xlsx)',
                            help='This is an initialize helper option.\n\
                            Generate template xlsx file based on same filename.yaml.\
                            \n**And if you set this, other options are ignored.** will be subcommand.')
