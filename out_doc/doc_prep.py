import os

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.styles import Alignment

from pathlib import Path
from docxtpl import DocxTemplate

from .models import Dog
from .models import Breed
from .models import DogClass
from .models import Participant



BASE_DIR = Path(__file__).resolve().parent.parent
templates_path = BASE_DIR / 'out_doc/templates/out_doc/'



# Преобразование даты к строке с сохранение лидирующих нолей
def toDateStr(number):


    str_number = str(number)
    if len(str_number) > 3:
        # Если передан год для преобразования
        return str_number
    if len(str_number) < 2:
        # Передано однозначное число дня или месяца
        str_number = '0' + str_number

    return str_number



# Функция печати временных сертификатов
def print_temp_sertif(events, temp_path, project_name):

    # Загрузка документа
    template_name = 'временный сертификат.docx'
    template_file = templates_path / template_name

    for event in events:
        
        save_path = temp_path / project_name / ('Тестирование ' + event['rank'] + ' ' + event['comment'] + '/')
    
        if not os.path.exists(BASE_DIR / save_path):
            os.makedirs(BASE_DIR / save_path)  # Создание пути сохранения файла

        dogs_list = event['participants_data']
        for i in range(len(dogs_list)):

            doc = DocxTemplate(template_file)

            dogie = dogs_list[i]

            sex = '{} \ {}'.format(dogie['sex_ru'], dogie['sex_en'])

            # Подстановка данных
            context = {
                'name': dogie['name'],
                'sex': sex,
                'tattoo': dogie['tattoo'],
                'rkf': dogie['rkf'],
                'birth': dogie['birth_date'],
                'owner': dogie['owner'],
                'breed': dogie['breed']
            }
            doc.render(context)

            # Сохранение документа
            save_file = save_path / (dogs_list[i]['tattoo'] + '.docx')
            doc.save(save_file)

    return



