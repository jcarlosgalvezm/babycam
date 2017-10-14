#!/usr/bin/env python3
import yaml

with open('config.yml') as yml:
    cfg = yaml.safe_load(yml)

print(cfg)

print('Config done!')
