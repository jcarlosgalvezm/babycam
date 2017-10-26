#!/usr/bin/env python3
import yaml

with open('config.yml', 'r', encoding='utf-8') as yml:
    cfg = yaml.safe_load(yml)

print('BabyCam CFG - 1/3 - Insert the baby name:')
cfg['usercfg']['babyname'] = input()

print('BabyCam CFG - 2/3 - Insert the Instapush appid:')
cfg['usercfg']['instapush']['appid'] = input()

print('BabyCam CFG - 3/3 - Insert the Instapush secret key:')
cfg['usercfg']['instapush']['secret'] = input()

print(cfg)

with open('config.yml', 'w', encoding='utf-8') as yaml_file:
    yaml.dump(cfg, yaml_file, default_flow_style=False)

print('Config done!')
