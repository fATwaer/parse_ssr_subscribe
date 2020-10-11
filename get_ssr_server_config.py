#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2012-2020 fatwaer

from blessed import Terminal
from yaml import load, dump
from yaml import Loader, Dumper
import parse
import os
import time

DEBUG=False

def loop():
    term = Terminal()

    print(f"{term.home}{term.clear}")
    data = parse.parse_feed(parse._CONFIG['subscribe_url'])
    if data != None:
        parse.save_servers_to_json(data, parse._CONFIG['servers_path'])
    begin_postion = term.get_location()
    # print(begin_postion)
    # time.sleep(1000)
    # print(data)
    for idx, s in enumerate(data):
        print("%2d: %s (%s:%s)"%(idx, s['remarks'], s['server'], s['server_port']))

    print(term.yellow+"press 'q' to quit. press 'Enter' to select server config."+term.normal)
    
    cur = 0
    print(term.move_xy(0, begin_postion[0]+cur), end='')
    print(term.orangered+"%2d: %s (%s:%s)"%(cur, data[cur]['remarks'], data[cur]['server'], data[cur]['server_port'])+term.normal, flush=True, end='')

    with term.cbreak():
        val = ''
        while val.lower() != 'q':
            val = term.inkey(10)
            if not val: 
                continue
         
            if val.is_sequence and val.code == term.KEY_DOWN:
                if cur == len(data)-1:
                    continue
                # clean
                print(term.move_xy(0, begin_postion[0]+cur), end='')
                print("%2d: %s (%s:%s)"%(cur, data[cur]['remarks'], data[cur]['server'], data[cur]['server_port']))
                # nextline
                cur += 1
                print(term.move_xy(0, begin_postion[0]+cur), end='')
                print(term.orangered+"%2d: %s (%s:%s)"%(cur, data[cur]['remarks'], data[cur]['server'], data[cur]['server_port'])+term.normal, flush=True, end='')
          
            if val.is_sequence and val.code == term.KEY_UP:
                if cur == 0:
                    continue
                # clean
                print(term.move_xy(0, begin_postion[0]+cur), end='')
                print("%2d: %s (%s:%s)"%(cur, data[cur]['remarks'], data[cur]['server'], data[cur]['server_port']))
                # nextline
                cur -= 1
                print(term.move_xy(0, begin_postion[0]+cur), end='')
                print(term.orangered+"%2d: %s (%s:%s)"%(cur, data[cur]['remarks'], data[cur]['server'], data[cur]['server_port'])+term.normal, flush=True, end='')

            if val.is_sequence and val.code == term.KEY_ENTER:
                parse._CONFIG['server_name'] = data[cur]['remarks']
                parse._CONFIG['ssr_config_path'] = 'config.json'  
                print(term.move_xy(0, begin_postion[0]+len(data)+1)+term.clear_eol, end='', flush=True)
                json_string = parse.gen_json_config_by_server_name(parse._CONFIG)
                break;

            if DEBUG is True:
                print(term.move_xy(0, begin_postion[0]+len(data)+1)+term.clear_eol, end='', flush=True)
                if val.is_sequence:
                   print("got sequence: {0}.".format((str(val), val.name, val.code)), end='', flush=True)
                elif val:
                   print("got {0}.".format(val), end='', flush=True)
        print(f'bye!{term.normal}')

def parse_yaml():
    with open('default.yaml', 'a+') as f:
        f.seek(0, 0)
        yaml_data = f.read()
    data = load(yaml_data, Loader=Loader)
    return data 

def save_yaml(data):
     with open('default.yaml', 'w+') as f:
        f.write(dump(data))

def get_new_yaml():
    yaml = {}
    print('please input your ssr subscribe url:', end='')
    yaml['ssr_url'] = input()
    print('please input your ssr server info path(dafault=./ssr_server_info.json):', end='')
    info_path = input()
    if (len(info_path) == 0):
        info_path = 'ssr_server_info.json'
    yaml['info_path'] = info_path
    save_yaml(yaml)
    return yaml

def list_info(yaml):
    parse._CONFIG['subscribe_url'] = yaml['ssr_url']
    parse._CONFIG['servers_path'] = yaml['info_path']
    
    try:
        f = open(yaml['info_path'], 'w+')
        f.close()
    except Exception as e:
        os.remove("default.yaml")
        print(e)
    loop()

def main():
    yaml = parse_yaml()
    if yaml is None:
        print('It seems that this is first use...')
        yaml = get_new_yaml()
    list_info(yaml)


if __name__ == "__main__":
    main()
