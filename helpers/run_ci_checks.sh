#!/usr/bin/env bash

default_python_version='3.8'

if [[ $1 == '-h' || $1 == '--help' ]];then
  echo "Run the GitLab CI checks locally to detect any problems."
  echo "Run the script from the root directory of your python code:"
  echo ""
  echo "    ./helpers/run_ci_checks.sh"
  echo ""
  exit 0
fi

python_version=${1-$default_python_version}
eval "python${python_version} --version &>> /dev/null"
if [ $? -ne 0 ]; then
  echo "python${python_version} was not found and is required for initializing this project. Please install python${python_version}"
  echo "Aborting CI checks :("
  exit 1
fi

start=$(date +%s)
echo "$(date +"%Y/%m/%d-%H:%M:%S"): Running all GitLab CI checks (using $(eval 'which python${python_version}'))"
passed=1

. venv/bin/activate
SOURCE=$(dirname "${BASH_SOURCE[0]}")

# Black code formatting
cmd_black="black . --line-length=120 &>> /dev/null"
eval "$cmd_black"
if [ $? -eq 0 ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): black ran successfully"
else
  passed=0
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): black failed (command launched: ${cmd_black/ &>> \/dev\/null/})"
fi

# Isort import sorting
cmd_isort="isort . --filter-files --profile=black --line-length=120 &>> /dev/null"
eval "$cmd_isort"
if [ $? -eq 0 ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): isort ran successfully"
else
  passed=0
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): isort failed (command launched: ${cmd_isort/ &>> \/dev\/null/})"
fi

# Autoflake
cmd_autoflake="autoflake . --in-place --remove-all-unused-imports --remove-unused-variables --expand-star-imports --ignore-init-module-imports &>> /dev/null"
eval "$cmd_autoflake"
if [ $? -eq 0 ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): autoflake ran successfully"
else
  passed=0
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): autoflake failed (command launched: ${cmd_autoflake/ &>> \/dev\/null/})"
fi

# Mypy type hints checks
python_lib="${SOURCE}/../venv/lib/python${python_version}/site-packages"
if [ ! -d ${python_lib}/fountainpy-stubs ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): Generating stubs for fountainpy..."
  stubgen ${python_lib}/fountainpy &>/dev/null && mv out/fountainpy ${python_lib}/fountainpy-stubs && rm -r out
fi

cmd_mypy="mypy . --config config/mypy.ini --follow-imports=skip &>> /dev/null"
eval "$cmd_mypy"
if [ $? -eq 0 ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): mypy check completed successfully"
else
  passed=0
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): mypy failed (command launched: ${cmd_mypy/ &>> \/dev\/null/})"
fi

# Pylint linter
cmd_pylint="pylint \$(git ls-files '*.py') --rcfile config/pylint.ini &>> /dev/null"
eval "$cmd_pylint"
if [ $? -eq 0 ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): pylint check completed successfully"
else
  passed=0
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): pylint failed (command launched: ${cmd_pylint/ &>> \/dev\/null/})"
fi

# Bandit security checks
cmd_bandit="bandit -r ./ --exclude ./venv --recursive --configfile config/bandit.yml &>> /dev/null"
eval "$cmd_bandit"
if [ $? -eq 0 ]; then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): bandit security checks completed successfully"
else
  passed=0
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): bandit security checks failed (command launched: ${cmd_bandit/ &>> \/dev\/null/})"
fi

end=$(date +%s)
runtime=$((end-start))
if [ $passed -eq 1 ];then
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): All good! :) Total execution took ${runtime}s."
else
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): Some problems were found. Please fix them before merging your changes, don't forget to activate your virtual environment."
  echo "$(date +"%Y/%m/%d-%H:%M:%S"): Total execution took ${runtime}s."
fi
