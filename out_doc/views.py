import os
import json
import shutil
import string
from zipfile import ZipFile
from django.http import FileResponse
from django.shortcuts import render, redirect
from .models import Dog
from .models import Breed
from .models import Event
from .models import Type
from .models import Rank
from .models import Participant
from .models import DogClass
from docxtpl import DocxTemplate
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import Alignment
import datetime as dt
from pathlib import Path
from .doc_prep import *



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

templates_path = BASE_DIR / 'out_doc/templates/out_doc/'
save_dir = BASE_DIR / 'saved_documents/'



# # Функция печати временных сертификатов
# def print_temp_sertif(events, temp_path, project_name):

#     test_doc_prep()

#     # Загрузка документа
#     template_name = 'временный сертификат.docx'
#     template_file = templates_path / template_name

#     for event in events:
        
#         save_path = temp_path / project_name / ('Тестирование ' + event['rank'] + ' ' + event['comment'] + '/')
    
#         if not os.path.exists(BASE_DIR / save_path):
#             os.makedirs(BASE_DIR / save_path)  # Создание пути сохранения файла

#         dogs_list = event['participants_data']
#         for i in range(len(dogs_list)):

#             doc = DocxTemplate(template_file)

#             dogie = dogs_list[i]

#             sex = '{} \ {}'.format(dogie['sex_ru'], dogie['sex_en'])

#             # Подстановка данных
#             context = {
#                 'name': dogie['name'],
#                 'sex': sex,
#                 'tattoo': dogie['tattoo'],
#                 'rkf': dogie['rkf'],
#                 'birth': dogie['birth_date'],
#                 'owner': dogie['owner'],
#                 'breed': dogie['breed']
#             }
#             doc.render(context)

#             # Сохранение документа
#             save_file = save_path / (dogs_list[i]['tattoo'] + '.docx')
#             doc.save(save_file)

#     return



# # Создание каталогов для каждого события отдельно
# def create_events_catalogs(events, temp_path, project_name):

#     # Оформление документа
#     doc_font_name = 'Times New Roman'
#     doc_font_size = 12
#     doc_width = 85

#     # Оформление группы fci
#     font_fci = Font(
#         name=doc_font_name,
#         size=16,
#         bold=True,
#     )

#     alignment_fci = Alignment(
#         horizontal='center',
#         # vertical='bottom',
#         # text_rotation=0,
#         # wrap_text=False,
#         # shrink_to_fit=False,
#         # indent=0
#     )

#     # Оформление породы
#     font_breed = Font(
#         name=doc_font_name,
#         size=doc_font_size,
#         bold=True,
#     )

#     alignment_breed = Alignment(
#         horizontal='center',
#         wrap_text=True,
#         vertical='top',
#         # vertical='bottom',
#         # text_rotation=0,
#         # wrap_text=False,
#         # shrink_to_fit=False,
#         # indent=0
#     )

#     # Оформление пола
#     font_sex = Font(
#         name=doc_font_name,
#         size=doc_font_size,
#         bold=True,
#         italic=True,
#     )

#     # Оформление класса
#     font_class = Font(
#         name=doc_font_name,
#         size=doc_font_size,
#         bold=True,
#         underline='single',
#     )

#     # Оформление записи собаки
#     font_dogie = Font(        
#         name=doc_font_name,
#         size=doc_font_size,
#     )
    
#     alignment_dogie = Alignment(
#         wrap_text=True,
#         vertical='top',
#     )



#     for event in events:

#         # Создание чистого Excel документа
#         wb = Workbook()
#         # Делаем единственный лист активным
#         ws = wb.active

#         ws.column_dimensions['A'].width = doc_width

#         # Путь сохранения нового каталога
#         save_path = temp_path / project_name
        
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)  # Создание пути сохранения файла

#         save_path = save_path / ('Каталог ' + event['rank'] + ' ' + event['comment'] + '.xlsx')


        
#         dogs_list = event['participants_data']

#         current_fci = ''
#         current_breed = ''
#         current_sex = ''
#         current_class = ''
#         current_line = 1

