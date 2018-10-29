# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
from math import *
# import cgi
# from django.views.decorators.csrf import csrf_exempt

variables = ['a', 'b', 'f', 'w', 'T']


# Create your views here.
def data_processing(request):
    # from math import sin, cos, sqrt
    # get data
    request_context = request.GET
    text = request_context['formula']
    svg_width = int(request_context['width'])
    svg_height = int(request_context['height'])
    parameters = json.loads(request_context['parameters'])
    step_count = svg_width * int(request_context['detail'])
    delta_step = 1.0 / float(request_context['detail'])
    points = []
    # creating parameters
    for param in parameters:
        globals()[param['name']] = float(param['value'])
    for step in range(-step_count, step_count):
        try:
            x = step*delta_step
            points.append([x, eval(text)])
        except ValueError:
            pass
    return HttpResponse(json.dumps(points))


def base(request):
    context = {}
    svg_width = 1200
    svg_height = 600
    context['svg_width'] = svg_width
    context['svg_height'] = svg_height
    context['variables'] = variables
    return render(request, 'base_page.html', context)


def lexical_analysis(text):
    '''
    Splitting an input formula from string format into a list of lexemes
    :param text: str formula
    :return: list of lexemes (?)
    '''
    text = text.replace(' ', '')
    delimiters = ['^', '*', '/', '+', '-', '(', ')']  # возможные разделители
    text_len = len(text)
    lexemes = []
    number = 0
    while number < text_len:
        if text[number] in delimiters:  # если является разделителем
            lexemes.append(text[number])
        elif text_len - number >= 6 and text[number:number + 3] in ['sin', 'cos']:
            lexemes.append(text[number:number + 3])
            number += 2
        else:  # если это константа/переменная
            tmp_lexeme = ''
            while text[number] not in delimiters:
                # пока не встретится разделитель или sin/cos
                if text_len - number >= 6 and text[number:number + 3] in ['sin', 'cos']:
                    break
                else:
                    tmp_lexeme += text[number]
                number += 1
            number -= 1
            lexemes.append(tmp_lexeme)
        number += 1
    return lexemes


def sorting_station(lexemes):
    from graph.stack import Stack
    from math import sin, cos
    output_list = []  # очередь вывода
    operation_stack = Stack()
    # for lexeme in lexemes:
    #     if
    print(lexemes)
    x=1
    y = 1.57
    delta = 3
    result = eval(lexemes)
    print(result)
    return 'test'


