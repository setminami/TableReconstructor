# -*- coding: utf-8 -*-
# this made for python3
import os, sys
import csv, openpyxl
from table_reconstructor import TableReConstructor, Validator, TypeSign
from util import Util

class XLSX:
  """ """
  DEBUG = True
  # childへのリンクを示す接頭辞
  sheet_link_sign = 'sheet://'
  # topレベルを示すシート名
  root_name = 'root'

  def __init__(self, file, output_path, forms=None):
    print(file)
    self.filepath = file
    self.output_path = output_path
    self.format = forms
    self.book = openpyxl.load_workbook(self.filepath, keep_vba=True, data_only=False)
    pass

  def generateJSON(self, sheet_name=root_name):
    dest_dir = self.output_path
    os.makedirs(dest_dir, exist_ok=True)
    sheets = self.__nameToSheets()
    sheet_names = list(sheets.keys())
    print(sheet_name)
    print(sheet_names)
    print(sheets)
    assert sheet_name in sheet_names
    root_sheet = sheets[sheet_name]
    columns = []
    for i, row in enumerate(root_sheet.iter_rows()):
      if self.format:
        self.__outputCSV(dest_dir, root_sheet)
        pass
      for j, cell in enumerate(row):
        v = cell.value
        print(v)
        if i == 0:
          # cell.commentは必ずつくが、中身がない場合はNone
          if hasattr(cell, "comment") and cell.comment:
            # column 準備
            columns.append((v, Util.runtimeDictionary(cell.comment.text)))
            print('%s : %s'%(columns[j], v))
          else:
            self.errorout(2, 'sheet = {}, col = {}, row = {}'.format(sheet_name, i, j))
        else:
          if isinstance(v, str) and v.startswith(XLSX.sheet_link_sign):
            link = v.lstrip(XLSX.sheet_link_sign)
            if link in sheet_names:
              self.generateJSON(link)
            else:
              self.errorout(1, 'sheet = from {} to {}, col = {}, row = {}'.format(sheet_name, link, i, j))
              pass
          else:
            print(j)
            print('%s : %s'%(columns[j][0], v))
            self.typeValidator(v, columns[j])
    pass

  def __outputCSV(self, base_path, sheet):
    assert self.format in TableReConstructor.output_formats
    xdest = os.path.join(base_path, self.format)
    os.makedirs(xdest, exist_ok=True)
    xdest_path = os.path.join(xdest, sheet.title + '.' + self.format)
    print(" > %s"%xdest_path)
    with open(xdest_path, 'w', encoding='utf-8') as f:
      writer = csv.writer(f)
      for cols in sheet.rows:
        writer.writerow([str(col.value or '') for col in cols])

  def __nameToSheets(self):
    """
    sheetを{sheet名:sheet}形式にして返す
    instance 生成後、実行中のExcel更新は考えない
    """
    if not hasattr(self, '__sheets_cache'):
      self.__sheets_cache = {s.title: s for s in self.book.worksheets}
    return self.__sheets_cache

  def errorout(self, e, additonal=''):
    """ 出力細部はあとで調整すること """
    errors = ['OK', 'sheets link not found.', 'scheme not found.']
    assert e < len(errors)
    print('{} : {}'.format(errors[e], additonal))
    sys.exit(e)

  def typeValidator(self, value, type_desc, validator=Validator.jsonschema):
    """ Validator switch"""
    __type = type_desc[0]
    raw = '\"{}\": {}'.format(type_desc[0], '%s'%('\"%s\"'%value if __type == TypeSign.STRING else value))
    # jsonschema による型チェック
    if validator == Validator.jsonschema:
      from jsonschema import Draft4Validator
      print('%s < %s : %s >'%(value, type_desc[0], type_desc[1]))
      pass


def __print(str, flag=XLSX.DEBUG):
  if flag:
    print(str)
  pass
