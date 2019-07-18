# -*- coding: utf-8 -*-
import sys
import os
import randomvalue
import re
import json


if_num_min = 1
if_num_max = 5

#最小值不能修改！！！
switch_num_min = 2
switch_num_max = 5

func_num_min = 1
func_num_max = 5

tab_level_1 = "\t"
tab_level_2 = "\t\t"
tab_level_3 = "\t\t\t"


def inline_model_tablevel(level):
    param_name = randomvalue.stringvalue()
    param_value = randomvalue.stringvalue()

    result_string = ""
    tab_string = ""
    if level == 1:
        tab_string = f'{tab_level_1}'
    elif level == 2:
        tab_string = f'{tab_level_2}'
    elif level == 3:
        tab_string = f'{tab_level_3}'
    else:
        tab_string = f'{tab_level_3}\t'
    result_string = f'{tab_string}NSString *{param_name} = @\"{param_value}\";\n{tab_string}NSLog(@\"%@\", {param_name});\n'
    return result_string

def if_model():

    param_name = randomvalue.stringvalue()
    param_value = randomvalue.intvalue(0,1000)
    if_string = f"\tint {param_name} = {param_value};\n"

    #if的分支数
    random_num = randomvalue.intvalue(if_num_min,if_num_max)

    if random_num == 1:
        inline_string = inline_model_tablevel(2)
        if_string = f'{if_string}\tif ({param_name} <= 1000){{\n{inline_string}\t}}\n'
    elif random_num == 2:
        inline_string1 = inline_model_tablevel(2)
        inline_string2 = inline_model_tablevel(2)
        if_string = f'{if_string}\tif ({param_name} <= 500){{\n{inline_string1}\t}}else{{\n{inline_string2}\t}}\n'
    else:
        level = 1000/random_num
        for num in range(1,random_num+1):
            if num == 1:
                inline_string = inline_model_tablevel(2)
                level_num_str = str(level*num)
                if_string = f'{if_string}\tif ({param_name} <= {level_num_str}){{\n{inline_string}\t}}\n'
            elif num == random_num:
                inline_string = inline_model_tablevel(2)
                if_string = f'{if_string}\telse{{\n{inline_string}\t}}\n'
            else:
                level_num_str = str(level*(num-1))
                level_num_str1 = str(level*num)
                inline_string = inline_model_tablevel(2)
                if_string = f'{if_string}\telse if({param_name} > {level_num_str} && {param_name} <= {level_num_str1}){{\n{inline_string}\t}}\n'
    return f'\n{if_string}\n'

def switch_model():

    param_name = randomvalue.stringvalue()
    param_value = randomvalue.intvalue(switch_num_min,switch_num_max)
    switch_string = f"\tint {param_name} = {param_value};\n"

    #switch的分支数
    random_num = randomvalue.intvalue(switch_num_min,switch_num_max)
    randstring1 = randomvalue.stringvalue()
    if random_num == switch_num_min:
        inline_string1 = inline_model_tablevel(3)
        switch_string = f'{switch_string}\tswitch ({param_name}) {{\n{tab_level_2}case 2:{{\n{inline_string1}{tab_level_3}}}break;\n{tab_level_2}default:{{\n{tab_level_3}NSLog(@\"do not catch anything\");\n{tab_level_3}}}break;\n\t}}\n'
    else:
        for num in range(switch_num_min,random_num+1):
            if num == switch_num_min:
                inline_string1 = inline_model_tablevel(3)
                switch_string = f'{switch_string}\tswitch ({param_name}) {{\n{tab_level_2}case 2:{{\n{inline_string1}{tab_level_3}}}break;\n'
            elif num == random_num:
                switch_string = f'{switch_string}\n{tab_level_2}default:\n{tab_level_3}{{NSLog(@\"do not catch anything\");\n{tab_level_3}}}break;\n\t}}\n'
            else:
                inline_string1 = inline_model_tablevel(3)
                num_str = str(num)
                switch_string = f'\n{switch_string}\n{tab_level_2}case {num_str}:{{\n{inline_string1}{tab_level_3}}}break;'
    return f'\n{switch_string}\n'

