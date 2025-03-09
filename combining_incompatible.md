

**Пример-1**

Пример исходного кода с комментариями (ранее для класса ниже не было никаких комментариев)

```py
# Root-Causes Analysis (RCA) для текущей реализации подразумевает расчёт некоторого перечня метрик
# для графа инцидентов.
# Граф с инцидентами обязательно должен содержать только объекты, для которых в системе на момент расчёта RCA был зафиксирован инцидент (авария).
# Таким образом, сама числовая оценка RCA для некоторого объекта представляет собой взвешенную оценку для некоторого числа метрик
 
class RcaMetrics:
    def __init__(self, graph):
        self.graph = graph # incidents graph
        self.metrics = {k: dict() for k in self.graph.nodes()}

    def _calculate_metric_1(self, depth: int):
        pass

    def _calculate_metric_2(self, depth: int):
        pass

    def _calculate_metric_3(self):
        pass

    def _calculate_metric_4(self):
        pass

    def calculate_rca_metrics(self, metric_1_depth: int, metric_2_depth: int):
        pass 
```

Часть функционала и детали логики работы класса изменил, ввиду ограничений на распространение данной информации.
В процессе описания данного класса понял, что его в принципе стоит несколько иначе переработать :)


**Пример-2**

Пример исходного кода с комментариями (ранее для класса ниже не было никаких комментариев).

```py
# Автоматический подбор гиперпараметров для некоторого распределения возможных значений гиперпараметра
# с помощью оптимизатора Optuna. 
# Так, для каждой модели можно настроить свой АТД с некоторым зафиксированным набором гиперпараметров для оптимизации.
class OptunaOptimizer(ABC):
    def __init__(self, model: object, loss_func: object):
        self.model = model
        self.loss_func = loss_func
        self.study = None

    @abstractmethod
    def objective(self, trial):
        raise NotImplementedError

    def optimize(self, direction: str, n_trials: int) -> None:
        study = optuna.create_study(direction=direction)
        study.optimize(self.objective, n_trials=n_trials)
        self.study = study

    def get_best_params(self):
        if self.study is not None:
            return self.study.best_params
        return None

    def get_best_error(self):
        if self.study is not None:
            return self.study.best_value
        return None

    # Additional commands
    def get_model(self):
        return self.model

    def get_loss_func(self):
        return self.loss_func

    def get_study(self):
        return self.study
```

Данный пример с абстрактным классом может быть полезно описать с позиции дизайна для лучшего понимания, какую часть системы
может представлять данный функционал, а также как он может быть расширяем и для чего использоваться.



**Пример-3**

Добавил комментарий перед функцией (ниже исходный код с комментарием):

```py
# Объект "Дерево объектов (objects_tree)" представляет собой отображение статической информации обо всех объектах системы.
# Наиболее ценные данные по ним - это информация для их идентификации, а также о связи между объектами системы.
def preprocess_objects_tree(df_objects_tree: pd.DataFrame):
    df = df_objects_tree.copy()
    # 1. Handle Null values
    df["last_state_update"] = df["last_state_update"].fillna(df["updated"])
    df = df.dropna(subset=["last_state_update"])
    # 2. Convert timestamp to datetime
    df["last_state_update"] = df["last_state_update"].astype("int64")
    df["last_state_update"] = df["last_state_update"].apply(utils.unix_to_datetime)
    # 3. Convert key fields to string type
    df["name"] = df["name"].astype("str")
    df["id"] = df["id"].astype("str")
    return df

```

Лучше, пожалуй, будет разбить данную функцию хотя бы на 2 класса (для представления самого объекта и пайплайна его предобработки).
Тем не менее, описание дизайна предобработки данных, полагаю, требует описания требований к самим данным.


Помимо описанного в материалах СИ, как мне кажется, может быть достаточно следующих описательных компонентов:

- Описание класса в соответствии с подходом АТД.
- Ведение проектной документации (в целом с описанием проекта).
- Описание ожидаемых атрибутов на входе (что они с собой представляют и каким требованиям должны соответствовать).
- Описание сущностей "скрытых" в классе (если они есть). Их как раз можно было бы выносить как комментарии, либо и вовсе реализовать в рамках некоторой отдельной сущности (здесь, к сожалению, конкретных примеров реализации в моменте предложить не могу).


