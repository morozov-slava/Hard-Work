**Пример-1**

Исходный код:

```py
# Если это первый прогон, то мы считаем для всех кампаний 
# При повторных запусках берём только кампании под мониторингом
if len(dfp_actual_analytical_report):
    query_active_camps = query_active_campaigns(today, camps_id_to_exclude, n_month_monitoring)
else:
    query_active_camps = query_all_campaigns(camps_id_to_exclude)

filepath_active_camps = os.path.join(path_data, "active_camps.csv") 
dfp_active_camps = orc.execute_query(
    db_configs, query_active_camps, save_result=True, filepath=filepath_active_camps
)
```

**Дизайн:**

Выгружаем перечень всех кампаний, для которых доступны отчётные периоды.
    1. Из таблицы со статистикой за все периоды отбираем те кампании и отчётные периоды, которые не были посчитаны.
    2. Из таблицы с полными перечнем всем кампаний отбираем новые кампании, которых ещё нет в таблице со статистикой.
    3. Отбираем из таблицы с полным перечнем всех кампаний новые кампании и старые, для которых не были посчитаны отчётные периоды.


Существующий код отличается от описанного дизайна. Для этого дизайна в принципе напрашивается другой код.

Новый код:

```py
old_reportable_camps = get_old_reportable_campaigns()
new_reportable_camps = get_new_reportable_campaigns()
all_reportable_camps = set(old_reportable_camps).union(set(new_reportable_camps))
if len(all_reportable_camps) != len(old_reportable_camps) + len(new_reportable_camps):
    raise AssertionError
df_reportable_campaigns = get_reported_campaigns_dataset(all_reportable_camps)
```

Для данного кода итерация заняла около 45 минут, но для данного примера я большой объём кода опустил, т.к. там есть аспекты бизнес-логики + SQL-запросы



**Пример-2**


Исходный код:

```py
import polars as pl
import numpy as np

from sklearn.model_selection import train_test_split


class SampleSplitter:
    
    @staticmethod
    def random_split(df: pl.DataFrame, core_share: float):
        if "IS_CORE" in df.columns:
            raise KeyError("There is already column 'IS_CORE'")
        df_splitted = df.clone()
        # generate UCG flag array
        is_core_group_array = np.random.choice(
            [1, 0], size=df.shape[0], p=[core_share, 1-core_share]
        )
        df_core = df_splitted[np.where(is_core_group_array == 1)[0]]
        df_other = df_splitted[np.where(is_core_group_array == 0)[0]]
        return df_core, df_other
    
    @staticmethod
    def stratified_splitting(df: pl.DataFrame, columns: list, core_share: float):
        df_core, df_other = train_test_split(
            df, train_size=core_share, 
            stratify=df.select(columns),
        )
        return df_core, df_other

```


**Дизайн:**

Область алгоритма:
Необходимы 2 алгоритма для разбиения некоторой выборки:
    1. Генерация случайной бинарной выборки (0 и 1) заданного размера с некоторым вероятностным соотношением.
    2. Генерация стратифицированной бинарной выборки (0 и 1) относительно некоторого вектора с длиной равной длине вектора.
       (данная реализация в целом уже есть в функции `train_test_split()`)

Область бизнес-логики:
    1. Разбиение табличного датасета по алгоритму случайного бинарного разбиения на две группы с формированием поля `IS_CORE`
    2. Разбиение табличного датасета по алгоритму стратифицированного бинарного разбиения на две группы с формированием поля `IS_CORE`

Существующий код отличается от описанного дизайна тем, что я объединил в нём два интерфейса. 
Соответственно, здесь можно реализовать эти два интерфейса.


**Новый код:**

```py
from abc import ABC, abstractmethod

import polars as pl
import numpy as np
from sklearn.model_selection import train_test_split


class ParentDatasetSplitter(ABC):

    def __init__(self, dataset: pl.DataFrame):
        if "IS_CORE" in dataset.columns:
            raise KeyError("There is already column 'IS_CORE' in dataset")
        self.df = dataset
        self.dataset_core = None
        self.dataset_other = None

    @abstractmethod
    def split(self) -> None:
        raise NotImplementedError


    # Additional methods
    def get_dataset(self):
        return self.dataset

    def get_dataset_core(self):
        return self.dataset_core
    
    def dataset_other(self):
        return self.dataset_other


class BinaryRandomDatasetSplitter(ParentDatasetSplitter):
    def __init__(self):
        super().__init__()

    def _binary_random_splitting(self, size: int, one_label_share: float) -> np.array:
        return np.random.choice([1, 0], size=size, p=[one_label_share, 1-one_label_share])

    def split(self, core_share: float) -> None:
        is_core_array = self.make_binary_random_splitting(self.df.shape[0], core_share)
        df_splitted = self.df.with_columns(
            pl.lit(is_core_array).alias("IS_CORE")
        )
        self.dataset_core = df_splitted.filter(pl.col("IS_CORE") == 1)
        self.dataset_other = df_splitted.filter(pl.col("IS_CORE") == 0)


class BinaryStratifiedDatasetSplitter(ParentDatasetSplitter):
    def __init__(self):
        super().__init__()

    def split(columns: list, core_share: float) -> None:
        df_core, df_other = train_test_split(self.df, train_size=core_share, stratify=self.df.select(columns))
        self.dataset_core = df_core
        self.dataset_other = df_other
```

Для данного кода итерация заняла около часа.


К сожалению, у меня есть не так много подходящего кода, который можно было бы использовать в рамках данного задания, т.к. большая часть ML-кода довольна прямолинейна сама по себе и упирается в конкретные реализации и общепринятые концепции по работе с данными.