#         for i in range(len(dogs_list)):
#             fci = dogs_list[i]['fci']
#             dog_id = dogs_list[i]['dog_id']
#             dog_obj = Dog.objects.filter(id=dog_id).first()
#             participant_id = dogs_list[i]['participant_id']
#             breed_obj = Breed.objects.filter(id=dog_obj.breed_id).first()
#             parts_object = Participant.objects.filter(id=participant_id).first()
#             class_obj = DogClass.objects.filter(id=parts_object.class_id).first()
            
#             if fci != current_fci:
#                 current_line += 1
#                 current_fci = fci
#                 value = str(current_fci) + ' ГРУППА F.C.I.'
#                 cell = 'A' + str(current_line)
#                 current_line += 2
#                 ws[cell] = value
#                 ws[cell].font = font_fci
#                 ws[cell].alignment = alignment_fci

#             name_ru = breed_obj.name_ru
#             country_ru = breed_obj.country_ru
#             name_en = breed_obj.name_en
#             country_en = breed_obj.country_en
#             breed_str = '{} ({}) \ {} ({})'.format(name_ru, country_ru, name_en, country_en)

#             if breed_str != current_breed:
#                 current_breed = breed_str
#                 cell = 'A' + str(current_line)
                
#                 ws[cell] = current_breed
#                 ws[cell].font = font_breed
#                 ws[cell].alignment = alignment_breed
#                 ws.row_dimensions[current_line].auto_size = True
#                 current_line += 2

#             sex_str = 'СУКИ \ FEMALES'
#             if dog_obj.is_male == True:
#                 sex_str = 'КОБЕЛИ \ MALES'

#             if sex_str != current_sex:
#                 current_sex = sex_str
#                 cell = 'A' + str(current_line)
#                 current_line += 2
#                 ws[cell] = current_sex
#                 ws[cell].font = font_sex

#             class_str = 'Класс: {} \ {} class'.format(class_obj.name_ru, class_obj.name_en.capitalize())

#             if class_str != current_class:
#                 current_class = class_str
#                 cell = 'A' + str(current_line)
#                 current_line += 2
#                 ws[cell] = current_class
#                 ws[cell].font = font_class

#             dogie_str = ''
#             dogie_str += str(dogs_list[i]['npp']) + '. '
#             dogie_str += dogs_list[i]['name'] + ', '
#             dogie_str += 'д.р. ' + dogs_list[i]['birth_date'] + ', '
#             dogie_str += dogs_list[i]['tattoo'] + ', '

#             colour_str = dog_obj.colour_ru
#             if colour_str == '-':
#                 colour_str = dog_obj.colour_en
#             dogie_str += colour_str + ', '

#             # Разобраться с вводом родителей собаки

#             # father_obj = Dog.objects.filter(tattoo=dog_obj.father_tattoo).first()
#             # mother_obj = Dog.objects.filter(tattoo=dog_obj.mother_tattoo).first()

#             # father_name = father_obj.name_ru
#             # if father_name == '-':
#             #     father_name = father_obj.name_en

#             # mother_name = mother_obj.name_ru
#             # if mother_name == '-':
#             #     mother_name = mother_obj.name_en

#             # dogie_str += father_name + 'X' + mother_name + ', '

#             dogie_str += 'зав. ' + dog_obj.breeder + ', '
#             dogie_str += 'вл. ' + dog_obj.owner



#             cell = 'A' + str(current_line)
#             current_line += 2
#             ws[cell] = dogie_str
#             ws[cell].font = font_dogie
#             ws[cell].alignment = alignment_dogie

        
#         wb.save(save_path)
#         del wb



# # Создание отчётов на каждое событие
# def create_events_reports(events, temp_path, project_name):
    
#     print('Создание отчётов')

#     for event in events:

#         # Путь сохранения нового отчёта
#         save_path = temp_path / project_name
        
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)  # Создание пути сохранения файла

#         save_path = save_path / ('Отчёт ' + event['rank'] + ' ' + event['comment'] + '.xlsx')

#         # Создание чистого Excel документа
#         wb = Workbook()

#         # Делаем единственный лист активным
#         ws = wb.active

#         # Вставка заголовка отчёта
#         ws['B2'] = 'ИТОГОВЫЙ ОТЧЕТ'

