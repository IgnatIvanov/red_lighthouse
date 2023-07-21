import os
from django.shortcuts import render
from .models import Dog
from .models import Breed
from docxtpl import DocxTemplate
import datetime as dt



templates_path = 'out_doc/templates/out_doc/'
save_dir = 'документы/'



# Функция печати временных сертификатов
def print_temp_sertif(dogs_list, dt_now):

    # Загрузка документа
    template_name = 'временный сертификат.docx'
    template_file = templates_path + template_name

    # Путь сохранения изменённого документа
    save_path = save_dir
    save_path += dt_now + '/'
    save_path += 'временный сертификат/'
    
    os.makedirs(save_path)  # Создание пути сохранения файла
    
    for i in range(len(dogs_list)):

        # doc = docx.Document(docx = template_file)
        doc = DocxTemplate(template_file)

        dogie = dogs_list[i]

        # Подстановка данных
        context = {
            'name': dogie['name'],
            'sex': dogie['sex'],
            'tattoo': dogie['tattoo'],
            'rkf': dogie['rkf'],
            'birth': dogie['birth_date'],
            'owner': dogie['owner'],
            'breed': dogie['breed']
        }
        doc.render(context)

        # Сохранение документа
        save_file = save_path + dogs_list[i]['tattoo'] + '.docx'
        doc.save(save_file)



def main(request):

    dogs = Dog.objects.order_by('id')

    dogs_list = []
    for el in dogs:
        dogie = {}
        dogie['name'] = el.name_ru
        if dogie['name'] == '-':
            dogie['name'] = el.name_en
        dogie['breed'] = Breed.objects.filter(id=el.breed_id).first().name_ru
        dogie['sex'] = el.is_male

        if el.is_male:
            dogie['sex'] = 'КОБЕЛИ \ MALES'
        else:
            dogie['sex'] = 'СУКИ \ FEMALES'

        if el.birth_date.day < 10:
            day = '0' + str(el.birth_date.day)
        else:
            day = str(el.birth_date.day)

        if el.birth_date.month < 10:
            month = '0' + str(el.birth_date.month)
        else:
            month = str(el.birth_date.month)        

        birth_date = '{}.{}.{}'.format(
            day,
            month,
            el.birth_date.year
        )
        
        dogie['birth_date'] = birth_date
        dogie['tattoo'] = el.tattoo
        dogie['rkf'] = el.rkf
        dogie['owner'] = el.owner
        dogs_list.append(dogie)

    data = {
        'dogs': dogs_list
    }

    dt_now = str(dt.datetime.now()).replace(':','.')
    print_temp_sertif(dogs_list, dt_now)

    return render(request, 'out_doc/main.html', data)