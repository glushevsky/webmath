# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
import cgi
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def data_processing(request):
    from math import sin, cos, sqrt
    request_context = request.GET
    text = request_context['formula']
    svg_width = int(request_context['width'])
    svg_height = int(request_context['height'])
    step_count = svg_width * int(request_context['detail'])

    w = 1.0
    f = 1.0
    m = 1.0
    T = 20.0
    b = 1.0
    d = m*m/(T*T)
    # re_psi = ((d*d - d*(w*w - a*cos(f) - b) - b*w*w)*(a*d*cos(f-w*T) - b*w*w + b*d) - (w*w - a*w*sin(f) - d)*a*d*w*sin(f-w*T))/((a*d*cos(f-w*T)-b*w*w+b*d)*(a*d*cos(f-w*T)-b*w*w+b*d) + a*a*d*w*w*sin(f-w*T)*sin(f-w*T))
    # im_psi = ((d*d - d*(w*w - a*cos(f) - b) - b*w*w)*a*sqrt(d)*w*sin(f-w*T) + sqrt(d)*(w*w - a*w*sin(f) - d)*(a*d*cos(f-w*T)-b*w*w+b*d))/((a*d*cos(f-w*T)-b*w*w+b*d)*(a*d*cos(f-w*T)-b*w*w+b*d) + a*a*d*w*w*sin(f-w*T)*sin(f-w*T))
    # f1 = re_psi*2.0*sqrt(d)*(a*cos(f-w*T) + b) + im_psi-a-w-sin(f-w*T) - 4.0*d*sqrt(d) + 2.0*sqrt(d)*(w*w-a*cos(f)-b)
    # f2 = re_psi*d*(a*cos(f-w*T) + b) + im_psi*sqrt(d)*a*w*sin(f-w*T) - re_psi*b*w*w
    # f3 = -re_psi*a*w*sin(f-w*T) + im_psi*2.0*sqrt(d)*(a*cos(f-w*T) + b) - w*w + 3.0*d + a*w*sin(f)
    # f4 = -re_psi*sqrt(d)*a*w*sin(f-w*T) - re_psi*b*w*w + im_psi*d*(a*cos(f-w*T)+b)

    delta_step = 1.0 / float(request_context['detail'])
    points = []
    for step in range(-step_count, step_count):
        try:
            a = step*delta_step
            re_psi = ((d * d - d * (w * w - a * cos(f) - b) - b * w * w) * (
                        a * d * cos(f - w * T) - b * w * w + b * d) - (w * w - a * w * sin(f) - d) * a * d * w * sin(
                f - w * T)) / ((a * d * cos(f - w * T) - b * w * w + b * d) * (
                        a * d * cos(f - w * T) - b * w * w + b * d) + a * a * d * w * w * sin(f - w * T) * sin(
                f - w * T))
            im_psi = ((d * d - d * (w * w - a * cos(f) - b) - b * w * w) * a * sqrt(d) * w * sin(f - w * T) + sqrt(
                d) * (w * w - a * w * sin(f) - d) * (a * d * cos(f - w * T) - b * w * w + b * d)) / (
                                 (a * d * cos(f - w * T) - b * w * w + b * d) * (
                                     a * d * cos(f - w * T) - b * w * w + b * d) + a * a * d * w * w * sin(
                             f - w * T) * sin(f - w * T))
            f1 = re_psi * 2.0 * sqrt(d) * (a * cos(f - w * T) + b) + im_psi - a - w - sin(f - w * T) - 4.0 * d * sqrt(
                d) + 2.0 * sqrt(d) * (w * w - a * cos(f) - b)
            f2 = re_psi * d * (a * cos(f - w * T) + b) + im_psi * sqrt(d) * a * w * sin(f - w * T) - re_psi * b * w * w
            f3 = -re_psi * a * w * sin(f - w * T) + im_psi * 2.0 * sqrt(d) * (
                        a * cos(f - w * T) + b) - w * w + 3.0 * d + a * w * sin(f)
            f4 = -re_psi * sqrt(d) * a * w * sin(f - w * T) - re_psi * b * w * w + im_psi * d * (a * cos(f - w * T) + b)
            points.append([a, f1*f2+f3*f4])
            # points.append([x, eval(text)])
        except ValueError:
            pass
    return HttpResponse(json.dumps(points))


def base(request):
    context = {}
    # from math import sin, cos, sqrt
    # points = []
    svg_width = 1400
    svg_height = 600
    variables = ['x', 'y', 'a', 'b', 'w']
    # text = '4*sqrt(x)+25'
    # step_count = svg_width*10
    # #current_step = 0
    # delta_step = 0.1
    # for step in range(-step_count, step_count):
    #     try:
    #         x = step*delta_step
    #         points.append([x, eval(text)])
    #     except ValueError:
    #         pass
    #
    # context['points'] = json.dumps(points)
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