#         ws['B4'] = 'Название кинологической организации'
#         ws['E4'] = 'МЕЖРЕГИОНАЛЬНАЯ ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ КЛУБ ПЛЕМЕННОГО СОБАКОВОДСТВА "КРАСНЫЙ МАЯК"'

#         ws['B5'] = 'Название выставки'
#         ws['E5'] = 'СЕРТИФИКАТНАЯ ВЫСТАВКА "КРАСНЫЙ МАЯК"'

#         ws['B6'] = 'Дата проведения'
#         event_date = event['date']
#         ws['E6'] = str(event_date)

#         ws['B7'] = 'Город'
#         ws['E7'] = 'МОСКВА'

#         ws['B8'] = 'Ранг выставки'
#         ws['E8'] = event['rank']


#         # Сохранение текущего отчёта
#         wb.save(save_path)
#         del wb 



# Функция получения списка событий
def get_events_list(selected_events = []):

    if type(selected_events) == type(1):
        selected_events = [selected_events]

    len_selected_events = len(selected_events)

    # Получение объектов событий
    events_objects = Event.objects.order_by('-date')

    # Получение объектов типов событий
    types = Type.objects.all()
    types_names = []
    for el in types:
        types_names.append(el.name)

    # Получение объектов рангов событий
    ranks = Rank.objects.all()
    ranks_names = []
    for el in ranks:
        ranks_names.append(el.name)

    # Составление списка событий
    events_list = []
    for el in events_objects:

        # Если есть выбранные события и текущее событие не выбрано
        # Тогда переходим к следующему событию
        if len_selected_events > 0 and el.id not in selected_events:
            continue

        event = {}
        event['id'] = el.id

        if el.org_id == 0:
            event['org'] = 'Красный маяк'

        event['type'] = Type.objects.filter(id=el.type_id).first().name
        event['rank'] = Rank.objects.filter(id=el.rank_id).first().name
        event['date'] = el.date
        event['comment'] = el.comment
        events_list.append(event)

    return events_list



# Получение данных собак-участниц по скиску событий 
def get_participants_data(selected_events_id):

    if type(selected_events_id) != type([]):
        selected_events_id = [selected_events_id]
    
    parts_object = Participant.objects.all()

    dogs_list = []
    for el in parts_object:

        if el.event_id not in selected_events_id:
            # Отбор участников выбранных событий
            continue

        dogie = {}
        dog_obj = Dog.objects.filter(id=el.dog_id).first()
        breed_obj = Breed.objects.filter(id=dog_obj.breed_id).first()
        class_obj = DogClass.objects.filter(id=el.class_id).first()

        dogie['fci'] = breed_obj.group
        dogie['breed_ru'] = breed_obj.name_ru
        dogie['breed_en'] = breed_obj.name_en
        dogie['judge'] = '-'
        dogie['ring'] = '-'
        
        if dog_obj.is_male == True:
            dogie['sex_ru'] = 'Кобель'
            dogie['sex_en'] = 'Male'
        else:
            dogie['sex_ru'] = 'Сука'
            dogie['sex_en'] = 'Female'
        
        dogie['class_id'] = class_obj.id
        dogie['class_ru'] = class_obj.name_ru
        dogie['class_en'] = class_obj.name_en
        dogie['npp'] = 0
        dogie['dog_id'] = dog_obj.id
        dogie['participant_id'] = el.id

        dogie['name'] = dog_obj.name_ru
        if dogie['name'] == '-' or dogie['name'] == '':
            dogie['name'] = dog_obj.name_en

        dogie['tattoo'] = dog_obj.tattoo
        dogie['rkf'] = dog_obj.rkf


        dogie['birth_date'] = dog_obj.birth_date.strftime("%d.%m.%Y")
        dogie['owner'] = dog_obj.owner
        dogie['breed'] = dog_obj.breeder

        dogs_list.append(dogie)


    # Сортировка собак
    dogs_list.sort(key=lambda dogie: dogie['name'])
    dogs_list.sort(key=lambda dogie: dogie['class_id'])
    dogs_list.sort(key=lambda dogie: dogie['sex_ru'])
    dogs_list.sort(key=lambda dogie: dogie['breed_ru'])
    dogs_list.sort(key=lambda dogie: dogie['fci'])

    # Удаление повторяющихся собак с одинаковыми классами
    for i in range(len(dogs_list) - 1, 0, -1):
        dogie = dogs_list[i]
        prev_dogie = dogs_list[i - 1]
        # print(dogie['dog_id'])
        if dogie['dog_id'] == prev_dogie['dog_id']:
            if dogie['class_id'] == prev_dogie['class_id']:
                dogs_list.pop(i)

    # Проставление порядковых номеров в каталоге
    for i in range(len(dogs_list)):
        dogs_list[i]['npp'] = (i + 1)

    return dogs_list



