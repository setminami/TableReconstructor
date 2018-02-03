# -*- coding: utf-8 -*-
# this made for python3
import os, csv, openpyxl
from jsonica import errorout, PROGNAME
from schema_helper import Schema, TypeSign, Validator
from sub_command_core.generate import output_formats
from util import Util, Hoare

class XLSX:
  """ xlsx 具象操作クラス """
  DEBUG = not (os.getenv('TRAVIS', False))
  # childへのリンクを示す接頭辞
  sheet_link_sign = 'sheet://'
  @property
  def schema(self): return self.__schema
  @schema.setter
  def schema(self, value):
    if not hasattr(self, '__schema'):
      self.__schema = value

  @property
  def piled_schema(self):
    """
    __all_schema: {sheet: [schemas]}
    """
    return self.__all_schema
  @piled_schema.setter
  def piled_schema(self, value):
    """ value : (sheet:Some, schema:dict) """
    if value[0] in self.piled_schema.keys():
      self.piled_schema[value[0]].update(value[1])
    else:
      self.piled_schema[value[0]] = value[1]

  def __init__(self, file, enc, forms=None):
    self.filepath = file
    self.filename = os.path.basename(file)
    self.__all_schema = {}
    if forms:
      self.format = forms[0]
      self.format_delimiter = forms[1]
      self.format_output = forms[2]
    self.char_encode = enc
    if forms: # generate
      self.book = openpyxl.load_workbook(self.filepath, keep_vba=True, data_only=False)
    else: # init
      self.book = openpyxl.Workbook()

  def generateJSON(self, sheet_name, acc=None):
    """
    sheet_nameが指すsheetのJSONをaccに追加する
    """
    sheets = self.__nameToSheets()
    # pyxl...Workbookで[sheet名]を持っているが、あまり高速処理向けではないため
    sheet_names = list(sheets.keys())
    Util.sprint('in process %s'%sheet_name, self.DEBUG)
    Hoare.P(sheet_name in sheet_names, '"%s" not found in %s'%(sheet_name ,sheet_names))
    root_sheet = sheets[sheet_name]
    self.checkCharEncode(root_sheet)
    columns = []
    acc = [] if not acc else acc
    Util.sprint('I\'ll update {}'.format(acc), self.DEBUG)
    # COMBAK: 処理速度に問題が出るようであれば分散処理検討
    # A1, B1...で場所を特定するか、indexで回すか
    for i, row in enumerate(root_sheet.iter_rows()):
      subacc = {}
      if self.format:
        self.__outputCSV(self.format_output, root_sheet, self.char_encode)
      for j, cell in enumerate(row):
        v = cell.value # off-by-oneを気にしないといけなくなるので、col_idxではなくenumerate使う
        if v is None: continue # cell check
        if i == 0: # 初行 column check
          # cell.commentは必ずつくが、中身がない場合はNone
          if hasattr(cell, "comment") and cell.comment:
            # column 準備 / schemaは遅延せずこの時点で辞書として成立している事を保証
            columns.append((v, Util.runtimeDictionary(cell.comment.text)))
          else:
            self.errorout(2, 'sheet = {}, col = {}, row = {}'.format(sheet_name, j, i))
        else:
          # TODO: 関数へ置き換え type = array, objectのケース をカバー
          if isinstance(v, str) and v.startswith(XLSX.sheet_link_sign):
            # COMBAK: sheetであることがarray, objectの必要条件になってしまっている
            # primitive配列をどう表現するかによって改修が必要 __storeに包含させる？
            link = v.lstrip(XLSX.sheet_link_sign)
            if link in sheet_names:
              col_name = columns[j][0]
              Util.sprint('process %s -> %s'%(col_name, link), self.DEBUG)
              Util.sprint('current acc = %s'%acc, self.DEBUG)
              new_acc = XLSX.__brandnewAccForType(columns[j][1])
              # recursive seed
              XLSX.__store({col_name:self.generateJSON(sheet_name=link, acc=new_acc)}, subacc)
            else:
              errorout(1, 'sheet = from %s to %s, col = %d, row = %d'%(sheet_name, link, j, i))
          else:
            XLSX.__store(self.typeValidator(sheet_name, v, columns[j]), subacc)
        # pass columns
      Util.checkEmptyOr(lambda x: XLSX.__store(x, acc), subacc)
      # pass a row
    return acc

  def __outputCSV(self, base_path, sheet, enc):
    """
    CSV, TSV出力
    """
    if not self.format: return
    Hoare.P(self.format in output_formats)
    xdest = os.path.join(base_path, self.filename)
    os.makedirs(xdest, exist_ok=True)
    xdest_path = os.path.join(xdest, '%s.%s'%(sheet.title ,self.format))
    Util.sprint(' > %s'%xdest_path, self.DEBUG)
    with open(xdest_path, 'w', encoding=enc) as f:
      writer = csv.writer(f, delimiter=self.format_delimiter)
      for cols in sheet.rows:
        writer.writerow([str(col.value or '') for col in cols])

  def __nameToSheets(self):
    """
    sheetを{sheet名:sheet}形式にして返す
    instance 生成後、実行中のExcel更新は考えない
    """
    # TODO: pyxl.get_sheet_names(), get_sheet_by_name()で代用できるか検討
    if not hasattr(self, '__sheets_cache'):
      self.__sheets_cache = {s.title: s for s in self.book.worksheets}
    return self.__sheets_cache

  def checkCharEncode(self, item, valid_enc=None):
    Hoare.P(isinstance(item, openpyxl.workbook.workbook.Workbook) or \
            isinstance(item, openpyxl.worksheet.Worksheet) or \
            isinstance(item, openpyxl.cell.Cell))
    enc = valid_enc if bool(valid_enc) else self.char_encode
    Util.sprint(enc, self.DEBUG)
    if not (item.encoding == enc):
      # TODO: sheet, cellごとにエラーを上げる場合の処理
      if isinstance(item, openpyxl.workbook.workbook.Workbook):
        add = 'sheet_names = %s'%item.sheet_names
      elif isinstance(item, openpyxl.worksheet.Worksheet):
        add = 'sheet_name = %s'%item.title
      else: # Cell
        add = 'parent = {} index = {}'.format(item.parent ,item.cordinate)
      print('*'*50)
      print(add)
      print('*'*50)
      # TODO: excel rw 状態チェック
      item.encoding = enc

  def typeValidator(self, sheet_name, value, type_desc, validator=Validator.jsonschema):
    """ Validator switcher """
    self.schema = Schema(validator)
    raw = Util.convEscapedKV(XLSX.__getType(type_desc[1]), type_desc[0], value)
    instance = Util.runtimeDictionary('{%s}'%raw)
    Util.sprint('i\'m %s. call validator'%self, self.DEBUG)
    Util.sprint('== %s : %s =='%(sheet_name, {type_desc[0]:type_desc[1]}), self.DEBUG)
    self.piled_schema = (sheet_name, {type_desc[0]:type_desc[1]})
    self.schema.validate(instance, type_desc)
    Hoare.P(instance is not None)
    return instance

  def generateSheet(self, name):
    return self.book.create_sheet(name)

  def putCommentToCell(self, cell, text, author=PROGNAME):
    from openpyxl.comments import Comment
    cell.comment = Comment(text, author)

  @classmethod
  def __getType(cls, schema):
    Hoare.P('type' in schema.keys())
    return schema['type']

  @classmethod
  def __brandnewAccForType(cls, schema):
    Hoare.P(isinstance(schema, dict))
    _type = XLSX.__getType(schema)
    if _type == TypeSign.ARRAY:
      return []
    elif _type == TypeSign.OBJ:
      return {}
    else:
      errorout(4, _type)

  @classmethod
  def __store(cls, item, accumulator):
    if isinstance(accumulator, dict):
      accumulator.update(item)
    elif isinstance(accumulator, list):
      accumulator.append(item)
    else:
      errorout(5)
    return accumulator
