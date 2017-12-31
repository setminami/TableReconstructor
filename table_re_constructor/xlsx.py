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
    self.filename = os.path.basename(file)
    self.output_path = output_path
    self.format = forms
    self.book = openpyxl.load_workbook(self.filepath, keep_vba=True, data_only=False)
    pass

  def generateJSON(self, acc=[], sheet_name=root_name):
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
            # column 準備 / schemeは遅延せずこの時点で辞書として成立している事を保証
            columns.append((v, Util.runtimeDictionary(cell.comment.text)))
          else:
            self.errorout(2, 'sheet = {}, col = {}, row = {}'.format(sheet_name, j, i))
        else:
          if isinstance(v, str) and v.startswith(XLSX.sheet_link_sign):
            link = v.lstrip(XLSX.sheet_link_sign)
            if link in sheet_names:
              col_name = columns[j][0]
              print(f'process {col_name} -> {link}')
              print(f'current acc = {acc}')
              self.__store({col_name:self.generateJSON(acc=[], sheet_name=link)}, subacc)
            else:
              self.errorout(1, 'sheet = from {} to {}, col = {}, row = {}'.format(sheet_name, link, j, i))
              pass
          else:
            self.__store(self.typeValidator(v, columns[j]), accumrator=subacc)
        pass # pass columns
      Util.checkEmptyOr(lambda x: self.__store(x, acc), subacc)
      pass # pass a row
    return acc

  def __store(self, item, accumrator):
    if isinstance(accumrator, dict):
      accumrator.update(item)
    elif isinstance(accumrator, list):
      accumrator.append(item)
    else:
      print('Unknown accumrator!')
      exit(-3)
    return accumrator

  def __outputCSV(self, base_path, sheet):
    """
    CSV, TSV出力
    """
    assert self.format in TableReConstructor.output_formats
    xdest = os.path.join(base_path, self.filename)
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
    __type = type_desc[1]['type']
    # ToDo: type switch
    raw = Util.convEscapedKV(__type, type_desc[0], value)
    # jsonschema による型チェック
    if validator == Validator.jsonschema:
      from jsonschema import validate, ValidationError, SchemaError
      # as jsonschema style
      # 課題: failfastとして小粒度で都度Errorを上げるか、reduceしたあと最後にvalidationをかけるか
      schema = {'type':'object'}
      if 'required' in type_desc[1].keys():
        schema['required'] = [type_desc[0]]
      schema['properties'] = {type_desc[0] : {'type':type_desc[1]['type']}}
      # print('%s < %s : %s >\n%s'%(value, type_desc[0], schema, raw))
      instance = '{%s}'%raw
      try:
        validate(Util.runtimeDictionary(instance), schema)
      except ValidationError as ve:
        print('Validation Error has found.\n%s'%ve)
        exit(-1)
      except SchemaError as se:
        print('Schema Error has found.\n%s'%se)
        exit(-2)
      pass
    assert instance is not None
    return Util.runtimeDictionary(instance)

def __print(str, flag=XLSX.DEBUG):
  if flag:
    print(str)
  pass
