# coding: utf-8
import json
import urllib
import sys, os
import traceback
import time
sys.path[0] = '../'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_globalhome'
#from hotspot.models import Category, SubEvent, Event, Venue
from tickets.models import Category, SubEvent, Event, Venue
session = 'globalhome353216' # Дается к API

all_categories = Category.objects.all()


def get_events():
    first_run = True
    for category in all_categories:
        category = category.id
        #category = 454827
    
        
        events = urllib.urlopen('http://api.cultserv.ru/jtransport/partner/get_events?category=%s&session=%s'%(category, session)).read()
        data_events = json.loads(events)
        
        if not first_run:
            time.sleep(2)
        first_run = False
        for key, value in data_events.items():
    
            if 1:
                for el in data_events['message']:
                     try:
                         sub = SubEvent.objects.get(id =el['id'])
                         print "Update of SubEvent, id = ",
                         print el['id']
                     except SubEvent.DoesNotExist:
                         print 'Add new event с id: %s ... '%(el['id'])
                         sub = SubEvent(id=el['id'])
                     try:
                        sub.str_date = el['str_date']
                     except:
                        print u'Нет элемента str_date'
    
                     try:
                        sub.str_time = el['str_time']
                     except:
                        print u'Нет элемента str_time'
                     try:
                       for elm in el['event']:
                           id = False
                           #========================================================
                           # print "===============111==Element========="
                           # print elm
                           # print "===============111==Element========="
                           #========================================================
                           try:
                               #print el['event']['id']
                               event = Event(el['event']['id'])
                               id = True
                           except:
                               print u'Нет элемента id в модели Events'
                           try:
                                event.title = el['event']['title']
                           except:
                               print u'Нет элемента title в модели Events'
                           try:
                                event.dates = el['event']['dates']
                           except:
                               print u'Нет элемента dates в модели Events'
                           try:
                               
                                   event.alias = el['event']['alias']
                           except:
                               print u'Нет элемента alias в модели Events'
                           try:
                                event.link = el['event']['link']
                           except:
                               print u'Нет элемента link в модели Events'
                           if id:
                               event.save()
                               sub.event_id = event.id
    
                          
                     except Exception, e:
                        print traceback.print_exc()
                        print u'Нет элемента event'
                       
                       
                     try:
                        sub.title = el['title'].replace('[TEST]','')
                     except:
                        print u'Нет элемента title'
                     try:
                        sub.sub_event_id = el['id']
                     except:
                        print u'Нет элемента id'
                     try:
                        sub.date = el['date']
                     except:
                        print u'Нет элемента date'
                     try:
                        sub.image = el['image']
                     except:
                        print u'Нет элемента image'
                     try:
                        sub.original_image = el['original_image']
                     except:
                        print u'Нет элемента original_image'
                     #==============================================================
                     # try:
                     #    print "11111111111111111111"
                     #    print el['alias']
                     #    #sub.original_image = el['alias']
                     # except:
                     #    print u'Нет элемента alias'
                     #==============================================================
    
                     try:
                       for elm in el['venue']:
                           id = False
    
                           try:
                               #print el['venue']['id']
                               venue = Venue.objects.get(id =el['venue']['id'])
                               id = True
                           except Venue.DoesNotExist:
                               venue = Venue(id =el['venue']['id'])
                               id = True
                           except:
                               print u'Нет элемента id в модели venue'
                           try:
                                   venue.title = el['venue']['title']
                           except:
                               print u'Нет элемента title в модели venue'
                           try:
                                venue.address = el['venue']['address']
                           except:
                               print u'Нет элемента address в модели venue'
                           try:
                                venue.alias = el['venue']['alias']
                           except:
                               print u'Нет элемента alias в модели venue'
                           try:
                                venue.region_id = el['venue']['region_id']
                           except:
                               print u'Нет элемента region_id в модели venue'
                           
                           if id:
                               venue.save()
                               sub.venue_id = venue.id
                     except:
                        print u'Нет элемента venue'
                     try:
                        sub.min_price = el['min_price']
                     except:
                        print u'Нет элемента min_price'
                     try:
                        sub.max_price = el['max_price']
                     except:
                        print u'Нет элемента max_price'
                     try:
                        sub.ticket_count = el['ticket_count']
                     except:
                        print u'Нет элемента ticket_count'
                     try:
                        sub.eticket_possible = el['eticket_possible']
                     except:
                        print u'Нет элемента eticket_possible'
                     #==============================================================
                     # try:
                     #    print "=========el['tags']========2222"
                     #    print  el['tags']
                     #    #sub.tags = el['tags']
                     # except:
                     #    print u'Нет элемента tags'
                     #==============================================================
                     try:
                        sub.type = el['type']
                     except:
                        print u'Нет элемента type'
                     try:
                        sub.add_title = el['add_title']
                     except:
                        print u'Нет элемента add_title'
                     try:
                        sub.end_date = el['end_date']
                     except:
                        print u'Нет элемента end_date'
                     try:
                        sub.categories_ids = el['categories_ids']
                     except:
                        print u'Нет элемента categories_ids'
                     try:
                        pass #sub.has_offer = el['has_offer']
                     except:
                        print u'Нет элемента has_offer'
                     import traceback
                     try:
                         sub.save()
                     except Exception, e:
                         print e
                         print traceback.print_exc()
                     cat = Category.objects.get(id=category)
                     sub.category.add(cat)
                     sub.save()