# 自定义函数的调用
def constom_func_call_model(funcjsonstring,tablevel):
    funcdic = eval(funcjsonstring)
    if funcdic["funcname"] == "":
        print("函数名为空")
        return
    obj_name = randomvalue.stringvalue()
    class_type = funcdic["class_name"]

    func_string = ""
    func_string = f'{tab_level_1}{class_type} *{obj_name} = [{class_type} new];\n'

    params_name = []
    for i in range(0,len(funcdic["params"])):
        params_name.append(randomvalue.stringvalue())

    param_init_string = ""
    for i in range(len(funcdic["params"])):
        param_init_string = f'{param_init_string}{tab_level_1}{funcdic["params"][i]} {params_name[i]};\n'


    call_string = ""
    if len(params_name) == 0:
        call_string = f'{tab_level_1}[{obj_name} {funcdic["funcname"]}];\n'
    else:
        if len(funcdic["descrip"]) == 1:
            call_string = f'{tab_level_1}[{obj_name} {funcdic["funcname"]}:{params_name[0]}];\n'
        else:
            call_string = f'{tab_level_1}[{obj_name} {funcdic["funcname"]}:{params_name[0]} '
            for i in range(1,len(funcdic["descrip"])):
                call_string = f'{call_string}{funcdic["descrip"][i]}:{params_name[i]} '
            call_string = f'{call_string}];\n'

    return f'\n{func_string}{param_init_string}{call_string}\n'

# 系统函数的调用
def system_func_call_model(funcjsonstring,tablevel):

    funcdic = eval(funcjsonstring)
    if funcdic["funcname"] == "":
        print("函数名为空")
        return
    class_name = randomvalue.stringvalue()
    class_string = randomvalue.stringvalue()

    func_string = ""
    func_string = f'{tab_level_1}Class {class_name} = NSClassFromString(@\"{class_string}\");\n'

    msg_send_param = ""
    param_string = ""
    param_descri_string = ""
    sel_name = randomvalue.stringvalue()
    if len(funcdic["params"]):
        for i in range(len(funcdic["params"])):
            param_name = randomvalue.stringvalue()
            param_string = f'{param_string}{tab_level_1}id {param_name};\n'
            msg_send_param = f'{msg_send_param},{param_name}'
            if i != 0:
                param_descri_string = f'{param_descri_string}:{funcdic["descrip"][i-1]}'
        if param_descri_string == "":
            param_descri_string = ":"
        sel_string = f'{tab_level_1}SEL {sel_name} = @selector({funcdic["funcname"]}{param_descri_string}:);\n'
        func_string = f'{func_string}{param_string}{sel_string}'
    else:
        sel_string = f'{tab_level_1}SEL {sel_name} = @selector({funcdic["funcname"]});\n'
        func_string = f'{func_string}{sel_string}'

    func_string = f'{func_string}{tab_level_1}objc_msgSend({class_name},{sel_name}{msg_send_param});'
    return f'\n{func_string}\n'

# 自定义函数的声明
def constom_func_head_model(funcdic):

    
    func_head_string = ""
    func_head_string = f'- (void) {funcdic["funcname"]}:({funcdic["params"][0]}){funcdic["descrip"][0]}'

    descrp_string = ""
    for j in range(1,len(funcdic["descrip"])):
        descrp_string = f'{descrp_string} {funcdic["descrip"][j]}:({funcdic["params"][j]}){funcdic["descrip"][j]}'

    return f'\n{func_head_string}{descrp_string}'

# 自定义函数的实现
def func_model(if_model_flag, while_model_flag, switch_model_flag, func_call_string_array, tablevel,func_dic):

    if_string = ""
    if if_model_flag == 1:
        if_string = if_model()
    
    while_string = ""
    if while_model_flag == 1:
        while_string = while_model()

    switch_string = ""
    if switch_model_flag == 1:
        switch_string = switch_model()

    func_call_string = ""
    for item in func_call_string_array:
        func_call_string_item = system_func_call_model(str(item).strip('\n'), tablevel)
        if func_call_string_item is None:
            func_call_string_item = " "
        func_call_string = f'{func_call_string}{func_call_string_item}'

    if func_call_string == "":
        func_call_string = " "
    
    func_head_string = constom_func_head_model(func_dic)
    func_create_string = f'{func_head_string}{{\n{if_string}{while_string}{switch_string}{func_call_string}}}'
        
    return f'\n{func_create_string}\n'

def while_model():

    while_string = "\n\twhile(0){\n\t\tNSLog(@\"滚滚滚滚\");\n\t}\n"
    return while_string