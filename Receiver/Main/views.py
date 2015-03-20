from django.shortcuts import render, render_to_response
from django.template import RequestContext
from Main.forms import MapperInpForm
from mapper.main import *
from mapper.errors import WrongTrashField, WrongContent


def data_to_model(request):
    data = contype = success = ''
    if request.method == 'GET':
        map_form = MapperInpForm()
    if request.method == 'POST':
        map_form = MapperInpForm(request.POST)
        if map_form.is_valid():
            cd = map_form.cleaned_data
            print('cleaned_data: %s' % cd)
            m = Mapper(url=cd['data_addr'], trash_fields=cd['trash_fields'])
            m.fill_model()

            try:
                data = m.data
            except (WrongTrashField, WrongContent):
                pass
            contype = m.contype
            success = m.success

    return render_to_response('data_to_model.html',
                              {'data': data, 'contype': contype, 'success': success},
                              context_instance=RequestContext(request))