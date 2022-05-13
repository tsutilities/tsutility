#!/usr/bin/env bash

default_python_version='3.8'
if [[ $1 == '-h' || $1 == '--help' ]];then
  echo "Initialize the project by installing its dependencies."
  echo "Run the script from the root directory of your python code (where your 'requirements.txt' file is)."
  echo "It can take one argument:"
  echo ""
  echo "    ./helpers/dev-install.sh <python_version:${default_python_version}>"
  echo ""
  echo "    * python_version: the python version used. Default is python${default_python_version}"
  echo ""
  exit 0
fi

python_version=${2-$default_python_version}
eval "python${python_version} --version &>> /dev/null"
if [ $? -ne 0 ]; then
  echo "python${python_version} was not found and is required for initializing this project. Please install python${python_version}"
  echo "Aborting installation :("
  exit 1
fi

if [ ! -d ./venv ]; then
  echo "Virtual environment directory ./venv/ was not found, creating..."
  eval "python${python_version} -m venv venv"
fi

. venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
  echo "Something went wrong while installing the python dependencies"
fi
