# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json

# Create your views here.


def base(request):
    context = {}
    points = []
    for point in range(-21, 21):
        points.append((point, point*point))
    context['points'] = json.dumps(points)
    text = '2+33/545+12-(s*22)*34+sin(x)'
    # print('Text: ', text)
    lexemes = lexical_analysis(text)
    # print('Lexemes: ', lexemes)
    context['test'] = lexemes
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
    output_list = []  # очередь вывода
    return 'test'

