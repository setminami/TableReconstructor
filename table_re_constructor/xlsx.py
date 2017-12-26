# -*- coding: utf-8 -*-
# this made for python3
import os
import csv, openpyxl
from openpyxl.worksheet.hyperlink import Hyperlink
from table_reconstructor import TableReConstructor

class XLSX:
  """ """
  DEBUG = True
  sheet_link_sign = 'sheet://'
  root_name = 'root'

  def __init__(self, file, output_path, forms=None):
      print(file)
      self.filepath = file
      self.output_path = output_path
      self.format = forms
      self.book = openpyxl.load_workbook(self.filepath, keep_vba=False)
      pass

  def generateCSVs(self):
    dest_dir = self.output_path
    print(dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    sheets = self.__nameToSheets()
    sheet_names = list(sheets.keys())
    assert XLSX.root_name in sheet_names
    root_sheet = sheets[XLSX.root_name]
    for row in root_sheet.iter_rows():
      if self.format:
        self.__outputCSV(dest_dir, root_sheet)
        pass
      for cell in row:
        v = cell.value
        print(v)
        if isinstance(v, str) and v.startswith(XLSX.sheet_link_sign):
          link = v.lstrip(XLSX.sheet_link_sign)
          if link in sheet_names:
            self.__outputCSV(dest_dir, sheets[link])
          else:
            self.errorout(1)
          pass
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
    実行中のExcel更新は考えない
    """
    if not hasattr(self, '__sheets_cache'):
      self.__sheets_cache = {s.title: s for s in self.book.worksheets}
    return self.__sheets_cache

  def errorout(self, e):
    """ 出力細部はあとで調整すること """
    errors = ['OK', 'sheets link not found.']
    assert e < len(errors)
    print(errors[e])

def __print(str, flag=XLSX.DEBUG):
  if flag:
    print(str)
  pass