# Получение списка ранее созданных проектов
def get_existing_projects():

    json_path = BASE_DIR / 'projects.json'
    
    # Загрузка записей о проектах
    json_path = BASE_DIR / 'projects.json'
    with open(json_path, 'r', encoding='utf8') as projects_file:
        projects = json.load(projects_file)

    return projects



# Открытие существующего проекта по пути json файла
# def open_project(project_path):  # TODO

    
#     # Загрузка записей о проектах
#     json_path = BASE_DIR / 'projects.json'
#     with open(json_path, 'r', encoding='utf8') as projects_file:
#         projects = json.load(projects_file)    


#     project_file = open(project_path)
#     project = json.load(project_file)
#     events_id = project['events_id']
#     project_file.close()

#     events_id_str = [str(el) for el in events_id]
#     project = {
#         'events_id': events_id,
#     }
#     for el in events_id:

#         # Сбор данных об участниках
#         project.setdefault(el, {})
#         project[el].setdefault('participants_data', [])
#         project[el]['participants_data'] = get_participants_data(el)

#         # Сбор данных о событии
#         event_data = get_events_list(el)[0]
#         project[el]['id'] = el
#         project[el]['org'] = event_data['org']
#         project[el]['type'] = event_data['type']
#         project[el]['rank'] = event_data['rank']
#         project[el]['date'] = event_data['date'].strftime("%d.%m.%Y")
#         project[el]['comment'] = event_data['comment']


#     with open(project_path, 'w') as outfile:
#         json.dump(
#             project, 
#             outfile, 
#             ensure_ascii=False, 
#             indent=4
#         )


#     project_file = open(project_path)
#     project = json.load(project_file)

#     return project



def rename_project(request, project_id):    
    # Запрос переименования проекта

    if request.method == 'POST':

        button = request.POST.get("btn")

        if button == 'rename_project':

            new_name = request.POST.get("project_new_name")
            projects = []

            # Загрузка записей о проектах
            json_path = BASE_DIR / 'projects.json'
            with open(json_path, 'r', encoding='utf8') as projects_file:
                projects = json.load(projects_file)

            # Поиск и переименование проекта по id
            for i in range(len(projects)):
                pr = projects[i]
                if pr['id'] == project_id:
                    projects[i]['name'] = new_name
                    break

            # Перезапись projects.json
            with open(json_path, 'w', encoding='utf8') as outfile:
                json.dump(
                    projects, 
                    outfile, 
                    ensure_ascii=False, 
                    indent=4
                )

            # return redirect('out_doc_edit_project', project_id = project_id)
            

    return redirect('out_doc_edit_project', project_id = project_id)



# def rename_project_func(old_name, new_name):

#     print(
#         {old_name},
#         {new_name},
#         sep='\n',
#     )

#     # Предварительно убираем все знаки препинания из нового имени
#     # Кроме точек
#     punct = string.punctuation
#     punct = punct.replace('.', '')
#     # new_name = request.POST.get("project_new_name")
#     new_name = new_name.translate(str.maketrans('', '', punct))
#     old_path = BASE_DIR / ('projects/' + old_name + '.json')
#     new_name = BASE_DIR / ('projects/' + new_name + '.json')

#     os.rename(old_path, new_name)
#     return



