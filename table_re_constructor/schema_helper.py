# -*- coding: utf-8 -*-
import sys, enum
from util import Util


class Validator(str, enum.Enum):
  """ 対応validator """
  jsonschema = 'jsonschema'

class TypeSign(str, enum.Enum):
  """ Type adhoc """
  # https://tools.ietf.org/html/draft-zyp-json-schema-04
  # RFC 4627#2.1 https://tools.ietf.org/html/rfc4627
  OBJ = 'object'
  ARRAY = 'array'

  STRING = 'string'
  NUM = 'number'

  FALSE = 'false'
  TRUE = 'true'

  JSON_NULL = 'null'

class Schema:
  """ abstract """
  class JsonSchema:
    """ concrete 1 as jsonschema style """
    def __init__(self):
      self.__schemas = []
    pass

    def _makeSchema(self, type_desc):
      schema = {'type':'object'}
      if 'required' in type_desc[1].keys():
        schema['required'] = [type_desc[0]]
      schema['properties'] = {type_desc[0] : {'type':type_desc[1]['type']}}
      self.__schemas.append(schema)
      return schema

    def _validate(self, evl, schema):
      assert isinstance(evl, list) or isinstance(evl, dict)
      from jsonschema import validate, ValidationError, SchemaError
      # jsonschema による型チェック
      try:
        validate(evl, schema)
      except ValidationError as ve:
        print('Validation Error has found.\n%s'%ve)
        sys.exit(-1)
      except SchemaError as se:
        print('Schema Error has found.\n%s'%se)
        sys.exit(-2)
      pass

  def __init__(self, validator):
    self.schema_name = validator
    # ToDo: type switch
    if validator == Validator.jsonschema:
      self.schema = Schema.JsonSchema()
    pass

  def makeSchema(self, desc):
    """ 一項目ずつの定義であることに留意 """
    # 課題: failfastとして小粒度で都度Errorを上げるか、reduceしたあと最後にvalidationをかけるか
    return self.schema._makeSchema(desc)

  def validate(self, evl, desc):
    sc = self.makeSchema(desc)
    self.schema._validate(evl, sc)
    pass
