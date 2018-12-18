# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json
from math import *
import numpy

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


# yf
def checking(formula, **parameters):
    # print('hello')
    # print(formula)
    # print(parameters)
    # print(eval(formula)
    zeros = []
    file_a1 = open('zeros_a1.txt', 'w')
    file_a1.write('f T w b res\n')
    steps = 628.0*1000.0*1000.0*500.0
    step = 0
    for b in numpy.arange(0.0, 50.0, 0.001):
        tmp_result = eval(formula)
        if abs(tmp_result) < 0.0001:
            file_a1.write(str(b) + ' ' + str(tmp_result) + '\n')
            zeros.append([b, tmp_result])
    # for f in numpy.arange(0.0, 6.28, 0.01):
    #     print(str(round(step * 100.0 / steps)) + '%')
    #     for T in numpy.arange(0.0, 100.0, 0.1):
    #         for w in numpy.arange(0.0, 100.0, 0.1):
    #             for b in numpy.arange(0.0, 50.0, 0.1):
    #                 tmp_result = eval(formula)
    #                 step += 1
    #                 if abs(tmp_result) < 0.0001:
    #                     file_a1.write(str(f) + ' ' + str(T) + ' ' + str(w) + ' ' + str(b) + ' ' + str(tmp_result) + '\n')
    file_a1.close()
    return zeros

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
    step_count2 = svg_height * int(request_context['detail'])
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
    elif type_selector == 'sign':  # sign values case
        omega = globals()['b']
        cos_part = eval('cos(f) - cos(f - w*T)')
        sin_part = eval('sin(f) - sin(f - w*T)')
        for step1 in range(-1*int(request_context['detail']), 1*int(request_context['detail'])):
            for step2 in range(-1*int(request_context['detail']), 1*int(request_context['detail'])):
                a = step1 * delta_step
                b = step2 * delta_step
                try:
                    l_sign = 0
                    # вычисления для lambda2
                    try:
                        Re_lambda2 = eval('-1.0 - omega**2 * (w**2 - a*cos_part + a*sin(f - w*T)*(w**2 - a*w*sin_part)/(b*w) + (w**2 - a*w*sin_part)*(w**2 - a*w*sin_part)/(2.0*b*w**2))/(b*w**2)')
                        if Re_lambda2 > 0.0:
                            l_sign = 1
                        elif Re_lambda2 < 0.0:
                            l_sign = -1
                    except:
                        l_sign = 2
                        pass
                    # проверка дельты
                    d_flag = 0
                    d_list = []
                    try:
                        coeff_1 = eval('2.0*b+1+2.0*a*cos(f)-w**2')
                        coeff_2 = eval('-w**2*(2.0*b+1)+2.0*a*(b*cos(f)+w*sin(f)-b*cos(f-w*T)) - a**2*(sin(f)**2-sin(f-w*T)**2)')
                        delta_status, delta_root1, delta_root2 = quadratic_equation_results(1.0, coeff_1, coeff_2)
                        # print(a, delta_status)
                        if delta_status:  # если удалось найти корни
                            if delta_root1 > 0.0:
                                d_flag += 1
                                d_list.append(delta_root1)
                            if delta_root2 > 0.0:
                                d_flag += 1
                                d_list.append(delta_root2)
                    except:
                        pass
                    # вычисления для lambda1
                    L1_sign = 2  # если ошибка
                    if not d_list:
                        pass
                    else:
                        L1_counter = -1  # если только отрицательные значения
                        for d in d_list:
                            try:
                                text_parts = [
                                    ['Re_psi','((d**2-d*(w**2-a*cos(f)-b)-b*w**2)*(a*d*cos(f-w*T)-b*w**2+b*d)-(w**2-a*w*sin(f)-d)*a*d*w*sin(f-w*T))/((a*d*cos(f-w*T)-b*w**2+b*d)**2+a**2*d*w**2*(sin(f-w*T))**2)'],
                                    ['Im_psi','((d**2-d*(w**2-a*cos(f)-b)-b*w**2)*a*sqrt(d)*w*sin(f-w*T)+sqrt(d)*(w**2-a*w*sin(f)-d)*(a*d*cos(f-w*T)-b*w**2+b*d))/((a*d*cos(f-w*T)-b*w**2+b*d)**2+a**2*d*w**2*(sin(f-w*T))**2)'],
                                    ['F1', 'Re_psi*2.0*sqrt(d)*(a*cos(f-w*T)+b)+Im_psi*a*w*sin(f-w*T)-4.0*d*sqrt(d)+2.0*sqrt(d)*(w**2-a*cos(f)-b)'],
                                    ['F2', 'Re_psi*d*(a*cos(f-w*T)+b)+Im_psi*sqrt(d)*a*w*sin(f-w*T)-Re_psi*b*w**2'],
                                    ['F3', '-Re_psi*a*w*sin(f-w*T)+Im_psi*2.0*sqrt(d)*(a*cos(f-w*T)+b)-w**2+3.0*d+a*w*sin(f)'],
                                    ['F4', '-Re_psi*sqrt(d)*a*w*sin(f-w*T)-Im_psi*b*w**2+Im_psi*d*(a*cos(f-w*T)+b)']
                                    ]
                                final_formula = 'F1*F2+F3*F4'
                                for part in text_parts:
                                    # part = part.replace(' ', '')
                                    globals()[part[0]] = eval(part[1].replace(' ', ''))
                                final_result = eval(final_formula)
                                if final_result > 0.0 and L1_counter != 2:  # если существует положительное значение
                                    L1_counter = 1
                            except:
                                L1_counter = 2
                                pass
                        if L1_counter != 2:
                            L1_sign = L1_counter
                    points.append(([a, b, l_sign, d_flag, L1_sign]))
                except:
                    pass
    elif type_selector == 'a1':  # проверка знаменателя a1 на нули
        check_formula = '(w**2+b)*cos(f)+w*sin(f)-b*cos(f-w*T)'
        print(parameters)
        # checking(check_formula, b=globals()['b'], f=globals()['f'], T=globals()['T'], w=globals()['w'])
        zero_list = checking(check_formula, f=globals()['f'], T=globals()['T'], w=globals()['w'])
        # checking(check_formula)
    elif type_selector == 'resolve':  # проверка разрешимости lambda1 (при a1)
        try:
            theta = 0.0
            dzeta = eval('w*T')
            while abs(dzeta) > 2.0*pi:
                if dzeta > 0.0:
                    dzeta = dzeta - 2.0*pi
                elif dzeta < 0.0:
                    dzeta = dzeta + 2.0*pi
            # print (dzeta)
            if dzeta > 0.0:
                theta = 2.0*pi - dzeta
            elif dzeta < 0.0:
                theta = -2.0*pi - dzeta
            # print(theta)
            # print(eval('theta + w*T')/(2.0*pi))
        except:
            zero_list.append('Невозможно вычислить theta')
        try:
            A_value = eval('(-w**3 - (2.0*b + 1)*w)/((w**2 + b) * cos(f) + w*sin(f) - b*cos(f-w*T))')
        except:
            zero_list.append('Невозможно вычислить А')
        try:
            part1 = eval('2.0*(w**2+b)+w*A_value*cos(f)')
            part2 = eval('2.0*b+w*A_value*cos(f-w*T)')
            part3 = eval('w*(2.0+A_value*sin(f))')
            delimiter = eval('(2.0*b + w*A_value*cos(f-w*T))**2 + (sin(f-w*T))**2')
            cosV_value = eval('(part1*part2 + part3*sin(f-w*T))/delimiter')
            sinV_value = eval('-(part1*sin(f-w*T)-part2*part3)/delimiter')
            if abs(cosV_value) > 1.0 or abs(sinV_value) > 1.0:
                zero_list.append('Значение cos или sin некорректно')
        except:
            zero_list.append('Невозможно вычислить exp')
        try:
            V_value = acos(cosV_value)
            a1_value = (theta + V_value)* A_value
        except:
            zero_list.append('Невозможно вычислить a1')
        try:
            lpart = eval('-2.0*w**2 + cos(V_value)*(w**2*a1_value*cos(f-w*T)+2.0*w*b*(theta+V_value)) - sin(V_value)*w**2 * a1_value*sin(f-w*T)')
            rpart = eval('2.0*w**3 + 2.0*w*b + cos(V_value)* w**2 * a1_value*sin(f-w*T) + sin(V_value)*(w**2 * a1_value * cos(f-w*T) + 2.0*w*(theta+V_value)*b)')
            zero_list.append('Theta = ' + str(theta) + '; Omega = ' + str(V_value) + '; Знаменатель lambda1 = ' + str(lpart**2 + rpart**2))
        except:
            zero_list.append('Невозможно вычислить знаменатель lambda1')
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
    # print(points)
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


