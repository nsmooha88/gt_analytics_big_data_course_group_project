#!/bin/sh
cd ./app
var_path=$PWD
echo $var_path
python flask_app.py
