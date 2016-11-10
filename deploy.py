#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/11/9


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import sys


def run(str_command):
    print str_command
    os.system(str_command)

project_config_file = "project"
if len(sys.argv) == 2:
    project_config_file = sys.argv[1]
dir_web = os.path.join(os.path.dirname(os.path.abspath(__file__)))
file_project_config = os.path.join(dir_web, "%s.json" % project_config_file)

try:
    with open(file_project_config , "r+") as f:
        project_config = json.load(fp=f)
except IOError:
    project_config = {
        "id": raw_input("Please enter Project name: "),
        "version": raw_input("Please enter version: ")
    }
    j = json.dumps(project_config, indent=4)
    with open(file_project_config, "w") as f:
        f.write(j)


def deploy(project_id="argeweb-framework", project_version= "2016"):
    dir_web = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",  "..")
    file_app_yaml = os.path.join(dir_web, "app.yaml")
    os.chdir(dir_web)
    line_list = []
    with open(file_app_yaml) as f:
        for line in f:
            if line.find("ssl") > 0:
                line_list.append("- name: ssl\n")
                line = "  version: latest\n"
            line_list.append(line)
    with open(file_app_yaml, 'w+') as f:
        for line in line_list:
            f.write(line)
    print file_app_yaml

    # run ("gcloud app deploy app.yaml --project argeweb-framework")
    run("appcfg.py update . -A %s -V %s" %(project_id, project_version))

    is_ssl = False
    with open(file_app_yaml, 'w+') as f:
        for line in line_list:
            if is_ssl:
                is_ssl = False
                line = "#ssl\n"
            if line.find("name: ssl") > 0:
                is_ssl = True
                continue
            f.write(line)
os.chdir(dir_web)
deploy(project_config["id"], project_config["version"])