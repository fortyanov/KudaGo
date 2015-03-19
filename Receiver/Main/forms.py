from django.forms import *
from Main.mapper import MODELS_LIST


class RelationModelDataForm(Form):
    model_type = ChoiceField(label='Модель', choices=[(m, m) for m in MODELS_LIST])
    data_addr = URLField(label='Адрес', max_length=100)