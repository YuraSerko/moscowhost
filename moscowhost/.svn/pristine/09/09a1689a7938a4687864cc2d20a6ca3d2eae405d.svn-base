# coding: utf-8
import json
import urllib
import sys, os
import traceback
import time
from BeautifulSoup import BeautifulSoup
sys.path[0] = '../'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_globalhome'
from tickets.models import Category, SubEvent, Event, Venue, Get_SubEvent,  Tags #Sectors,


def origin_number(ll):
    for l1 in ll:
        count = 0
        for l2 in ll:
            if l1==l2:
                count = count+1
        if count>1:
            for c in range(count-1):
                ll.remove(l1)
    return ll

def del_event(event_id, value):
    try:
        passed_ev = SubEvent.objects.get(id = event_id)
        title = passed_ev.title
        passed_ev.deleted = True
        str_date = passed_ev.str_date
        passed_ev.save()
        #passed_ev.delete()
    except Exception, e:
        print u'Исключение при удалении события(SubEvent):',
        print e
    try:
        passed_event = Get_SubEvent.objects.get(id = event_id)
        passed_event.deleted = True
        passed_event.save()
        #passed_event.delete()
    except Exception, e:
        print u'Исключение при удалении события(Get_SubEvent):',
        print e
    print u"Удаляю событие с id = %s , Название: %s , Дата проведения: %s, Причина: %s"%(event_id, title, str_date, value)

all_events = SubEvent.objects.all().filter(deleted = False)