def delete_project(request, project_id):    
    # Запрос удаления проекта

    projects = []

    # Загрузка записей о проектах
    json_path = BASE_DIR / 'projects.json'
    with open(json_path, 'r', encoding='utf8') as projects_file:
        projects = json.load(projects_file)

    # Поиск и удаление проекта по id
    for i in range(len(projects)):
        pr = projects[i]
        if pr['id'] == project_id:
            del projects[i]
            break

    # Перезапись projects.json
    with open(json_path, 'w', encoding='utf8') as outfile:
        json.dump(
            projects, 
            outfile, 
            ensure_ascii=False, 
            indent=4
        )


    return redirect('out_doc_select_project')



def load_project(events_id):
    # Загрузка проекта из БД
    # Вход: [int, .., int] список id событий
    # Выход: 
    #   {
            # 'events_id': events_id,  список id событий
            # event_id : {
                # 'participants_data': [данные собак участниц]
            # }
    #   }

    project = {
        'events_id': events_id,
    }

    for el in events_id:

        # Сбор данных об участниках
        project.setdefault(el, {})
        project[el].setdefault('participants_data', [])
        project[el]['participants_data'] = get_participants_data(el)

        # Сбор данных о событии
        event_data = get_events_list(el)[0]
        project[el]['id'] = el
        project[el]['org'] = event_data['org']
        project[el]['type'] = event_data['type']
        project[el]['rank'] = event_data['rank']
        project[el]['date'] = event_data['date'].strftime("%d.%m.%Y")
        project[el]['comment'] = event_data['comment']

    return project



def create_project(events_id):
    # Функция создания нового каталога

    
    now = dt.datetime.now()
    yyyy = now.year
    mm = now.month
    dd = now.day
    hour = now.hour
    minutes = now.minute
    seconds = now.second

    json_path = BASE_DIR / 'projects.json'
    project_name = '{}.{}.{}.{}.{}.{}'.format(
        yyyy, mm, dd, hour, minutes, seconds
    )
    projects = []


    # Открытие projects.json
    with open(json_path, 'r', encoding='utf8') as projects_file:
        # Загрузка сведений о проектах
        projects = json.load(projects_file)
        print(projects)
        
        # Создание нового id
        max_project_id = -1
        for pr in projects:

            # Если события повторно собираются в проект
            # то возвращаем id существующего проекта
            if pr['events_id'] == events_id:
                return pr['id']

            if pr['id'] > max_project_id:
                max_project_id = pr['id']

        new_id = max_project_id + 1
        print('new_id', new_id)

    # Создание нового проекта
    new_project = {
        'id': new_id,
        'name': project_name,
        'events_id': events_id,
    }

    # Добавление нового проекта в список проектов
    projects.append(new_project)
    print('projects after', projects)

    # Перезапись projects.json
    with open(json_path, 'w', encoding='utf8') as outfile:
        json.dump(
            projects, 
            outfile, 
            ensure_ascii=False, 
            indent=4
        )

    return new_id



# ----------------------------------------------------------------------------------------
# ОБРАБОТЧИКИ ЗАПРОСОВ



def edit_project(request, project_id):
    # Обработчик формы редактирования проекта

    project_events_id = []
    project_name = str()

    # Загрузка записей о проектах
    json_path = BASE_DIR / 'projects.json'
    with open(json_path, 'r', encoding='utf8') as projects_file:
        projects = json.load(projects_file)

    # Поиск информации нужного проекта
    for project in projects:
        if project['id'] == project_id:
            project_events_id = project['events_id']
            project_name = project['name']


    events_list = get_events_list(project_events_id)
    events = {}
    
    for el in project_events_id:
        events[el] = get_participants_data(el)


    for i in range(len(events_list)):
        current_event = events_list[i]
        current_id = current_event['id']
        current_event['participants_data'] = get_participants_data(current_id)
        events_list[i] = current_event
    

    # Подготовка русских названий пород
    breeds = Breed.objects.all()
    breed_ru_names = []
    for el in breeds:
        breed_ru_names.append(el.name_ru)
    del breeds


    # Формирование списка классов
    classes = DogClass.objects.all()
    classes_names = []
    for el in classes:
        dog_class = {}
        dog_class['id'] = el.id
        dog_class['name'] = el.name_ru + ' / ' + el.name_en
        classes_names.append(dog_class)


    # Формирование списка клейм собак
    dogs = Dog.objects.all()
    dogs_tattoo = []
    for el in dogs:
        dogs_tattoo.append(el.tattoo)


    data = {
        'project_id': project_id,
        'project_name': project_name,
        'events_id': project_events_id,
        'events_list': events_list,
        'events': events,
        'breed_ru_names': breed_ru_names,
        'classes_names': classes_names,
        'dogs_tattoo': dogs_tattoo,
    }
    

    # Удаление старых временных папок
    for root, dirs, files in os.walk(save_dir):
        for dir in dirs:
            shutil.rmtree(root + '/' + dir)
            
            
    return render(request, 'out_doc/edit.html', data)



