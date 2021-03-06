import os
import json
import re

dep_tailfix = ".jar"
jar_prefix = "vwvo-runnable"
jar_tailfix = "vwvo-executable.jar"
ext_tailfix = "vwvo-extension.jar"
war_prefix = "vwvo-runnable"
war_tailfix = ".war"

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


def get_config(configPath):
    pt = os.path.dirname(os.path.abspath(__file__)) + "/" + configPath

    return json.load(file(pt))


def modify_root_config(file_path, default_config_type):
    j = json.load(file(file_path))
    j["defaultType"] = default_config_type

    with open(file_path, "w") as out_file:
        json.dump(j, out_file, indent=4, sort_keys=False)


def get_jar(path):
    if not os.path.isdir(path):
        return None
    for f in os.listdir(path):
        if f.endswith(jar_tailfix):
            return os.path.abspath(os.path.join(path, f))
    return


def get_dependencies(path):
    deps = []
    if not os.path.isdir(path):
        return deps
    for f in os.listdir(path):
        if f.endswith(dep_tailfix) and f.startswith(jar_prefix):
            deps.append(os.path.abspath(os.path.join(path, f)))
    return deps


def get_war(path):
    if not os.path.isdir(path):
        return None
    for f in os.listdir(path):
        if f.endswith(war_tailfix) and f.startswith(war_prefix):
            return os.path.abspath(os.path.join(path, f))
    return None


def get_ext(path):
    if not os.path.isdir(path):
        return None
    for f in os.listdir(path):
        if f.endswith(ext_tailfix):
            return os.path.abspath(os.path.join(path, f))
    return None


def get_project_paths(root_path):
    paths = []
    for root, dirs, files in os.walk(root_path):
        if not os.path.basename(root).startswith("vwvo-runnable"):
            continue
        dirs[:] = [dd for dd in dirs if dd.startswith("vwvo-runnable")]

        if len(dirs) == 0:
            paths.append(root)
    return paths


def match_regexs(regexs, str):
    for regex in regexs:
        p = re.compile(regex)
        if p.match(str):
            return True

    return False


def match_projects(projects, file_path):
    for project in projects:
        if os.path.basename(file_path).startswith(project):
            return True

    return False

