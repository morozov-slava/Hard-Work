import os


#################
### Example 1 ###
#################

# Initial code
def scoring_client_mapper(age: int, education: str, has_credit_history: bool):
    score = 0
    if age < 18:
        raise ValueError("Клиент слишком молод для кредитования.")
    elif age < 25:
        score += 10
    elif age < 40:
        score += 20
    elif age < 60:
        score += 30
    else:
        score += 15
    # Образование
    if education.lower() in ['бакалавр', 'магистр']:
        score += 25
    elif education.lower() in ['среднее', 'профессиональное']:
        score += 15 
    else:
        score += 10
    # credit history scoring
    if has_credit_history:
        score += 30
    # rating
    if score > 70:
        client_rating = 'A'
    elif score > 50:
        client_rating = 'B'
    elif score > 30:
        client_rating = 'C'
    else:
        client_rating = 'D'
    return {"score": score, "rating": client_rating}


# Modified code
class ClientCreditScorer:
    def __init__(self, age: int, education: str, has_credit_history: bool):
        self.age = age
        self.education = education.lower()
        self.has_credit_history = has_credit_history
        
        self.score = 0

    def _age_scoring(self):
        if (self.age >= 18) and (self.age < 25):
            return 10
        if (self.age >= 25) and (self.age < 40):
            return 40
        if (self.age >= 40) and (self.age < 60):
            return 30
        if self.age >= 60:
            return 15

    def _education_scoring(self):
        education_mapper = {
            "бакалавр": 25,
            "магистр": 25,
            "среднее": 15,
            "профессиональное": 15
        }
        return education_mapper.get(self.age, 10)

    def _credit_history_scoring(self):
        if has_credit_history:
            return 30
        return 0

    def _clear_scoring(self):
        self.score = 0
        
    def make_scoring(self):
        self._clear_scoring()
        # scoring
        self.score += self._age_scoring()
        self.score += self._education_scoring()
        self.score += self._credit_history_scoring()

    def get_credit_rating(self):
        if self.age < 18:
            return "Too Young"
        if self.score > 70:
            return "A"
        if self.score > 50:
            return "B"
        if self.score > 30:
            return "C"
        return "D

    def get_credit_score(self):
        return self.score

    def get_age(self):
        return self.age

    def get_education(self):
        return self.education

    def get_has_credit_history(self):
        return self.has_credit_history


# Улучшения:
# 1. Избавился от else
# 2. Разбил логику в отдельные методы
# 3. Избавился от исключений - заменил их выводом специальных значений




#################
### Example 2 ###
#################

# Initial code
def calculate_total_revenue(sales_data: list[dict], tax_rate: float):
    total_revenue = 0
    for sale in sales_data:
        sale_amount = sale['amount']
        sale_type = sale['type']
        # Revenue
        if sale_type == 'product':
            revenue = sale_amount
        elif sale_type == 'service':
            revenue = sale_amount * 1.2
        elif sale_type == 'subscription':
            revenue = sale_amount * 12
        else:
            revenue = sale_amount
        # Taxes
        tax = revenue * tax_rate
        total_revenue += revenue - tax
    return total_revenue


# Modified code
class RevenueReport:

    def _calc_product_revenue(self, amount: float):
        return amount

    def _calc_service_revenue(self, amount: float):
        return amount * 1.2

    def _calc_subsciption_revenue(self, amount: float):
        return amount * 12 # yearly subscription

    def _get_revenue_method(self, method: str):
        methods = {
            "product": self._calc_product_revenue,
            "service": self._calc_service_revenue,
            "subscription": self._calc_subsciption_revenue
        }
        return methods.get(method, self._calc_product_revenue)

    def calc_total_revenue(self, sales_data: list[dict], tax_rate: float):
        total_revenue = 0
        for i in range(len(sales_data)):
            calculator = self._get_revenue_method(sales_data[i]["type"])
            total_revenue += calculator(sales_data[i]["amount"])
        return total_revenue * (1 - tax_rate)

# Улучшения:
# 1. Вынес функционал в отдельный класс
# 2. Избавился от else
# 3. Динамическое добавление чистой функциональности (абстракции)



#################
### Example 3 ###
#################

# Initial code
def is_text_in_files(text: str, path: str):
    f = 0
    os.chdir(path)
    files = os.listdir()
    for file_name in files:
        abs_path = os.path.abspath(file_name)
        if os.path.isdir(abs_path):
            is_text_in_files(abs_path)
        if os.path.isfile(abs_path):
            f = open(file_name, "r")
            if text in f.read():
                f = 1
                print(text + " found in ")
                final_path = os.path.abspath(file_name)
                print(final_path)
                return True

    if f == 1:
        print(text + " not found! ")
        return False


# Modified Code
def get_all_filepaths(path: str):
    all_filepaths = []
    for root, _, files in os.walk(path):
        for file in files:
            all_filepaths.append(os.path.join(root, file))
    return all_filepaths


def is_text_in_files(text: str, path: str):
    filepaths_list = get_all_filepaths(path)
    for filepath in filepaths_list:
        with open(filepath, "r") as f:
            if text in f.read():
                return True
    return False


# Улучшения:
# 1. Ввиду сложности логики в исходной функции, разбил функцию на две.
# 2. Заменил более эффективной и понятной реализацией функцией walk для обхода файловой системы из стандартной библиотеки.
# 3. Снизил кол-во ветвлений в коде (вложенные if конструкции)



