# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
from math import *

# TODO: постмотреть SymPy и https://github.com/augustt198/latex2sympy (конвертер latex в sympy)
# import cgi
# from django.views.decorators.csrf import csrf_exempt

variables = ['w', 'f', 'T', 'b']
# lambda1_variables = ['w', 'f', 'm', 'T', 'b']


# нахождение корней квадратного уравнения ax^2+bx+c=0
def quadratic_equation_results(quad_coefficient, linear_coefficient, const_coefficient):
    # quad_coefficient = eval(a)
    # linear_coefficient = eval(b)
    # const_coefficient = eval(c)
    try:
        discriminant = linear_coefficient**2 - 4.0*quad_coefficient*const_coefficient
        denominator = 2.0*quad_coefficient
        if discriminant == 0.0:
            return True, -linear_coefficient/denominator
        elif discriminant > 0.0:
            return True, (-linear_coefficient - sqrt(discriminant))/denominator, (-linear_coefficient + sqrt(discriminant))/denominator
    except:
        return False, 0.0, 0.0
    return False, 0.0, 0.0


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
    substep_count = 2000000
    delta_step = 1.0 / float(request_context['detail'])
    points = []
    # creating parameters
    for param in parameters:
        globals()[param['name']] = float(param['value'])

    type_selector = request_context['type_selector']
    zero_list = []  # список точек с делением на ноль
    empty_delta_list = []  # список точек, в которых delta невычислима
    negative_delta_list = []  # список точек с отрицательными delta
    if type_selector == 'lambda1':  # special  case
        final_formula = request_context['final_formula'].replace(' ', '')
        text_parts = text.split('\n')
        # for part in text_parts:
        #     print('===', part)
        m = 1
        # d = eval('m * m / (T * T)')
        for step in range(-step_count, step_count):
            a = step * delta_step
            # вычисление delta
            try:
                coeff_1 = eval('2.0*b+1+2.0*a*cos(f)-w**2')
                coeff_2 = eval('-w**2*(2.0*b+1)+2.0*a*(b*cos(f)+w*sin(f)-b*cos(f-w*T)) - a**2*(sin(f)**2-sin(f-w*T)**2)')
            except:
                # print('empty', step * delta_step)
                empty_delta_list.append(step * delta_step)
                pass
            # print(a, w, b, f)
            # print('COEF 1', coeff_1)
            # print('COEF 2', coeff_2)
            delta_status, delta_root1, delta_root2 = quadratic_equation_results(1.0, coeff_1, coeff_2)
            # print(a, delta_status)
            if delta_status:  # если удалось найти корни
                # формирования списка положительных корней
                d_list = []
                if delta_root1 >= 0.0:
                    d_list.append(delta_root1)
                if delta_root2 >= 0.0:
                    d_list.append(delta_root2)
                # print(d_list)
                if not d_list:
                    # print('negative', step*delta_step)
                    negative_delta_list.append(step * delta_step)
                    pass
                else:
                    for d in d_list:
                        # print(a, '===', d)
                        try:
                            for part in text_parts:
                                part = part.replace(' ', '')
                                # print('>>>', part.split('=')[0])
                                globals()[part.split('=')[0]] = eval(part.split('=')[1])
                                # print(globals()['f1'])
                            # print('______________________')
                            # print(eval(final_formula))
                            points.append(([a, eval(final_formula)]))
                            # re_psi = eval('((d * d - d * (w * w - a * cos(f) - b) - b * w * w) * (a * d * cos(f - w * T) - b * w * w + b * d) - (w * w - a * w * sin(f) - d) * a * d * w * sin(f - w * T)) / ((a * d * cos(f - w * T) - b * w * w + b * d) * (a * d * cos(f - w * T) - b * w * w + b * d) + a * a * d * w * w * sin(f - w * T) * sin(f - w * T))')
                            # im_psi = eval('((d * d - d * (w * w - a * cos(f) - b) - b * w * w) * a * sqrt(d) * w * sin(f - w * T) + sqrt(d) * (w * w - a * w * sin(f) - d) * (a * d * cos(f - w * T) - b * w * w + b * d)) / ((a * d * cos(f - w * T) - b * w * w + b * d) * (a * d * cos(f - w * T) - b * w * w + b * d) + a * a * d * w * w * sin(f - w * T) * sin(f - w * T))')
                            # f1 = eval('re_psi * 2.0 * sqrt(d) * (a * cos(f - w * T) + b) + im_psi - a - w - sin(f - w * T) - 4.0 * d * sqrt(d) + 2.0 * sqrt(d) * (w * w - a * cos(f) - b)')
                            # f2 = eval('re_psi * d * (a * cos(f - w * T) + b) + im_psi * sqrt(d) * a * w * sin(f - w * T) - re_psi * b * w * w')
                            # f3 = eval('-re_psi * a * w * sin(f - w * T) + im_psi * 2.0 * sqrt(d) * (a * cos(f - w * T) + b) - w * w + 3.0 * d + a * w * sin(f)')
                            # f4 = eval('-re_psi * sqrt(d) * a * w * sin(f - w * T) - re_psi * b * w * w + im_psi * d * (a * cos(f - w * T) + b)')
                            # points.append([a, f1 * f2 + f3 * f4])
                        except ValueError:
                            pass
                        except ZeroDivisionError:
                            # print('zero_division')
                            zero_list.append(step * delta_step)
                            pass
            else:  # если корни не найдены
                # print('empty', step * delta_step)
                empty_delta_list.append(step * delta_step)
                pass
    else:  # common cases
        for step in range(-step_count, step_count):
            try:
                x = step*delta_step
                points.append([x, eval(text)])
            except ValueError:
                pass
            except ZeroDivisionError:
                # print('zero_division')
                zero_list.append(step * delta_step)
                pass
    print(points)
    # new_points = []
    # for step in range(0, len(points), 10):
    #     new_points.append(points[step])

    return HttpResponse(json.dumps([points, zero_list, empty_delta_list, negative_delta_list]))


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


