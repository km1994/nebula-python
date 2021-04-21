#!/usr/bin/env python
# --coding:utf-8--

# Copyright (c) 2020 vesoft inc. All rights reserved.
#
# This source code is licensed under Apache 2.0 License,
# attached with Common Clause Condition 1.0, found in the LICENSES directory.

import sys
import os
import time


current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..')
sys.path.insert(0, root_dir)

from nebula2.Config import Config
from nebula2.common.ttypes import (
    DateTime,
    Date,
    Time
)

from nebula2.graph import ttypes
from nebula2.data.DataObject import (
    DateTimeWrapper,
    DateWrapper,
    TimeWrapper,
    Null
)

from nebula2.gclient.net import ConnectionPool

from unittest import TestCase


class TestBaseCase(TestCase):
    pool = None
    session = None
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        configs = Config()
        configs.max_connection_pool_size = 1
        cls.pool = ConnectionPool()
        cls.pool.init([('127.0.0.1', 9671)], configs)
        cls.session = cls.pool.get_session('root', 'nebula')
        resp = cls.session.execute(
            '''
            CREATE SPACE IF NOT EXISTS test_data; 
            USE test_data;
            CREATE TAG IF NOT EXISTS person(name string, age int8, grade int16, 
            friends int32, book_num int64, birthday datetime, 
            start_school date, morning time, property double, 
            is_girl bool, child_name fixed_string(10), expend float, 
            first_out_city timestamp, hobby string);
            CREATE TAG IF NOT EXISTS student(name string);
            CREATE EDGE IF NOT EXISTS like(likeness double);
            CREATE EDGE IF NOT EXISTS friend(start_year int, end_year int);
            CREATE TAG INDEX IF NOT EXISTS person_name_index ON person(name(8));
            '''
        )
        assert resp.is_succeeded(), resp.error_msg()

        time.sleep(5)
        resp = cls.session.execute(
            "INSERT VERTEX person(name, age, grade,friends, book_num,"
            "birthday, start_school, morning, property,"
            "is_girl, child_name, expend, first_out_city) VALUES"
            "'Bob':('Bob', 10, 3, 10, 100, datetime('2010-09-10T10:08:02'),"
            "date('2017-09-10'), time('07:10:00'), "
            "1000.0, false, 'Hello World!', 100.0, 1111)," 
            "'Lily':('Lily', 9, 3, 10, 100, datetime('2010-09-10T10:08:02'), "
            "date('2017-09-10'), time('07:10:00'), "
            "1000.0, false, 'Hello World!', 100.0, 1111)," 
            "'Tom':('Tom', 10, 3, 10, 100, datetime('2010-09-10T10:08:02'), "
            "date('2017-09-10'), time('07:10:00'), "
            "1000.0, false, 'Hello World!', 100.0, 1111)," 
            "'Jerry':('Jerry', 9, 3, 10, 100, datetime('2010-09-10T10:08:02')," 
            "date('2017-09-10'), time('07:10:00'), "
            "1000.0, false, 'Hello World!', 100.0, 1111), "
            "'John':('John', 10, 3, 10, 100, datetime('2010-09-10T10:08:02'), "
            "date('2017-09-10'), time('07:10:00'), "
            "1000.0, false, 'Hello World!', 100.0, 1111)"
        )
        assert resp.is_succeeded(), resp.error_msg()
        resp = cls.session.execute(
            "INSERT VERTEX student(name) VALUES "
            "'Bob':('Bob'), 'Lily':('Lily'), "
            "'Tom':('Tom'), 'Jerry':('Jerry'), 'John':('John')")
        assert resp.is_succeeded(), resp.error_msg()

        resp = cls.session.execute(
            "INSERT EDGE like(likeness) VALUES "
            "'Bob'->'Lily':(80.0), "
            "'Bob'->'Tom':(70.0), "
            "'Jerry'->'Lily':(84.0)," 
            "'Tom'->'Jerry':(68.3), "
            "'Bob'->'John':(97.2)")
        assert resp.is_succeeded(), resp.error_msg()
        resp = cls.session.execute(
            "INSERT EDGE friend(start_year, end_year) VALUES "
            "'Bob'->'Lily':(2018, 2020), "
            "'Bob'->'Tom':(2018, 2020), "
            "'Jerry'->'Lily':(2018, 2020)," 
            "'Tom'->'Jerry':(2018, 2020), "
            "'Bob'->'John':(2018, 2020)")
        assert resp.is_succeeded(), resp.error_msg()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.session is None:
            cls.session.release()
        if cls.pool is None:
            cls.pool.close()

    def test_base_type(self):
        resp = self.session.execute('FETCH PROP ON person "Bob" YIELD person.name, person.age, person.grade,'
                                    'person.friends, person.book_num, person.birthday, person.start_school, person.morning, '
                                    'person.property, person.is_girl, person.child_name, person.expend, person.first_out_city, person.hobby')
        assert resp.is_succeeded(), resp.error_msg()
        assert '' == resp.error_msg()
        assert resp.latency() > 0
        assert '' == resp.comment()
        assert ttypes.ErrorCode.SUCCEEDED == resp.error_code()
        assert 'test_data' == resp.space_name()
        assert not resp.is_empty()
        assert 1 == resp.row_size()
        names = ['VertexID',
                 'person.name',
                 'person.age',
                 'person.grade',
                 'person.friends',
                 'person.book_num',
                 'person.birthday',
                 'person.start_school',
                 'person.morning',
                 'person.property',
                 'person.is_girl',
                 'person.child_name',
                 'person.expend',
                 'person.first_out_city',
                 'person.hobby']
        assert names == resp.keys()

        assert 'Bob' == resp.row_values(0)[0].as_string()
        assert 'Bob' == resp.row_values(0)[1].as_string()
        assert 10 == resp.row_values(0)[2].as_int()
        assert 3 == resp.row_values(0)[3].as_int()
        assert 10 == resp.row_values(0)[4].as_int()
        assert 100 == resp.row_values(0)[5].as_int()
        assert resp.row_values(0)[6].as_datetime() == \
               DateTimeWrapper(DateTime(2010, 9, 10, 10, 8, 2, 0))

        assert DateWrapper(Date(2017, 9, 10)) == resp.row_values(0)[7].as_date()

        assert TimeWrapper(Time(7, 10, 0, 0)) == resp.row_values(0)[8].as_time()

        assert 1000.0 == resp.row_values(0)[9].as_double()
        assert False == resp.row_values(0)[10].as_bool()
        assert 'Hello Worl' == resp.row_values(0)[11].as_string()
        assert 100.0 == resp.row_values(0)[12].as_double()
        assert 1111 == resp.row_values(0)[13].as_int()
        assert Null(Null.__NULL__) == resp.row_values(0)[14].as_null()

    def test_list_type(self):
        resp = self.session.execute("YIELD ['name', 'age', 'birthday'];")
        assert resp.is_succeeded()
        assert 1 == resp.row_size()
        result = [name.as_string() for name in resp.row_values(0)[0].as_list()]
        assert ["name", "age", "birthday"] == result

    def test_set_type(self):
        resp = self.session.execute("YIELD {'name', 'name', 'age', 'birthday'};")
        assert resp.is_succeeded()
        assert 1 == resp.row_size()
        assert resp.row_values(0)[0].is_set()
        result = [name.as_string() for name in resp.row_values(0)[0].as_set()]
        assert sorted(["name", "age", "birthday"]) == sorted(result)

    def test_map_type(self):
        resp = self.session.execute("YIELD {name:'Tom', age:18, birthday: '2010-10-10'};")
        assert resp.is_succeeded()
        assert 1 == resp.row_size()
        assert resp.row_values(0)[0].is_map()
        val = resp.row_values(0)[0].as_map()
        assert len(val.keys()) == 3
        assert 'name' in val.keys()
        assert val['name'].as_string() == 'Tom'
        assert 'age' in val.keys()
        assert val['age'].as_int() == 18
        assert 'birthday' in val.keys()
        assert val['birthday'].as_string() == '2010-10-10'

    def test_node_type(self):
        resp = self.session.execute('MATCH (v:person {name: "Bob"}) RETURN v')
        assert resp.is_succeeded()
        assert 1 == resp.row_size()
        assert resp.row_values(0)[0].as_node()

    def test_relationship_type(self):
        resp = self.session.execute(
            'MATCH (:person{name: "Bob"}) -[e:friend]-> (:person{name: "Lily"}) RETURN e')
        assert resp.is_succeeded()
        assert 1 == resp.row_size()
        assert resp.row_values(0)[0].is_edge()
        rel = resp.row_values(0)[0].as_relationship()

        assert '("Bob")-[:friend@0{end_year: 2020, start_year: 2018}]->("Lily")' == str(rel)

    def test_path_type(self):
        resp = self.session.execute(
            'MATCH p = (:person{name: "Bob"})-[:friend]->(:person{name: "Lily"}) return p')
        assert resp.is_succeeded()
        assert 1 == resp.row_size()
        assert resp.row_values(0)[0].is_path()
        path = resp.row_values(0)[0].as_path()
        expected_str = '("Bob" :student{name: "Bob"} ' \
                       ':person{hobby: __NULL__, expend: 100.0, book_num: 100, ' \
                       'property: 1000.0, grade: 3, child_name: "Hello Worl", ' \
                       'start_school: 2017-09-10, friends: 10, ' \
                       'morning: 07:10:00.000000, first_out_city: 1111, ' \
                       'name: "Bob", age: 10, birthday: 2010-09-10T10:08:02.000000, is_girl: False})' \
                       '-[:friend@0{end_year: 2020, start_year: 2018}]->' \
                       '("Lily" :student{name: "Lily"} ' \
                       ':person{is_girl: False, birthday: 2010-09-10T10:08:02.000000, age: 9, ' \
                       'book_num: 100, grade: 3, property: 1000.0, hobby: __NULL__, expend: 100.0, ' \
                       'start_school: 2017-09-10, child_name: "Hello Worl", morning: 07:10:00.000000, ' \
                       'friends: 10, first_out_city: 1111, name: "Lily"})'
        assert expected_str == str(path)

        assert resp.whole_latency() > 100


