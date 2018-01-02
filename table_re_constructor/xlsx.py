# -*- coding: utf-8 -*-
# this made for python3
import os, sys
import csv, openpyxl
from table_reconstructor import TableReConstructor, errorout
from schema_helper import Schema, TypeSign, Validator
from util import Util

class XLSX:
  """ """
  DEBUG = True
  # childへのリンクを示す接頭辞
  sheet_link_sign = 'sheet://'

  def __init__(self, file, output_path, forms=None):
    print(file)
    self.filepath = file
    self.filename = os.path.basename(file)
    self.output_path = output_path
    self.format = forms
    self.book = openpyxl.load_workbook(self.filepath, keep_vba=True, data_only=False)
    pass

  def generateJSON(self, sheet_name, acc=[]):
    """
    sheet_nameが指すsheetのJSONをaccに追加する
    """
    dest_dir = self.output_path
    os.makedirs(dest_dir, exist_ok=True)
    sheets = self.__nameToSheets()
    sheet_names = list(sheets.keys())
    print(f'in process {sheet_name} ')
    assert sheet_name in sheet_names
    root_sheet = sheets[sheet_name]
    columns = []
    print('I\'ll update %s'%acc)
    for i, row in enumerate(root_sheet.iter_rows()):
      subacc = {}
      if self.format:
        self.__outputCSV(dest_dir, root_sheet)
        pass
      for j, cell in enumerate(row):
        v = cell.value
        if v is None: continue # cell check
        if i == 0: # column check
          # cell.commentは必ずつくが、中身がない場合はNone
          if hasattr(cell, "comment") and cell.comment:
            # column 準備 / schemaは遅延せずこの時点で辞書として成立している事を保証
            columns.append((v, Util.runtimeDictionary(cell.comment.text)))
          else:
            self.errorout(2, 'sheet = {}, col = {}, row = {}'.format(sheet_name, j, i))
        else:
          # ToDo: 関数へ置き換え type = array, objectのケース をカバー
          if isinstance(v, str) and v.startswith(XLSX.sheet_link_sign):
            link = v.lstrip(XLSX.sheet_link_sign)
            if link in sheet_names:
              col_name = columns[j][0]
              print(f'process {col_name} -> {link}')
              print(f'current acc = {acc}')
              new_acc = self.__generateNewAccumlatorForType(columns[j][1])
              self.__store({col_name:self.generateJSON(sheet_name=link, acc=new_acc)}, subacc)
            else:
              self.errorout(1, f'sheet = from {sheet_name} to {link}, col = {j}, row = {i}')
              pass
          else:
            self.__store(self.typeValidator(v, columns[j]), accumrator=subacc)
        pass # pass columns
      Util.checkEmptyOr(lambda x: self.__store(x, acc), subacc)
      pass # pass a row
    return acc

  def __getType(self, schema):
    assert 'type' in schema.keys()
    return schema['type']

  def __generateNewAccumlatorForType(self, schema):
    assert isinstance(schema, dict)
    _type = self.__getType(schema)
    if _type == TypeSign.ARRAY:
      return []
    elif _type == TypeSign.OBJ:
      return {}
    else:
      errorout(4, _type)

  def __store(self, item, accumrator):
    if isinstance(accumrator, dict):
      accumrator.update(item)
    elif isinstance(accumrator, list):
      accumrator.append(item)
    else:
      errorout(5)
    return accumrator

  def __outputCSV(self, base_path, sheet, enc='utf-8'):
    """
    CSV, TSV出力
    """
    assert self.format in TableReConstructor.output_formats
    xdest = os.path.join(base_path, self.filename)
    os.makedirs(xdest, exist_ok=True)
    xdest_path = os.path.join(xdest, sheet.title + '.' + self.format)
    print(" > %s"%xdest_path)
    with open(xdest_path, 'w', encoding=enc) as f:
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

  def typeValidator(self, value, type_desc, validator=Validator.jsonschema):
    """ Validator switch """
    if not hasattr(self, '__schema'):
      self.__schema = Schema(validator)
    raw = Util.convEscapedKV(self.__getType(type_desc[1]), type_desc[0], value)
    instance = Util.runtimeDictionary('{%s}'%raw)
    self.__schema.validate(instance, type_desc)
    assert instance is not None
    return instance

def __print(str, flag=XLSX.DEBUG):
  if flag:
    print(str)
  pass