def create_project_doc(request, project_id):
    # Запрос создания выбранной документации для проекта

    # Обработка входящего post запроса
    if request.method == 'POST':
        
        selected_events = []
        project_name = str()

        
        # Загрузка записей о проектах
        # и загрузка id событий выборанного проекта
        json_path = BASE_DIR / 'projects.json'
        with open(json_path, 'r', encoding='utf8') as projects_file:
            projects = json.load(projects_file)
            for pr in projects:
                if pr['id'] == project_id:
                    selected_events = pr['events_id']
                    project_name = pr['name']


        events = get_events_list(selected_events)


        for i in range(len(events)):
            
            event_id = events[i]['id']
            events[i]['participants_data'] = get_participants_data(event_id)

        # Создание временной папки для подготовки документации
        temp_path = save_dir / str(dt.datetime.now()).replace(':', '.')
        # Создаём каталог, если его ещё нет
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)  # создание каталога

        # Пути проекта
        project_path  = temp_path / project_name
        zip_path  = temp_path / (project_name + '.zip')

        # Проверка запроса временных сертификатов тестирования
        if request.POST.get("temp_sertif_checkbox") == 'on':
            # Создание временных сертификатов тестирования
            print_temp_sertif(events, temp_path, project_name)

        # Проверка запроса каталогов на каждое событие в проекте
        if request.POST.get("events_catalogs_checkbox") == 'on':
            # Создание каталогов на каждое событие
            create_events_catalogs(events, temp_path, project_name)

        # Проверка запроса отчётов на каждое событие в проекте
        if request.POST.get("events_reports_checkbox") == 'on':
            # Создание каталогов на каждое событие
            create_events_reports(events, temp_path, project_name)

        # Проверка запроса закрытого списка учатников excel в проекте
        if request.POST.get("events_parts_private_list_checkbox") == 'on':
            # Создание закрытого списка учатников
            create_private_list(events, temp_path, project_name)

        # Проверка запроса открытого списка учатников excel в проекте
        if request.POST.get("events_parts_open_list_checkbox") == 'on':
            # Создание открытого списка учатников
            create_open_list(events, temp_path, project_name)
        
        # Подготовка документов к отправке
        # Обход готовых файлов проекта
        real_file_path = []
        for root, dirs, files in os.walk(project_path):
            for filename in files:
                real_path = root + '/' + filename
                real_file_path.append(real_path)  

        # Запись файлов в архив
        with ZipFile(zip_path, "w") as myzip:
            for i in range(len(real_file_path)):
                real_file = real_file_path[i]
                zip_file = real_file.replace(str(project_path), '')
                myzip.write(real_file, zip_file)
        
        # Отправка созданного архива в ответ
        zip = open(zip_path, 'rb')
        print('zip_path', zip_path)
        response = FileResponse(zip)

        return response


    return redirect('out_doc_edit_project', project_name = project_name)



