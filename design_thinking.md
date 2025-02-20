Основные проблемы, с которыми я столкнулся:

Трудно проектировать системы в области анализа данных и машинного обучения, т.к. там очень много компонентов, которые могут изменяться, а также огромную роль играет бизнес-логика.
Соответственно, при даже незначительных изменениях в бизнес-логике могут потребоваться существенные изменения в системе.
В целом, я понимаю, что это означает провал дизайна, но пока что трудно при реализации не фокусироваться на имеющихся данных, т.к. они всё решают.
Как следствие вышесказанного, довольно трудно проектировать тесты в соответствии с TDD, т.к. не удаётся абстрагироваться от конкретики данных.
После изучения материалов у меня сложилось впечатление, что методология BDD может быть крайне полезной именно с привязкой в проектам в области анализа данных, т.к. помогает более чётко определить спецификацию проекта именно с точки зрения бизнеса.

В связи с этим мне не удалось полноценно спроектировать систему (по правде говоря, я даже не особо понимаю, как к этому вообще лучше подходить, если мы не фокусируемся на конкретной реализации), поэтому в рамках реализации по TDD я ограничился некоторыми функциональными аспектами проекта, не вдаваясь в глубокую абстракцию.

Тест в соответствии с TDD:

```py
class TestGetCoreCampaignPrePeriodsFunction(unittest.TestCase):
    def test_get_core_campaigns_pre_periods(self):
        camp_date_1 = dt.datetime(2024, 1, 1)
        camp_date_2 = dt.datetime(2024, 2, 29)
        camp_date_3 = dt.datetime(2024, 6, 10)

        result_camp_date_1 = [dt.datetime(2023, 11, 1), dt.datetime(2023, 12, 1), dt.datetime(2024, 1, 1)]
        result_camp_date_2 = [dt.datetime(2024, 2, 1), dt.datetime(2024, 1, 1), dt.datetime(2023, 12, 1)]
        result_camp_date_3 = [dt.datetime(2024, 6, 1), dt.datetime(2024, 5, 1), dt.datetime(2024, 4, 1)]

        self.assertCountEqual(cbl.get_core_campaign_pre_periods(camp_date_1), result_camp_date_1)
        self.assertCountEqual(cbl.get_core_campaign_pre_periods(camp_date_2), result_camp_date_2)
        self.assertCountEqual(cbl.get_core_campaign_pre_periods(camp_date_3), result_camp_date_3)
```

Реализация:

```py
def get_core_campaign_pre_periods(camp_date: dt.datetime) -> list:
    pre_periods = []
    for n_months_ago in range(3):
        pre_periods.append(camp_date - relativedelta(months=n_months_ago))
    return pre_periods
```
В целом, так как эта функция представляет собой минимальный блок дизайна программы, то для этого примера можно сказать, что тесты и код следуют дизайну.

Другие реализации являются похожими, и представляют собой примеры тестирования минимальных блоков дизайна системы.
Есть пример дизайна валидация некоторого набора данных:

```py
class TestCoreCampsReportValidator(unittest.TestCase):

    def SetUp(self):
        self.df_1 = pd.DataFrame(
            data={
                "CAMP_ID": [1, 2, 3, 4, 5],
                "CAMP_TYPE": ["UPGRADE_TARIFF", "UPGRADE_TARIFF", "VAS", "CHURN", "CHURN"],
            }
        )
        self.df_2 = pd.DataFrame(
            data={
                "CAMP_ID": [1, 2, 1, 4, 5],
                "CAMP_TYPE": ["UPGRADE_TARIFF", "UPGRADE_TARIFF", "VAS", "CHURN", "CHURN"],
            }
        )
        self.df_3 = pd.DataFrame(
            data={
                "CAMP_ID": [1, 2, 3, 4, 5],
                "CAMP_TYPE": ["UPGRADE_TARIFF", "NEW_TYPE", "VAS", "CHURN", "CHURN"],
            }
        )
        self.core_camps_report_validator_1 = crv.CoreCampsReportValidator(self.df_1)
        self.core_camps_report_validator_2 = crv.CoreCampsReportValidator(self.df_2)
        self.core_camps_report_validator_3 = crv.CoreCampsReportValidator(self.df_3)
    
    def test_are_all_unique_camps(self):
        self.assertTrue(self.core_camps_report_validator_1._are_all_unique_camps())
        self.assertFalse(self.core_camps_report_validator_2._are_all_unique_camps())
        self.assertTrue(self.core_camps_report_validator_3._are_all_unique_camps())

    def test_are_all_available_camp_types(self):
        self.assertTrue(self.core_camps_report_validator_1._are_all_available_camp_types())
        self.assertTrue(self.core_camps_report_validator_2._are_all_available_camp_types())
        self.assertFalse(self.core_camps_report_validator_3._are_all_available_camp_types())

    def test_validate(self):
        self.assertTrue(self.core_camps_report_validator_1.validate())
        self.assertFalse(self.core_camps_report_validator_2.validate())
        self.assertFalse(self.core_camps_report_validator_3.validate())
```

К сожалению, мне не удалось реализовать более комплексный дизайн ввиду жёсткой привязки проектов к данным.
