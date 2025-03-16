**Пример-1**

```py
def replace_alarm_groups_id(incidents_groups: dict, current_max_id: int):
    incidents_groups_upd = {}
    max_id = current_max_id + 1
    for v in incidents_groups.values():
        incidents_groups_upd[max_id] = v
        max_id += 1
    return incidents_groups_upd
```


Напишем unit-тесты для функции в соответствии с предложенной методологией из СильныхИдей:


```py
import unittest


class TestReplaceAlarmGroupsId(unittest.TestCase):
    def test_positive_current_max_id(self):
        incidents_groups = {
            'group1': 'incident1',
            'group2': 'incident2',
            'group3': 'incident3'
        }
        expected_result = {
            101: 'incident1',
            102: 'incident2',
            103: 'incident3'
        }
        current_max_id = 100
        result = replace_alarm_groups_id(incidents_groups, current_max_id)
        self.assertEqual(result, expected_result)

    def test_with_empty_incidents_groups(self):
        incidents_groups = {}
        expected_result = {}
        current_max_id = 100
        result = replace_alarm_groups_id(incidents_groups, current_max_id)
        self.assertEqual(result, expected_result)

    def test_single_group(self):
        incidents_groups = {'group1': 'incident1'}
        current_max_id = 100
        expected_result = {101: 'incident1'}
        result = replace_alarm_groups_id(incidents_groups, current_max_id)
        self.assertEqual(result, expected_result)

    def test_with_negative_current_max_id(self):
        incidents_groups = {'group1': 'incident1'}
        current_max_id = -5
        expected_result = {101: 'incident1'}
        with self.assertRaises(AssertionError):
            self.assertEqual(result, incorrect_expected_result)
```

Благодаря тесту удалось обнаружить потенциальный баг для случае, если id является отрицательным, а это значит, что нужно добавить соответствующую проверку.

Благодаря такому подходу можно буквально тестировать каждый функциональную единицу (грубо говоря, каждый блок кода, где происходят какие-либо манипуляции) и
по сути двигаться по коду "построчно".



**Пример-2**

```py
def exclude_incidents_connection_by_time(incident_edges: list, df_incidents: pd.DataFrame, thr_seconds: int):
    """
    Исключаем потенциальную взаимосвязь между инцидентами, для которых
    разница во времени больше заданного порога
    """
    incident_edges_upd = []
    for pn, cn, lenght in incident_edges:
        pn_incident_time = df_incidents[df_incidents["entityId"] == pn]["timestamp"].tolist()[0]
        cn_incident_time = df_incidents[df_incidents["entityId"] == cn]["timestamp"].tolist()[0]
        time_diff = max(pn_incident_time, cn_incident_time) - min(pn_incident_time, cn_incident_time)
        if time_diff.seconds <= thr_seconds:
            incident_edges_upd.append((pn, cn, lenght))
    return incident_edges_upd
```

Напишем unit-тесты для функции в соответствии с предложенной методологией из СильныхИдей:


```py
import unittest
import pandas as pd
from datetime import datetime, timedelta


class TestExcludeIncidentsConnectionByTime(unittest.TestCase):

    def setUp(self):
        data = {
            'entityId': ['incident_1', 'incident_2', 'incident_3'],
            'timestamp': [
                datetime(2025, 3, 16, 8, 0),
                datetime(2025, 3, 16, 8, 5),
                datetime(2025, 3, 16, 9, 0),
            ]
        }
        self.df_incidents = pd.DataFrame(data)

    def test_no_exclusion_when_within_threshold(self):
        incident_edges = [
            ('incident_1', 'incident_2', 10),
            ('incident_1', 'incident_3', 15)
        ]
        result = exclude_incidents_connection_by_time(incident_edges, self.df_incidents, 600)
        self.assertEqual(result, [('incident_1', 'incident_2', 10)])

    def test_exclusion_when_exceeds_threshold(self):
        incident_edges = [
            ('incident_1', 'incident_2', 10),
            ('incident_2', 'incident_3', 15)
        ]
        result = exclude_incidents_connection_by_time(incident_edges, self.df_incidents, 600)
        self.assertEqual(result, [('incident_1', 'incident_2', 10)])

    def test_empty_incident_edges(self):
        incident_edges = []
        result = exclude_incidents_connection_by_time(incident_edges, self.df_incidents, 600)
        self.assertEqual(result, [])

    def test_no_edges_within_threshold(self):
        incident_edges = [
            ('incident_1', 'incident_3', 10),
            ('incident_2', 'incident_3', 20)
        ]
        result = exclude_incidents_connection_by_time(incident_edges, self.df_incidents, 600)
        self.assertEqual(result, [])

    def test_time_difference_equals_threshold(self):
        incident_edges = [
            ('incident_1', 'incident_2', 10)
        ]
        result = exclude_incidents_connection_by_time(incident_edges, self.df_incidents, 600)
        self.assertEqual(result, [('incident_1', 'incident_2', 10)])
```

Проработка теста уже сообщила о том, что функция явно плохо спроектирована и требует рефакторинга.



**Обратите внимание на этапы вашего реального рабочего процесса, как часто вы комитите код?**

На практике довольно редко делаю комиты кода, т.к. большая часть написанного кода корректируется в процессе уточнения требований, а для небольших проектов чаще всего весь код пишется за короткий срок, поэтому делаю коммиты разом.


**Что из вышеописанной практики вы сможете применить в своей "настоящей" работе?**

Мне очень понравилась практика "пошаговых" тестов, потому что в таком случае можно крайне быстро либо найти изъяны в логике программы, а также быть более уверенным в полученных реализациях.
Эту практику я бы мог применять в работе.