# Создание каталогов для каждого события отдельно
def create_events_catalogs(events, temp_path, project_name):

    # Оформление документа
    doc_font_name = 'Times New Roman'
    doc_font_size = 12
    doc_width = 85

    # Оформление группы fci
    font_fci = Font(
        name=doc_font_name,
        size=16,
        bold=True,
    )

    alignment_fci = Alignment(
        horizontal='center',
        # vertical='bottom',
        # text_rotation=0,
        # wrap_text=False,
        # shrink_to_fit=False,
        # indent=0
    )

    # Оформление породы
    font_breed = Font(
        name=doc_font_name,
        size=doc_font_size,
        bold=True,
    )

    alignment_breed = Alignment(
        horizontal='center',
        wrap_text=True,
        vertical='top',
        # vertical='bottom',
        # text_rotation=0,
        # wrap_text=False,
        # shrink_to_fit=False,
        # indent=0
    )

    # Оформление пола
    font_sex = Font(
        name=doc_font_name,
        size=doc_font_size,
        bold=True,
        italic=True,
    )

    # Оформление класса
    font_class = Font(
        name=doc_font_name,
        size=doc_font_size,
        bold=True,
        underline='single',
    )

    # Оформление записи собаки
    font_dogie = Font(        
        name=doc_font_name,
        size=doc_font_size,
    )
    
    alignment_dogie = Alignment(
        wrap_text=True,
        vertical='top',
    )



    for event in events:

        # Создание чистого Excel документа
        wb = Workbook()
        # Делаем единственный лист активным
        ws = wb.active

        ws.column_dimensions['A'].width = doc_width

        # Путь сохранения нового каталога
        save_path = temp_path / project_name
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Создание пути сохранения файла

        save_path = save_path / ('Каталог ' + event['rank'] + ' ' + event['comment'] + '.xlsx')


        
        dogs_list = event['participants_data']

        current_fci = ''
        current_breed = ''
        current_sex = ''
        current_class = ''
        current_line = 1

        for i in range(len(dogs_list)):
            fci = dogs_list[i]['fci']
            dog_id = dogs_list[i]['dog_id']
            dog_obj = Dog.objects.filter(id=dog_id).first()
            participant_id = dogs_list[i]['participant_id']
            breed_obj = Breed.objects.filter(id=dog_obj.breed_id).first()
            parts_object = Participant.objects.filter(id=participant_id).first()
            class_obj = DogClass.objects.filter(id=parts_object.class_id).first()
            
            if fci != current_fci:
                current_line += 1
                current_fci = fci
                value = str(current_fci) + ' ГРУППА F.C.I.'
                cell = 'A' + str(current_line)
                current_line += 2
                ws[cell] = value
                ws[cell].font = font_fci
                ws[cell].alignment = alignment_fci

            name_ru = breed_obj.name_ru
            country_ru = breed_obj.country_ru
            name_en = breed_obj.name_en
            country_en = breed_obj.country_en
            breed_str = '{} ({}) \ {} ({})'.format(name_ru, country_ru, name_en, country_en)

            if breed_str != current_breed:
                current_breed = breed_str
                cell = 'A' + str(current_line)
                
                ws[cell] = current_breed
                ws[cell].font = font_breed
                ws[cell].alignment = alignment_breed
                ws.row_dimensions[current_line].auto_size = True
                current_line += 2

            sex_str = 'СУКИ \ FEMALES'
            if dog_obj.is_male == True:
                sex_str = 'КОБЕЛИ \ MALES'

            if sex_str != current_sex:
                current_sex = sex_str
                cell = 'A' + str(current_line)
                current_line += 2
                ws[cell] = current_sex
                ws[cell].font = font_sex

            class_str = 'Класс: {} \ {} class'.format(class_obj.name_ru, class_obj.name_en.capitalize())

            if class_str != current_class:
                current_class = class_str
                cell = 'A' + str(current_line)
                current_line += 2
                ws[cell] = current_class
                ws[cell].font = font_class

            dogie_str = ''
            dogie_str += str(dogs_list[i]['npp']) + '. '
            dogie_str += dogs_list[i]['name'] + ', '
            dogie_str += 'д.р. ' + dogs_list[i]['birth_date'] + ', '
            dogie_str += dogs_list[i]['tattoo'] + ', '

            colour_str = dog_obj.colour_ru
            if colour_str == '-':
                colour_str = dog_obj.colour_en
            dogie_str += colour_str + ', '

            # Разобраться с вводом родителей собаки

            # father_obj = Dog.objects.filter(tattoo=dog_obj.father_tattoo).first()
            # mother_obj = Dog.objects.filter(tattoo=dog_obj.mother_tattoo).first()

            # father_name = father_obj.name_ru
            # if father_name == '-':
            #     father_name = father_obj.name_en

            # mother_name = mother_obj.name_ru
            # if mother_name == '-':
            #     mother_name = mother_obj.name_en

            # dogie_str += father_name + 'X' + mother_name + ', '

            dogie_str += 'зав. ' + dog_obj.breeder + ', '
            dogie_str += 'вл. ' + dog_obj.owner



            cell = 'A' + str(current_line)
            current_line += 2
            ws[cell] = dogie_str
            ws[cell].font = font_dogie
            ws[cell].alignment = alignment_dogie

        
        wb.save(save_path)
        del wb



# Создание отчётов на каждое событие
def create_events_reports(events, temp_path, project_name):
    
    print('Создание отчётов')

    for event in events:

        # Путь сохранения нового отчёта
        save_path = temp_path / project_name
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Создание пути сохранения файла

        save_path = save_path / ('Отчёт ' + event['rank'] + ' ' + event['comment'] + '.xlsx')

        # Создание чистого Excel документа
        wb = Workbook()

        # Делаем единственный лист активным
        ws = wb.active

        # Вставка заголовка отчёта
        ws['B2'] = 'ИТОГОВЫЙ ОТЧЕТ'

        ws['B4'] = 'Название кинологической организации'
        ws['E4'] = 'МЕЖРЕГИОНАЛЬНАЯ ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ КЛУБ ПЛЕМЕННОГО СОБАКОВОДСТВА "КРАСНЫЙ МАЯК"'

        ws['B5'] = 'Название выставки'
        ws['E5'] = 'СЕРТИФИКАТНАЯ ВЫСТАВКА "КРАСНЫЙ МАЯК"'

        ws['B6'] = 'Дата проведения'
        event_date = event['date']
        ws['E6'] = str(event_date)

        ws['B7'] = 'Город'
        ws['E7'] = 'МОСКВА'

        ws['B8'] = 'Ранг выставки'
        ws['E8'] = event['rank']


        # Сохранение текущего отчёта
        wb.save(save_path)
        del wb