def select_project(request):
    # Обработчик формы выбора каталога


    error = ''
    events_list = get_events_list()
    projects_json = get_existing_projects()

    data = {
        'error': error,
        'events': events_list,
        'projects_json': projects_json
    }

    # ___________________________________________________________
    # Обработка входящего пост запроса

    if request.method == 'POST':
        
        # Получение списка выбранных событий для нового каталога
        selected_events_id = []
        for el in events_list:            
            checkbox = 'event ' + str(el['id'])
            if request.POST.get(checkbox):
                selected_events_id.append(el['id'])

        
        button = request.POST.get("btn")

        # Выбрано создание нового каталога
        if button == 'create':

            # Если не выбрано ни одного события
            if selected_events_id == []:            
                error = 'Ошибка: Выберите события для каталога.'
                data['error'] = error
                return render(request, 'out_doc/select.html', data)
            
            else:
                # Запуск создания нового каталога            
                project_id = create_project(selected_events_id)
                error = selected_events_id
                data['error'] = error
                return redirect('out_doc_edit_project', project_id = project_id)

    else:
        selected_events_id = []

    return render(request, 'out_doc/select.html', data)



def main(request):
    
    # Получение списка событий
    events_list = get_events_list()

    # ___________________________________________________________
    # Обработка входящего пост запроса

    if request.method == 'POST':
        selected_events_id = []
        for el in events_list:            
            checkbox = 'event ' + str(el['id'])
            if request.POST.get(checkbox):
                selected_events_id.append(el['id'])
    else:
        selected_events_id = []

    data = {
        'dogs': get_participants_data(selected_events_id),
        'events': events_list,
        'selected_events': selected_events_id
    }

    return render(request, 'out_doc/main.html', data)



def delete_participant(request, participant_id):
    # Запрос на удаление заявки на участие собаки на одной выставке
    # Принимает на вход уникальный id участника
    # Удаляет участника из таблицы участников в БД
    
    Participant.objects.filter(id=participant_id).delete()
    
    return redirect(request.META.get('HTTP_REFERER'))



def project_add_dog(request):
    # Добавление одной собаки в несколько событий в одном проекте.
    

    current_dog_id = -1
    
    current_dog_tattoo = request.POST.get("tattoo")
    result_set = Dog.objects.filter(tattoo=current_dog_tattoo)

    if len(result_set) == 0:
        # Действия если собаки нет в базе
        # Тогда нужно сначала записать собаку в таблицу с собаками
        # а потом по id собаки зарегистрировать её на событиях
        dog = Dog()

        breed_name_ru = request.POST.get("breed")
        breed = Breed.objects.filter(name_ru=breed_name_ru).first()
        dog.breed_id = breed.id

        dog.rkf = request.POST.get("rkf")
        dog.region = request.POST.get("region")
        dog.birth_date = request.POST.get("birth_date")
        dog.is_male = request.POST.get("sex") == 'male'
        dog.tattoo = current_dog_tattoo
        dog.chip = request.POST.get("chip")
        dog.name_ru = request.POST.get("name_ru")
        dog.name_en = request.POST.get("name_en")
        dog.colour_ru = request.POST.get("colour_ru")
        dog.colour_en = request.POST.get("colour_en")
        dog.breeder = request.POST.get("breeder")
        dog.owner = request.POST.get("owner")
        dog.father_tattoo = request.POST.get("father_tattoo")
        dog.mother_tattoo = request.POST.get("mother_tattoo")
        dog.save()

        current_dog_id = Dog.objects.filter(tattoo=current_dog_tattoo).first().id

    else:
        current_dog_tattoo = request.POST.get("tattoo")
        current_dog_id = Dog.objects.filter(tattoo=current_dog_tattoo).first().id
        

    # Получение списка событий
    events_list = get_events_list()
    events_id = []

    for el in events_list:
        
        class_field = 'event ' + str(el['id']) + ' class'        
        current_class = request.POST.get(class_field)

        if current_class != None:

            events_id.append(el['id'])
            
            if current_class != '':

                current_class = current_class.split()[0]
                participant = Participant()

                participant.dog_id = current_dog_id
                participant.event_id = el['id']

                current_class_id = DogClass.objects.filter(name_ru=current_class).first().id
                participant.class_id = current_class_id
                participant.is_pay = False
                
                for cl in DogClass.objects.all():
                    print(cl.name_ru, cl.name_en)

                print(
                    participant.dog_id,
                    participant.event_id,
                    participant.class_id,
                    participant.is_pay,
                    sep='\n',
                )

                participant.save()
                

    return redirect(request.META.get('HTTP_REFERER'))



def get_dog_by_tattoo(request):
    return {
        'status': 'success',
    }