#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import getpass


def run(str_command):
    print str_command
    os.system(str_command)


def main():
    s = requests.Session()
    if len(sys.argv) == 1:
        theme_name = raw_input("Please enter theme name: ")
    elif len(sys.argv) == 2:
        theme_name = sys.argv[1]
    else:
        print u"error param"
        return

    manager_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    file_theme_config = os.path.join(manager_dir, "theme_%s.json" % theme_name)
    try:
        with open(file_theme_config, "r+") as f:
            theme_config = json.load(fp=f)
    except IOError:
        theme_config = {
            "host": raw_input("server host: "),
            "account": raw_input("account: "),
        }
        j = json.dumps(theme_config, indent=4)
        with open(file_theme_config, "w") as f:
            f.write(j)
    password = getpass.getpass("password: ")
    try:
        r = s.post("%s/admin/login.json" % (theme_config["host"]), data={
            "account": theme_config["account"],
            "password": password
        })
        rn = json.loads(r.text)
        if rn["is_login"] == "false":
            print "account error"
            return
        pass
    except:
        print "server error"
        return
    theme_information = {
        "theme_title": "",
        "theme_name": theme_name,
        "exclusive": "all",
        "author": "",
        "using": ""
    }

    themes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", 'themes', theme_name)
    os.chdir(themes_dir)
    file_theme_information = os.path.join(themes_dir, "theme.json")
    try:
        with open(file_theme_information, "r+") as f:
            theme_information.update(json.load(fp=f))
            theme_information["theme_title"] = theme_information["name"]
    except IOError:
        pass
    print theme_information
    r = s.post("%s/admin/themes/upload" % (theme_config["host"]), data=theme_information)
    theme_path = "\\themes\\" + theme_name
    for root_path, _, files in os.walk(themes_dir):
        for file_name in files:
            if file_name.endswith(".html") or file_name.endswith(".js") or file_name.endswith(".css"):
                path = "/".join((theme_path + root_path.replace(themes_dir, "") + "\\" + file_name).split("\\"))
                print "upload:  " + path
                with open(os.path.join(root_path, file_name), 'r') as content_file:
                    content = content_file.read()
                    r = s.post("%s/admin/code/upload" % (theme_config["host"]), data={
                        "code": content,
                        "path": path
                    })
                    print "return:  " + r.text

if __name__ == "__main__":
    main()