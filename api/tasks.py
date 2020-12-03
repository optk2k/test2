import datetime

import openpyxl as openpyxl
from celery import shared_task
from api.models import FileProcessing


def find_in_sheet(sheet):
    """поиск в листах"""
    # находим нужные колонки
    col_name = col_name2 = None
    for i in sheet['1']:
        if i.value == "before":
            col_name = i.column_letter
        if i.value == "after":
            col_name2 = i.column_letter
        if i.value is None:
            break
    # проверка, если колонки
    if col_name is None or col_name2 is None:
        return False

    # собираем данные из колонок
    col_data = []
    for i in sheet[f'{col_name}']:
        if i.value is not None:
            col_data.append(i.value)
        else:
            break
    col_data2 = []
    for i in sheet[f'{col_name2}']:
        if i.value is not None:
            col_data2.append(i.value)
        else:
            break

    # проверка есть ли данные в колонках
    if len(col_data) < 3 or len(col_data2) < 3:
        return False

    # находим большую и меньшую колонки
    comp = {len(col_data): col_data, len(col_data2): col_data2}
    comp_res = max(comp), min(comp)

    # возвращаем несовпадения (находим наше Х)
    for i in comp[comp_res[1]][1:]:
        comp[comp_res[0]].remove(i)

    result = comp[comp_res[0]]
    if len(result) == 2:
        return comp[comp_res[0]]
    else:
        return False


def choice(x):
    """подстановка на основе заголовков"""
    if x[0] == "before":
        return f"added: {x[1]}"
    if x[0] == "after":
        return f"removed: {x[1]}"


def find_x(file_id):
    """"проходим по листам"""

    FileProcessing.objects.filter(id=file_id).update(status="processing")
    file_name = FileProcessing.objects.get(pk=file_id)
    file = file_name.filename.file

    wb = openpyxl.load_workbook(file)
    for point in enumerate(wb.sheetnames):
        wb.active = point[0]
        sheet = wb.active
        result = find_in_sheet(sheet)
        if bool(result):
            FileProcessing.objects.filter(id=file_id).update(
                status="done",
                date_time_end=datetime.datetime.now(),
                result=choice(result))
            # return



@shared_task
def find_data(file_id):
    find_x(file_id)