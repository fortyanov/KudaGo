from django.forms import *
#from Main.mapper import MODELS_LIST


class MapperInpForm(Form):
    #model_type = ChoiceField(label='Модель', choices=[(m, m) for m in MODELS_LIST])
    data_addr = URLField(label='Адрес', max_length=100)
    trash_fields = CharField(label='Лишние поля', max_length=100, required=False)