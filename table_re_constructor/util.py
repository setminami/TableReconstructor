# -*- coding: utf-8 -*-

import re, ast

class Util:
  comment_sign = ['#', '/{2}']

  @classmethod
  def stripComments(cls, rawStr):
    # ‘/\*/?([^/]|[^*]/)*\*/’ Ctype
    return re.sub(r'\n*[%s].*\n'%''.join(cls.comment_sign), '', rawStr.strip())

  @classmethod
  def runtimeDictionary(cls, rawStr):
    local = cls.stripComments(rawStr)
    local = cls.convPyBoolean(local)
    if not (local.startswith('{') and local.endswith('}')):
      asDic = '{%s}'%local
    else:
      asDic = local
    print(asDic)
    return ast.literal_eval(asDic)

  @classmethod
  def convPyBoolean(cls, v):
    tr = re.compile(r'true', re.IGNORECASE)
    fr = re.compile(r'false', re.IGNORECASE)
    local = re.sub(tr, 'True', v)
    return re.sub(fr, 'False', local)