def get_description():
    session = 'globalhome353216' # Дается к API
    description_event_text = '' # Изменил description_event на description_event_text при сохранении в детальное описание 
    #all_events = [459408, 450405] # Для тестового много-объектного зацикливания
    #for event_id in all_events: # Для тестового много-объектного зацикливания
    for event in all_events: # Закомментить для тестового много-объектного зацикливания
        event_id = event.id # Закомментить для тестового много-объектного зацикливания
        print u"Событие с id = ",

        ######################################################
        #event_id = 451928 # Проверка конкретного события
        #####################################################

        print event_id,
        attempt = 10
        while not attempt == 0:
            try:
                description = urllib.urlopen('http://api.cultserv.ru/jtransport/partner/get_subevent?id=%s&session=%s'%(event_id, session)).read()
                attempt = 0
            except IOError:
                attempt -= 1
                print  "Net seti ili ne dostupen sayt http://api.cultserv.ru/ Podojdite..."
                time.sleep(20)
        data_description = json.loads(description)
        main_event = SubEvent.objects.get(id = event_id)
        description_event = ''
        description_event = SubEvent.objects.get(id = event_id)
        #print description_event.event.alias
        try:
            time.sleep(2)
            # Сделать чтобы по городам 
            #print description_event.event.alias
            print "Region ID = ",
            print description_event.venue.region_id
            if description_event.venue.region_id == 1: # Москва
                res = urllib.urlopen('http://ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 19: #  Екатеринбург
                res = urllib.urlopen('http://ekb.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 8: #  Санкт-Петербург
                res = urllib.urlopen('http://spb.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 17: #  Краснодар
                res = urllib.urlopen('http://krd.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 77: #  Томск
                res = urllib.urlopen('http://tomsk.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 90: #  Петрозаводск
                res = urllib.urlopen('http://petrzsk.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 9: #  Нижний Новгород
                res = urllib.urlopen('http://nnov.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 79: #  Иваново
                res = urllib.urlopen('http://ivanovo.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 16: # Уфа
                res = urllib.urlopen('http://ufa.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 166: # Сочи
                res = urllib.urlopen('http://sochi.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 31: # Новосибирск
                res = urllib.urlopen('http://nsk.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 15: # Казань
                res = urllib.urlopen('http://kzn.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 59: # Вологда
                res = urllib.urlopen('http://vld.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 72: # Белгород
                res = urllib.urlopen('http://bel.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 179: # Череповец
                res = urllib.urlopen('http://cher.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 3: # Тверь
                res = urllib.urlopen('http://tver.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 58: # Калуга
                res = urllib.urlopen('http://kaluga.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 11: # Чебоксары
                res = urllib.urlopen('http://cheb.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 75: # Красноярск
                res = urllib.urlopen('http://krsk.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 177: # Великие Луки
                res = urllib.urlopen('http://vluki.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 67: # Ижевск
                res = urllib.urlopen('http://izh.ponominalu.ru/event/%s'%description_event.event.alias).read()
            elif description_event.venue.region_id == 124: # Орёл
                res = urllib.urlopen('http://orel.ponominalu.ru/event/%s'%description_event.event.alias).read()
            #elif description_event.venue.region_id == 10: # Москва
            #    res = urllib.urlopen('http://ponominalu.ru/event/%s'%description_event.event.alias).read()
            else:
                res =""
            if res:
                soup = BeautifulSoup(str(res))
                for des in  soup.findAll("div", {"id":"event_description"}):
                    description_event_text =  des.renderContents()

                links_desc_list = []
                for a in  soup.find("div", {"id":"event_description"}).findAll('a'):
                    #print a.get('href').find('ponominalu')
                    if a.get('href').find('ponominalu') == -1:
                        #print a
                        links_desc_list.append(a.get('href'))
            #print origin_number(links_desc_list)
            for link in origin_number(links_desc_list):
                description_event_text = description_event_text.replace(str(link), 'http://ponominalu.ru'+str(link))
            description_event_text = description_event_text.replace('http://ponominalu.ruhttp://ponominalu.ru', 'http://ponominalu.ru').replace('ponominalu.ruhttp://ponominalu.ru', 'http://ponominalu.ru')
        except UnicodeError:
            print e
            description_event = ''
        except IOError:
            print "Errno socket error"
        except Exception, e :
            print "Error when parse description:",
            print e
        time.sleep(1)
        for key, value in data_description.items():
            if key == 'message':
                if value in [str(value)]: # Если код ошибки есть, например 'no tickets event'
                     print u'Ошибка: ',
                     print value
                     if not value.find('Event passed') == -1: # Если событие произошло или билетов на него уже нету, то удаляем его из базы данных
                         del_event(event_id, value)
                     elif not value.find('no more tickets') == -1:
                         del_event(event_id, value)
                     continue
                else:
                     for k, el in value.iteritems():
                         if k == 'add_title':
                             add_title = el
                         if k == 'tags':
                             tags_list = []
                             for e in el: #
                                 for k, v  in e.items():
                                     if k == 'id':
                                         id_tag = v
                                     if k == 'title':
                                         pass #print  v
                                     if k == 'alias':
                                         tag_alias = v
                                     if k == 'groups':
                                         for d in v:
                                             for k,v in d.items():
                                                 if k == 'id':
                                                     
                                                     id_group = v
                                                 if k == 'show':
                                                     #print v
                                                     show_group = v
                                                 if k == 'title':
                                                     #print v
                                                     title_group = v
                                                 if k == 'alias': # Алиасы по которым определяются grouptags
                                                     #print "==============alias=============="
                                                     #print v
                                                     try:
                                                         tag = Tags.objects.get(alias = v)
                                                         tags_list.append(tag.id)
                                                     except Tags.DoesNotExist:
                                                         print u'Нет таких alias в таблице Tags'
                                                     alias_group = v
                         if k == 'venue':
                             id_venue = False
                             for k,v in el.iteritems():
                                 if k == 'id':
                                     try:
                                         venue = Venue.objects.get(id = v)
                                     except Venue.DoesNotExist:
                                         venue = Venue(id = v)
                                     id_venue = True
                                 if k == 'description':
                                     desc = v
                                 if k == 'image':
                                     image = v
                                     #print image
                                 if id_venue:
                                     venue.description_text = desc
                                     try:
                                         venue.image = image
                                     except NameError:
                                         print 'No image'
                                     venue.save()
                                     if not main_event.venue_id:
                                         print "Add venue relation"
                                         main_event.venue_id = venue.id
                                         main_event.save()

    #===========================================================================
    #                      if k == 'sectors': # Создаю со своими id потому что совподают id по номиналу
    #                          sectors_id_pomominalu =''
    #                          sector_id_list = []
    #                          save_exist = False
    #                          try:
    #                              s = Get_SubEvent.objects.get(id = event_id)
    #                          except Get_SubEvent.DoesNotExist:
    #                              s = Get_SubEvent(id = event_id)
    #                          exist_sector = False
    #                          
    #                          for d in s.sectors_m2m.all():
    #                              #sector_id_list.append(d.id)
    #                              d.delete()
    #                              exist_sector = True
    #                              save_exist = True
    #                          #sys.exit()
    #                          sectors = el
    #                          #save_sector = False
    #                          save_sector = True
    #                          for el in sectors:
    #                              for k, v in el.iteritems():
    #                                  if k == 'id':
    #                                      id_ponominalu = v
    #                                  if k == 'admission':
    #                                      admission = v 
    #                                  if k == 'title':
    #                                      title = v
    #                                  if k == 'count':
    #                                      count = v
    #                                  if k == 'min_price':
    #                                      min_price = v
    #                                  if k == 'max_price':
    #                                      max_price = v
    #                                  if k == 'gateway_id':
    #                                      gateway_id = v
    # 
    #                              sectors_id_pomominalu = sectors_id_pomominalu + title+' '+str(id_ponominalu)+'|' #str(id)
    #                              #if not exist_sector:
    #                              sector = Sectors()
    #                              sector.save()
    #                              sector_id_list.append(sector.id)
    #                              save_sector = True
    #                              if save_sector:
    #                                  #sector = Sectors()
    #                                  sector.admission = admission
    #                                  sector.title = title
    #                                  sector.count = count
    #                                  sector.min_price = min_price
    #                                  sector.max_price = max_price
    #                                  sector.gateway_id = gateway_id
    #                                  sector.sectors_id_pomominalu = id_ponominalu
    #                                  sector.sectors_id_pomominalu = id_ponominalu
    #                              try:
    #                                 sector.save()
    #                              except Exception, e:
    #                                 print u'Не сохранено в Sector базу данных...',
    #                                 print e
    #===========================================================================
                         if k == 'commission':
                             commission = el
                     try:
                         get_sub = Get_SubEvent.objects.get(id = event_id)
                         change = True
                     except Get_SubEvent.DoesNotExist:
                         change = False
                         get_sub = Get_SubEvent(id = event_id)
                      
                     get_sub.description_event = description_event_text #description_event
                     description_event_text = ''
                     try:
                         get_sub.add_title = add_title # Не знаю почему ошибку вызывает !!!!
                     except NameError:
                         print "name 'add_title' is not defined "
                     get_sub.commission = commission
                     
                     #get_sub.sectors_id_pomominalu = sectors_id_pomominalu
                     get_sub.save()
                     #==========================================================
                     # for id in sector_id_list:
                     #     sec = Sectors.objects.get(id=id)
                     #     get_sub.sectors_m2m.add(sec)
                     #     get_sub.save()
                     #==========================================================

                     #print origin_number(tags_list)
                     for id in origin_number(tags_list):
                         tag = Tags.objects.get(id=id)
                         get_sub.tags_category.add(tag)
                         get_sub.save()
                     if change:
                         print u" Успешно изменено"
                     else:
                         print u" Успешно добавлено"

