# coding: utf-8

import json
import urllib
import sys, os
sys.path[0] = '../'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_globalhome'
#from hotspot.models import Category
from tickets.models import Category


def get_category():
    session = 'globalhome353216' # Дается к API
    first = True # Первый запуск и последующие
    categories = urllib.urlopen('http://api.cultserv.ru/jtransport/partner/get_categories?session=%s'%session).read()
    data_categories = json.loads(categories)
    c_all = Category(id = 1)
    c_all.title = u"Все события"
    c_all.save()
    for key, value in data_categories.items():
        if key == 'message':
            for el in data_categories[key]:
                category = el['id']
                try:
                    cat = Category.objects.get(id = el['id'])
                    first = False
                except Category.DoesNotExist:
                    pass
                if first: # Первый запуск
                    print "First Start of Script ..."
                    c = Category(id = category)
                    if el['title']:
                        c.title = el['title']
                    try:
                        c.eng_title = el['eng_title']
                    except:
                        print u'Нет такого элемента "eng_title"'
                    try:
                        c.count = el['count']
                    except:
                        pass 
                    try:
                        c.avatars_amount = el['avatars_amount']
                    except: # Нет такого элемента
                        pass 
                    try:
                        c.main_description = el['main_description']
                    except:
                        pass 
                    try:
                        c.category_description = el['category_description']
                    except:
                        pass 
                    try:
                        c.html_title = el['html_title']
                    except:
                        pass 
                    try:
                        c.weight = el['weight']
                    except:
                        pass 
                    try:
                        c.admin_weight = el['admin_weight']
                    except:
                        pass 
                    try:
                        c.show_venue_list = el['show_venue_list']
                    except:
                        pass
                    try:
                        c.title_genitive = el['title_genitive']
                    except:
                        pass
                    try:
                        c.title_title_dative = el['title_dative']
                    except:
                        pass
                    try:
                        c.title_accusative = el['title_accusative']
                    except:
                        pass
                    try:
                        c.title_instrumental = el['title_instrumental']
                    except:
                        pass
                    try:
                        c.title_prepositional = el['title_prepositional']
                    except:
                        pass
                    try:
                        c.title_prefix = el['title_prefix']
                    except:
                        pass
                    try:
                        c.object_prefix = el['object_prefix']
                    except:
                        pass
                    c.save()
                    #print el['title']
                    #===================================================================
                    # for key, value in el:
                    #     if key=='title':
                    #         print key, value
                    #===================================================================
                    #===================================================================
                    # if key == 'title':
                    #     print key, value
                    #===================================================================
                print "category = "+str(category)







