from django.shortcuts import render, render_to_response
from django.template import RequestContext
from Main.forms import RelationModelDataForm
from Main.mapper import *


def data_to_model(request):
    if request.method == 'GET':
        rel_form = RelationModelDataForm()
    if request.method == 'POST':
        rel_form = RelationModelDataForm(request.POST)
        print('rel_form: %s' % rel_form)
        if rel_form.is_valid():
            cd = rel_form.cleaned_data
            print('cleaned_data: %s' % cd)
            # try:
            #     Mapper(data_addr=cd['data_addr'], model_type=cd['model_type'])
            # except Exception('Unsupported input data format')

    return render_to_response('data_to_model.html', {'all_models': MODELS_LIST}, context_instance=RequestContext(request))