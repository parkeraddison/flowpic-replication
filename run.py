#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src/data')

from collect import get_data

def main(targets):

    if 'data' in targets:
        with open('config/data-generation-params.json') as f:
            generation_params = json.load(f)
            get_data(generation_params)
                  
    return
    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)