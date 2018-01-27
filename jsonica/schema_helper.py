# -*- coding: utf-8 -*-
import sys, enum
from util import Hoare

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
  """
  抽象的な中継クラス
  下流具象クラスへの中継とreduce以外の作業はさせないこと
  """

  DEBUG = False
  class JsonSchema:
    """ concrete 1 as jsonschema style """
    def __init__(self):
      self.__schemas = []

    def _makeSchema(self, type_desc):
      """
      最小粒度でのjsonschema構築
      """
      schema = {'type':'object'}
      if 'required' in type_desc[1].keys():
        schema['required'] = [type_desc[0]]
      schema['properties'] = {type_desc[0] : {'type':type_desc[1]['type']}}
      self.__schemas.append(schema)
      return schema

    def _validate(self, evl, schema):
      from jsonschema import validate, ValidationError, SchemaError
      # jsonschema による型チェック
      try:
        validate(evl, schema)
      except ValidationError as ve:
        __print('Validation Error has found.\n%s'%ve)
        print('_validate {} with: {}'.format(evl, self.__schemas))
        sys.exit(-1)
      except SchemaError as se:
        __print('Schema Error has found.\n%s'%se)
        print('Error Schema : %s'%self.__schemas)
        sys.exit(-2)

  def __init__(self, validator):
    self.schema_name = validator
    self.schema_collection = []
    # TEMP: type switch
    if validator == Validator.jsonschema:
      self.schema = Schema.JsonSchema()

  def makeSchema(self, desc):
    """ 一項目ずつの定義であることに留意 """
    Hoare.P(isinstance(desc[0], str) and isinstance(desc[1], dict))
    # TEMP: failfastとして小粒度で都度Errorを上げるか、reduceしたあと最後にvalidationをかけるか
    self.schema_collection.append(self.schema._makeSchema(desc))
    return self.schema_collection[-1]

  def validate(self, evl, desc):
    Hoare.P(isinstance(evl, list) or isinstance(evl, dict))
    self.schema._validate(evl, self.makeSchema(desc))
    # print('i\'m {} \nNow I have -> {}'.format(self, self.schema_collection))

def __print(_str, flag=False):
  if flag: print(_str)
