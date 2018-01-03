# -*- coding: utf-8 -*-

import yaml
from xlsx import XLSX

class SettingProcessor:
  """" yaml 具象処理 """
  def __init__(self, fileloc, enc):
    self.settings = fileloc
    self.enc = enc
    pass

  def checkSettingFile(self):
    with open(self.settings, 'r') as f:
      self.setting_data = yaml.load(f)
    print(self.setting_data)
    # if self.setting_data['attach'] == 'xlsx':
    #  self.processor = XLSX()

  def __print(self, str, flag=False):
    if flag:
      print(str)
    pass
