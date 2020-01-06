#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json

from Commons import Logging


class GlobalMap:
    # 拼装成字典构造全局变量  借鉴_map  包含变量的增删改查
    log = Logging.Logs()

    _map = {}

    def set_map(self, key, value):
        if (isinstance(value, dict)):
            # 把dict转为str
            value = json.dumps(value)
        self._map[key] = value

    def set_List(self, key, value):
        if (isinstance(value, list)):
            self._map[key] = value

    def set_value(self, **keys):
        try:
            for key_, value_ in keys.items():
                self._map[key_] = str(value_)
                self.log.debug(key_+":"+str(value_))
        except BaseException as msg:
            self.log.error(msg)
            raise msg

    def set_bool(self, **keys):
        try:
            for key_, value_ in keys.items():
                self._map[key_] = value_
                self.log.debug(key_+":"+str(value_))
        except BaseException as msg:
            self.log.error(msg)
            raise msg


    def del_map(self, key):
        try:
            # 删除变量
            # del语句作用在变量上，而不是数据对象上。
            del self._map[key]
            return self._map
        except KeyError:
            self.log.error("key:'" + str(key) + "'  不存在")

    def get_value(self, *args):
        try:
            dic = {}
            for key in args:
                if len(args) == 1:
                    dic = self._map[key]
                    self.log.debug(key+":"+str(dic))
                elif len(args) == 1 and args[0] == 'all':
                    dic = self._map
                else:
                    dic[key] = self._map[key]
            return dic
        except KeyError:
            self.log.warning("key:'" + str(key) + "'  不存在")
            return 'Null_'


if __name__ == '__main__':
    gm = GlobalMap()
    gm.set_List("accountType", ["bullionMargin"])
    a = gm.get_value("accountType")
    print(a)
    print(gm._map)
