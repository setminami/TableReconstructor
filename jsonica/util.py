# -*- coding: utf-8 -*-
import re, ast

class Util:
  comment_sign = ['#', '/{2}']

  @classmethod
  def stripComments(cls, rawStr):
    assert isinstance(rawStr, str)
    # ‘/\*/?([^/]|[^*]/)*\*/’ Ctype
    return re.sub(r'\n*[%s].*\n'%''.join(cls.comment_sign), '', rawStr.strip())

  @classmethod
  def __checkValidDictionary(cls, raw_value):
    """ このmodule で固有の読み替え問題を解決 """
    local = cls.stripComments(raw_value)
    local = cls.__convPyBoolean(local)
    # print('>>> %s'%local)
    # ToDo: 真面目な構文チェック
    if not (local.startswith('{') and local.endswith('}')):
      asDic = '{%s}'%local
    else:
      asDic = local
    return asDic

  @classmethod
  def runtimeDictionary(cls, rawStr):
    asDic = cls.__checkValidDictionary(rawStr)
    return ast.literal_eval(asDic)

  @classmethod
  def __convPyBoolean(cls, v):
    tr = re.compile(r'true', re.IGNORECASE)
    fr = re.compile(r'false', re.IGNORECASE)
    local = re.sub(tr, 'True', v)
    return re.sub(fr, 'False', local)

  @classmethod
  def convEscapedKV(cls, type, key, value, enc='utf-8'):
    from schema_helper import TypeSign
    key = key.encode('unicode-escape').decode(enc)
    value = value.encode('unicode-escape').decode(enc)
    value = '{!s}'.format('"%s"'%value if TypeSign.STRING in type else value)
    local = f'"{key}": {value}'
    return local

  @classmethod
  def checkEmptyOr(cls, proc, item):
    """
    itemが空(list, dict, '', None...)なら何もしない、空でなければprocを実行
    """
    if bool(item): proc(item)
