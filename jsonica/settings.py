# -*- coding: utf-8 -*-
import yaml
from xlsx import XLSX
from util import Hoare

# Yaml 設定値
ATTACH = ('attach', ['xlsx'])
ROOT = 'root'
SHEET_NAME = 'sheet_name'
COLUMNS = 'columns'
COLUMN_FLAG = 'column'
COL_NAME = 'title'
NOTES = 'notes'
SCHEMA = 'schema'
SCHEMA_TYPE = 'type'
CHILD_SHEET = 'child_names'
REL_ITEM = 'relations'

class SettingProcessor:
  """" yaml 具象処理 """
  def __init__(self, fileloc, out, enc):
    self.settings = fileloc
    self.out = out
    self.enc = enc

  def check_settingfile(self):
    with open(self.settings, 'r') as f:
      self.setting_data = yaml.safe_load(f)
    if self.setting_data[ATTACH[0]] == ATTACH[1][0]:
      self.processor = XLSX(self.settings, self.enc)
    Hoare.P(self.processor)

  def create_sheets(self, item=ROOT, name=None):
    root_item = self.setting_data[item]
    if root_item:
      sheet_name = name if (name and name != '') else root_item[SHEET_NAME]
      if sheet_name:
        sheet = self.processor.generate_sheet(sheet_name)
      else:
        raise SettingsError('Invalid sheet name', sheet_name)
      cols = root_item[COLUMNS]
      if cols:
        for i, c in enumerate(cols):
          if not c[COLUMN_FLAG]: continue
          # care off-by-one
          cell = sheet.cell(row=1, column=i + 1, value=c[COL_NAME])
          schema = '{}'.format(c[SCHEMA]).lower()
          XLSX.put_cell_comment(cell, '# {}\n{}'.format(c[NOTES], schema))
          if c[SCHEMA][SCHEMA_TYPE] == 'array':
            for csheet in c[CHILD_SHEET]:
              self.create_sheets(c[REL_ITEM], csheet)
      else:
        # 設定によってエラーとはいえないケースあり
        print('%s : the item no columns.'%sheet_name)
    else:
      raise SettingsError('root item not set', self.setting_data)

  def save(self):
    Hoare.P(self.out.endswith('.xlsx'))
    output = self.out
    print(r'generate template to {}'.format(output))
    self.processor.book.save(output)

class SettingsError(Exception):
  """ ローカル設定 に関するエラー """
  def __init__(self, message, item):
    self.message = message
    self.about_item = item