# Создание закрытого списка участников для сверки
def create_private_list(events, temp_path, project_name):

    rows = []
    
    # Сбор строк
    for event in events:        

        # Сбор данных о событии
        event_date = event['date']
        event_field = str()
        event_field += event['org'] + ', '
        event_field += event['type'] + ', '
        event_field += event['rank'] + ', '
        event_field += toDateStr(event_date.day) + '.' + toDateStr(event_date.month) + '.' + toDateStr(event_date.year) + ', ' 
        event_field += event['comment']

        # Добавление новой строки в список
        for dogie in event['participants_data']:
            new_row = {}
            new_row['event'] = event_field
            new_row['breed'] = '{} \ {}'.format(dogie['breed_ru'], dogie['breed_en'])
            new_row['class'] = '{} \ {}'.format(dogie['class_ru'], dogie['class_en'])
            new_row['sex'] = '{} \ {}'.format(dogie['sex_ru'], dogie['sex_en'])
            new_row['tattoo'] = dogie['tattoo']
            new_row['owner'] = dogie['owner']
            rows.append(new_row)
            # print(new_row, '\n')

    
    # Сортировка собак по клейму 
    rows = sorted(rows, key=lambda x: x['tattoo'])
        
    # Путь сохранения нового отчёта
    save_path = temp_path / project_name
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # Создание пути сохранения файла

    save_path = save_path / ('Список закрытый для сверки.xlsx')

    # Создание чистого Excel документа
    wb = Workbook()

    # Делаем единственный лист активным
    ws = wb.active

    # Вставка заголовка списка
    ws['A1'] = 'Событие'
    ws['B1'] = 'Порода'
    ws['C1'] = 'Класс'
    ws['D1'] = 'Пол'
    ws['E1'] = 'Клеймо'
    ws['F1'] = 'Владелец'
    current_line = 2

    # Для настройки ширины столбцов
    a_width = 0
    b_width = 0
    c_width = 0
    d_width = 0
    e_width = 0
    f_width = 0

    # Вставка данных
    for row in rows:
        # print(row)
        ws['A' + str(current_line)] = row['event']
        ws['B' + str(current_line)] = row['breed']
        ws['C' + str(current_line)] = row['class']
        ws['D' + str(current_line)] = row['sex']
        ws['E' + str(current_line)] = row['tattoo']
        ws['F' + str(current_line)] = row['owner']
        # ws.row_dimensions[current_line].width = True
        current_line += 1
        
        # Сохранение максимальной ширины столбцов 
        a_width = max(a_width, len(row['event']))
        b_width = max(b_width, len(row['breed']))
        c_width = max(c_width, len(row['class']))
        d_width = max(d_width, len(row['sex']))
        e_width = max(e_width, len(row['tattoo']))
        f_width = max(f_width, len(row['owner']))


    # Настройка ширины столбцов
    ws.column_dimensions['A'].width = a_width
    ws.column_dimensions['B'].width = b_width
    ws.column_dimensions['C'].width = c_width
    ws.column_dimensions['D'].width = d_width
    ws.column_dimensions['E'].width = e_width
    ws.column_dimensions['F'].width = f_width

    # Сохранение текущего отчёта
    wb.save(save_path)
    # print('save_path', save_path)
    del wb