# -*- coding: utf-8 -*-
import re, ast

class Util:
  comment_sign = ['#', '/{2}']

  @classmethod
  def strip_comments(cls, rawStr):
    Hoare.P(isinstance(rawStr, str))
    # ‘/\*/?([^/]|[^*]/)*\*/’ Ctype
    return re.sub(r'\n*[%s].*\n'%''.join(cls.comment_sign), '', rawStr.strip())

  @classmethod
  def __validate_dict(cls, raw_value):
    """ このmodule で固有の読み替え問題を解決 """
    local = cls.strip_comments(raw_value)
    local = cls.__conv_pyBoolean(local)
    # print('>>> %s'%local)
    # TEMP: 真面目な構文チェック
    if not (local.startswith('{') and local.endswith('}')):
      asDic = '{%s}'%local
    else:
      asDic = local
    return asDic

  @classmethod
  def runtime_type(cls, rawStr):
    """ 連想配列を文字列で受けて、評価済みの型で返す """
    asDic = cls.__validate_dict(rawStr)
    return ast.literal_eval(asDic)

  @classmethod
  def __conv_pyBoolean(cls, v):
    tr = re.compile(r'true', re.IGNORECASE)
    fr = re.compile(r'false', re.IGNORECASE)
    local = re.sub(tr, 'True', v)
    return re.sub(fr, 'False', local)

  @classmethod
  def conv_escapedKV(cls, _type, key, value, enc='utf-8'):
    from schema_helper import TypeSign
    key = key.encode('unicode-escape').decode(enc)
    value = value.encode('unicode-escape').decode(enc)
    value = '{!s}'.format('"%s"'%value if TypeSign.STRING in _type else value)
    local = '"{}": {}'.format(key, value)
    return local

  @classmethod
  def check_emptyOR(cls, proc, item):
    """

    :param proc: lambda x: ... or function 引数をひとつ持つ関数

    :param item: 空 (list|dict|str) | None なら何もしない、空でなければprocを実行

    :returns procが返値を持つ場合は、procに従う
    """
    if bool(item): proc(item)

  @classmethod
  def sprint(cls, msg, flag=False):
    """
    | class, f単位で出力制御設定するためのシンプルなDEBUG出力関数
    | NOTE: Util\.sprint\(.+,\s*True\s*\) が見つかったらprintに書き換える

    :param msg: 表示文字列

    :param flag: 表示制御flag
    """
#    if flag:
#      import inspect
#      stack = inspect.stack()
#      the_class = stack[1][0].f_locals["self"].__class__.__name__
#      print('*** %s ***'%str(the_class))
#      # COMBAK: 効率化するならthe_class単位でloggerを切り替える
#      from logging import getLogger, StreamHandler, DEBUG
#      # https://docs.python.jp/3/library/logging.html#logger-objects
#      logger = getLogger(str(the_class))
#      handler = StreamHandler()
#      handler.setLevel(DEBUG)
#      logger.setLevel(DEBUG)
#      logger.addHandler(handler)
#      # https://docs.python.jp/3/library/logging.html#logging.Logger.propagate
#      logger.propagate = False
#      logger.debug(msg)
    if flag: print(msg)

# Why Pythonista hates 'assert' a great function?
# Meybe it is NOT a primary func. or want to use tests forcely.
class Hoare:
  @classmethod
  def P(cls, *formula):
    comment = lambda x: x[1] if len(x) > 1 else ''
    if __debug__:
      if not formula[0]:
        print('%s'%comment(formula))
        raise AssertionError()
    else:
      if not formula[0]:
        print('Not correct condition has found. [%s]'%comment(formula))
