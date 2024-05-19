
import os
import subprocess
from pathlib import Path


version_dict = {}
ROOT = Path(__file__).parent.parent.parent


def change_file(data_path, version):
    """
    Добавление текста в файл. Исключительно для теста
    :param version: тестовая строка с версией
    :param data_path: путь до файла
    """
    if os.path.exists(data_path):
        print(f'Файл {data_path} существует')
    else:
        print(f'Файл {data_path} НЕ существует')
    with open(data_path, "a") as myfile:
        myfile.write(f"\nappended text - {str(version)}")


def read_file(pathfile):
    """
    Чтение файла. Исключительно для теста
    :param pathfile: путь до файла
    :return:
    """
    f = open(pathfile, "r")
    return f.read()


def switch_head(tag):
    """
    Переключение ветки на тег.
    :param tag: наименование тэга
    :return:
    """
    command_1 = f'git checkout "{tag}"'
    command_2 = f'dvc pull'
    print(f"Switching ON {tag}")
    os.system(command_1)
    os.system(command_2)
    if get_current_tag() == tag:
        return f"Switched ON {tag}"
    else:
        return f"Failed switching on {tag}"


def create_new_version():
    """
    Создание новой версии данных. Включая добавление в dvc, git
    :param tag: наименование тэга новой версии данных
    :return:
    """
    if len(get_all_tags()) == 0:
        new_tag = "v0"
        git_1 = 'git config --global user.email "example@mail.com"'
        git_2 = 'git config --global user.name "Test Name"'
        os.system(git_1)
        os.system(git_2)
    else:
        latest_tag = max(get_all_tags())
        new_tag = f"v{int(latest_tag[1:])+1}"
    data_path = os.path.join(ROOT, "data")
    data_dvc_path = os.path.join(ROOT, "data.dvc")
    command_1 = f'dvc add "{data_path}"'
    command_2 = f'git add "{data_dvc_path}"'
    command_3 = f'git commit -a -m "put datasets under control - {new_tag}"'
    command_4 = f'git tag "{new_tag}"'

    os.system(command_1)
    os.system(command_2)
    os.system(command_3)
    os.system(command_4)
    os.system('dvc push')


def get_current_tag():
    """
    Получение текущего тэга
    :return: текущий тэг
    """
    command = 'git describe --tags --abbrev=0'
    cur_ver = subprocess.check_output(command, shell=True).decode('utf-8').replace("\n", "")
    return cur_ver


def parse_tag_info(tag_list):
    """
    Парсинг информации о тэгах
    :param tag_list: список тэгов
    :return: словарь с информацией о тэгах
    """
    tag_dict = {}
    for tag_info in tag_list:
        if "tag" in tag_info:
            tag_info_list = tag_info.split(' ')
            date = tag_info_list[0]
            time = tag_info_list[1]
            tag = tag_info_list[-1].replace(")", "")
            tag_dict[tag] = date + time
    return {key: tag_dict[key] for key in sorted(tag_dict, reverse=True)}


def get_all_tags():
    """
    Получение всех тэгов
    :return: словарь с информацией о тэгах (тэг : время создания)
    """
    command = 'git log --tags --pretty="format:%ci %d"'
    tags = subprocess.check_output(command, shell=True).decode('utf-8').split("\n")
    return parse_tag_info(tags)
