# coding: utf-8
# $Id: views.py 253 2010-12-10 16:09:08Z site $
#import urls
import datetime, time  # @UnusedImport
#from models import fax_sending  # @UnusedImport
from django.contrib.auth.models import User  # @UnusedImport
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.core.urlresolvers import reverse  # @UnusedImport
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.template import Context, loader  # @UnusedImport
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import iri_to_uri, force_unicode
from django.http import Http404  # @UnusedImport
from django.conf import settings  # @UnusedImport
from django.db import connections  # @UnusedImport
from account.forms import UserRegistrationForm, UserLoginForm, PasswordResetRequestForm, ChangePasswordForm
from account.forms import ProfilePhisicalDataForm, ProfileJuridicalDataForm, ProfileCardDataForm, ProfileJuridicalDataMainForm, \
                          ProfileJuridicalDataAdditionalForm, ProfilePhisicalDataAdditionalForm, \
                          ProfileJuridicalDataIgnoredForm, ProfilePhisicalNotEditForm
from account.forms import AddressLegalForm, AddressPostalForm, AddressPhysicalForm, AccountTypeSelectForm, AccountTypeSelectFormJuridical, AccountTypeSelectFormPhysical
from data_centr.models import Zakazy, Status_zakaza, IP, Status_ip, Servers, Tariff, CPU \
                          ,Limit_connection_service, SoftwareType, SoftwareGroup, Software, UserCountForSoftware
from data_centr.views import add_record_in_data_centr_payment, add_record_in_priority_of_services, write_off_of_money
from findocs.models import  Package_on_connection_of_service, FinDocSigned
from findocs.views import create_package, deactivation_zakaz_under_the_contract, \
    FINDOCS_NOT_TO_DELETE, data_configuration
from services.models import AddSPTransaction  # @UnusedImport
from devices.models import UserService
from dateutil.relativedelta import relativedelta  # @UnresolvedImport
from django.db.models import Q
from settings import *
from billing.models import BillserviceAccount  # @UnresolvedImport
import paramiko, scp  # @UnresolvedImport
import re
import sys, smtplib, base64, StringIO  # @UnusedImport
import locale  # @UnusedImport
from scp import SCPClient
from string import split  # @UnusedImport
from optparse import OptionParser  # @UnusedImport
#from account.forms import ChangeBillingGroupForm, FaxForm, ComplaintForm, WishInternetForm
from account.forms import ChangeBillingGroupForm, ComplaintForm, WishInternetForm
from account.models import *
from billing.models import *
#from externalnumbers.consts import *
from billing import forms as utm_forms
from lib.decorators import render_to, login_required
from lib.helpers import redirect
from lib.http import get_query_string
import log
from django.contrib.admin.views.decorators import staff_member_required
#from telnumbers.models import TelNumber
import codecs
# from content.models import Section_type, Article
from account.forms import ResendActivationCodeForm
# from common import nextnum
from findocs import decorator_for_sign_applications
import copy
from page.views import panel_base_auth
from lib.mail import send_email
#from billing.models import BillservicePhoneTransaction, BillserviceRecordTransaction
#from billing.models import  BillserviceRecordTransaction
#from externalnumbers.models import ExternalNumber

from pickle import TRUE
from cards.models import BillserviceCard
from data_centr.views import cost_dc, add_document_in_dict_for_send, send_mail_check
from findocs.models import FinDocSignedZakazy, Check
from data_centr.views import dict_count_ip_for_service
from findocs import get_signed
from lib.paginator import SimplePaginator
from account.forms import BalanceFaxFilterForm, BalanceFilterForm, first_date, last_date
from datetime import timedelta
from data_centr.forms import AccountColocationForm, AccountRackForm

#############################
#from fs.models import Record_talk_activated_tariff, create_myivr_temp, create_myivr, Voice_mail, fax_numbers, TelNumbersListDetailNumbers, TelNumbersList
#from call_forwarding.forms import RuleEditForm, RulesListForm
#from call_forwarding.models import Rule
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.template import Template, RequestContext, loader
#from constructor import check_direction, vsepomestam, voicemail_create_vm, fax_create_getfax, time_range, number_list, call_number, create_ivr, call_list, checklist, checkfax, checkvoicemail, checkivr, getform, createDraft, waiting_list, check_waiting_list
#from account.models import CallTimeRange, CallNumber
from account.models import CallTimeRange
#from fs.models import NumberTemplates, NumberTemplateRule
import ast
from django.db import transaction
from data_centr.models import Data_centr_payment
from admin_user_stats.modules import RegistrationCharts
from django.db.models import Count



#!!! вообще был импорт с external numberss
# MOSCOW = 1
# STPETERSBURG = 2
# NUMBER_800 = 3 
# REGIONS = (
#     (MOSCOW, u"Москва"),
#     (STPETERSBURG, u"Ст. Петербург"),
#     (NUMBER_800, u"Федеральный номер 8-800"),
# )
#from moscowhost.urls import patterns


###############################
without_drop_elements = ['voice_mail', 'fax_rec', 'waiting_list', 'call_number', ]
dict_arterial_elements = ['split_ter', 'split_ter_drop', 'check_direction', 'check_direction_drop', 'time_range_drop', 'number_list_drop', 'time_range', 'number_list', 'splitter', 'splitter_drop', 'voice_menu_drop', 'voice_menu', 'call_list', 'call_list_drop']
descript = {'split_ter':u'Переадресация', 'voice_mail':u'Голосовая почта', 'time_range':u'Время в</br>', 'call_number':u'Звонок на</br>', 'waiting_list':u'Очередь', 'fax_rec':u'Факс', 'voice_menu':u'Голосовое меню', 'call_list':u'Звонить на список', 'number_list':u'Номер в списке', 'check_direction':u'Проверка по шаблону', }

@render_to('account/registration.html')
def registration(request):
    """
    Registers a new user from web interface.
    Creates record in auth.models.User model
    Send activation link to the user's email.
    User login is autogenerated as `u_<datetime>` (see model file)
    """
    context = {}
    # скрывает кнопки вход | регистрация
    context['panel_off'] = True

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_profile'))
    if request.method == "POST":

        # log.add("showing user registration page: POST")
        form = UserRegistrationForm(request.POST.copy())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            action_key, send_mail = ActionRecord.registrations.create_inactive_user_key(
                new_user=user,
                #row_password=form.get_row_password(),
                row_password = user.password,
                send_email=True,
            )
            request.notifications.add(_(u'Registration was completed. Please check your mailbox for activation letter'), 'success')
            return HttpResponseRedirect(reverse('account_registration_completed'))
    else:
        form = UserRegistrationForm()
        # log.add("showing user registration page")
    context['form'] = form
    return context

def func_change_warn_balance(request):
    try:
        warn_balance = request.POST.get('warn_balance')
    except Exception, e:
        raise Http404

    profile = request.user.get_profile()
    bill_acc = BillserviceAccount.objects.get(id=profile.billing_account_id)
    bill_acc.notification_balance = warn_balance
    bill_acc.save()
    return HttpResponse("ok")



def delete_recursive(id_scheme):
    all_element_after = OrderScheme.objects.filter(id_scheme_id=id_scheme)
    for x in all_element_after:
        if x.type in dict_arterial_elements:
            if x.id_next_scheme_id:
                delete_recursive(x.id_next_scheme_id)
                if x.number_in_order == 1:
                    try:
                        parent_element_in_order = OrderScheme.objects.get(id_next_scheme_id=x.id_scheme_id)
                        parent_element_in_order.id_next_scheme_id = None
                        parent_element_in_order.save()
                    except OrderScheme.DoesNotExist, e:
                        pass
        x.delete()

# def delete_recursive_draft(id_scheme):
#    all_element_after = OrderSchemeDraft.objects.filter(id_scheme_id = id_scheme)
#    for x in all_element_after:
#        if x.type in dict_arterial_elements:
#            if x.id_next_scheme_id:
#                delete_recursive_draft(x.id_next_scheme_id)
#                if x.number_in_order == 1:
#                    try:
#                        parent_element_in_order = OrderSchemeDraft.objects.get(id_next_scheme_id = element.id_scheme_id)
#                        parent_element_in_order.id_next_scheme_id = None
#                        parent_element_in_order.save()
#                    except OrderSchemeDraft.DoesNotExist, e:
#                        pass
#        x.delete()

def delete_element(request):
    profile = request.user.get_profile()
    z = request.POST['element']
    try:
        replace_element = request.POST['replace_element']
    except:
        replace_element = None
    id_in_order = z.split('_')[-1]
    # id_element = request.POST['element'].split('_')[-2]
    type_element = '_'.join(z.split('_')[:-2])
    replace_id = {}
    element_in_draft = False
    try:
        if type_element in dict_arterial_elements:
            element_in_order = OrderScheme.objects.get(id=id_in_order)
            all_element_in_order = OrderScheme.objects.filter(type=type_element, id_element=z.split('_')[-2], id_scheme_id=element_in_order.id_scheme_id)
            if not all_element_in_order:
                all_element_in_order = OrderSchemeDraft.objects.filter(type=type_element, id_element=z.split('_')[-2])
                element_in_draft = True
            id_scheme_id_for_dec = None
            for element in all_element_in_order:
                if element.id_next_scheme_id:
                    if not replace_element:
                        delete_recursive(element.id_next_scheme_id)
                    else:
                        replace_id[element.number_in_arterial] = element.id_next_scheme_id
                        replace_id['level_width_%s' % element.number_in_arterial] = element.level_width
                if element.number_in_order == 1:
                    try:
                        if element_in_draft:
                            parent_element_in_order = OrderSchemeDraft.objects.get(id_next_scheme_id=element.id_scheme_id)
                        else:
                            parent_element_in_order = OrderScheme.objects.get(id_next_scheme_id=element.id_scheme_id)
                        parent_element_in_order.id_next_scheme_id = None
                        id_scheme_id_for_dec = parent_element_in_order.id_scheme_id
                        parent_element_in_order.save()
                    except OrderScheme.DoesNotExist, e:
                        id_scheme_id_for_dec = None
                        pass
                element.delete()
                if not replace_element and id_scheme_id_for_dec:
                    try:
                        dec_all_parentsnew(id_scheme_id_for_dec)
                    except:
                        pass
        else:
            element_in_order = OrderScheme.objects.get(id=id_in_order)
            all_element_after = OrderScheme.objects.filter(id_scheme_id=element_in_order.id_scheme_id, number_in_order__gte=element_in_order.number_in_order)
            for x in all_element_after:
                if x.type in dict_arterial_elements:
                    if x.id_next_scheme_id:
                        delete_recursive(x.id_next_scheme_id)
                if x.number_in_order == 1:
                    try:
                        parent_element_in_order = OrderScheme.objects.get(id_next_scheme_id=x.id_scheme_id)
                        parent_element_in_order.id_next_scheme_id = None
                        parent_element_in_order.save()
                    except OrderScheme.DoesNotExist, e:
                        pass
                x.delete()
    except Exception, e:
        print e
    return HttpResponse(str(replace_id))




def user_reg_check_ajax(request):
    if not request.POST.has_key('user'):
        raise Http404
    user = request.POST['user']
    users_object = User.objects.order_by('username').filter(username=user.encode('utf-8'))
    users_email_object = User.objects.order_by('email').filter(email=user.encode('utf-8'))
    check = len(users_object)
    check_e = len(users_email_object)
    if check == 1 or check_e >= 1:
        #return HttpResponse(check)
        return HttpResponse('1')
    else: users_object = BillserviceCard.objects.order_by('login').filter(login=user.encode('utf-8'))
    check = len(users_object)
    # transaction.commit_unless_managed(using=settings.BILLING_DB)
    return HttpResponse(check)

@render_to('account/registration_completed.html')
def registration_completed(request):
    """Shows page with registration complete message"""
    return panel_base_auth(request, {})

def activation(request, action_key):
    """
    Activates user based on activation key
    Activate user - set is_active to true
    """
    try:
        # активация или восстановление пароля
        action = ActionRecord.objects.get(action_key=action_key)
        print(action.action_type)
        if action.action_type == 'R':
            action_type = 'reset_password'
        else:
            action_type = 'activate'
        user = authenticate(activation_key=action_key, action=action_type)
        if not user:
        # action key does not exist or expired
            return HttpResponseForbidden(u'Запись о регистрации не найдена или просрочена. Чтобы получить код активации регистрации заново, пройдите по <a href="%s">ссылке</a>.' % reverse('resend_activation_code'))
    except ActionRecord.DoesNotExist:
        return HttpResponseForbidden(u'Запись о регистрации не найдена или просрочена. Чтобы получить код активации регистрации заново, пройдите по <a href="%s">ссылке</a>.' % reverse('resend_activation_code'))

    _login(request, user)

    # перелинковка в зависимости от активации или восстановления пароля
    if action.action_type == 'R':
        request.notifications.add(_(u'Новый пароль был выслан на Вашу почту'), 'success')
        _logout(request)
        return HttpResponseRedirect('/')
    else:
        try:
            profile = user.get_profile()
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()        
        profile.is_juridical = user.is_juridical
        profile.activated_at = datetime.datetime.now()
        profile.save()
        Limit_connection_service.create_limit_for_new_user(profile.billing_account)
        #request.notifications.add(_(u'Your account has been activated.'), 'success') 
        #return HttpResponseRedirect(reverse('account_profile'))
        return HttpResponseRedirect("/account/#suggest_change_password")

def complaint(request, context, subject, message, bool):
    if request.user.is_anonymous():
        context['bout'] = True
    else:
        context['user_name'] = request.user.username
    if request.method == 'POST':
        if bool:
            form = ComplaintForm(request.POST.copy())
            to_email = settings.LIST_WISH_PHONE
        elif not bool:
            form = WishInternetForm(request.POST.copy())
            to_email = settings.LIST_WISH_INT
        if form.is_valid():
                send_email(subject, message, settings.EMAIL_HOST_USER, to_email, request.user.id)
                request.notifications.add(_(u'Ваша жалоба принята. Благодарим Вас.'), 'success')
    else:
        if bool:
            form = ComplaintForm()
        elif not bool:
            form = WishInternetForm()
    context['form'] = form
    return context


@render_to('account/complaint.html')
def complaint_phone(request):
    context = {}
    bool = True
    context['form1'] = True
    context['title'] = u'Отправка жалобы'
    context['meta_title'] = u'Отправить жалобу через сайт'
    subject = u"Новая жалоба на сайте: %s" % request.POST.get("title")
    message = u"%s.\nE-Mail: %s" % (request.POST.get("bodytext"), request.POST.get("submitter_email"))
    context = complaint(request, context, subject, message, bool)
    return context

@render_to('account/complaint.html')
def complaint_int(request):
    context = {}
    bool = False
    context['title'] = (u'Отправка жалобы/просьбы')
    context['form1'] = False
    subject = u"Новая жалоба/просьба от хотспот пользователя:%s. Место оказания услуги: %s" % (request.POST.get("name"), request.POST.get("place"))
    message = u"%s.\n\n\nE-Mail: %s" % (request.POST.get("text"), request.POST.get("submitter_email"))
    context = complaint(request, context, subject, message, bool)
    return context


def handle_uploaded_file(f):
    destination = open('media/fax/doc/%s' % f, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def handle_uploaded_image(f):
    destination = open('media/fax/upl_fax/%s' % f, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

import os
from django.shortcuts import render_to_response




@render_to('account/resend_activation_code.html')
def resend_activation_code(request):
    context = {}
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_profile'))
    context['panel_off'] = True
    if request.method == 'POST':
        form = ResendActivationCodeForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            try:
                action = ActionRecord.objects.get(user=user, action_type='A')
            except (ActionRecord.DoesNotExist, ActionRecord.MultipleObjectsReturned):
                if user.is_active:
                    request.notifications.add(u'Данный пользователь уже активирован.', 'error')
                else:
                    request.notifications.add(u'Регистрационная запись для данного пользователя не найдена. Попробуйте зарегистрироваться заново.', 'error')
                context['form'] = form
                return context
            ActionRecord.registrations.resend_activation_email(action=action)
            request.notifications.add(u'Код регистрации выслан на email, указанный при регистрации.', 'success')
            return HttpResponseRedirect('/')
    else:
        form = ResendActivationCodeForm(initial=request.GET)
    context['form'] = form
    return context

class AccountCreationWizard(object):
    def __init__(self, request):
        self.request = request

@render_to('account/account_creation.html')
@login_required
def account_creation(request):
    """
    Just after activation we need to create a UserProfile object, and create needed changes in UTM pages
    1) Show form for creating user account (phisical or juridical person etc.) # TODO
    2) Creates user's Profile, UTM User, notify admin # TODO
    3) Creates needed changes in UTM database # TODO
    4) Redirects to teh User's cabinet
    """
    return {}

@render_to('account/password_reset_request.html')
def password_reset_request(request):
    """Восстановление пароля для пользователя"""
    context = {}
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_profile'))
    context['panel_off'] = True
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = form.user
            if user:
                ActionRecord.resets.create_password_reset([user])
                request.notifications.add(u'Письмо с инструкциями по смене пароля было выслано Вам по электронной почте.', 'success')
            else:
                request.notifications.add(u'Пользователя с указанным именем не существует!', 'error')
    else:
        form = PasswordResetRequestForm()
    context['form'] = form
    return context

#from hotspot.views import hotspot_identity
@render_to("account/login.html")
def login(request):
    """User login page"""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_profile'))
    if not request.user.is_anonymous():
        return HttpResponseRedirect(iri_to_uri(redirect(request)))
    context = {}
    context['login_page_account'] = True
    #context['site'] = settings.CURRENT_SITE
    context['panel_off'] = True

    class TopErrors(object):
        def __init__(self):
            self._errors = []
        def add(self, error):
            self._errors.append(u'<li>%s</li>' % error)
        def render(self):
            if self._errors:
                return u'<ul class="errorlist">%s</ul>' % '\n'.join(self._errors)
            return u''

    top_errors = TopErrors()

    if request.POST:
        form = UserLoginForm(request.POST.copy())
        if form.is_valid():
            user = form.user
            if user:
                if user.is_active:
                    _login(request, user)
                    return HttpResponseRedirect(redirect(request, next_only=get_base_url(user)))
                else:
                    try:
                        action = ActionRecord.objects.get(user=user, type='A')
                    except:
                        action = None
                    if not action or action.expired:
                        top_errors.add(u'''
                        Учётная запись не активирована.
                        Возможно, Вы не прошли по ссылке в письме,
                        присланном Вам после регистрации.
                        <br/>
                        Если Вы не получали письма, или код активации просрочен, Вы можете
                        <a class="bold" href="%s?user=%s">получить код активации заново</a>.
                        ''' % (reverse('resend_activation_code'), form.cleaned_data['username']))
        else:
            pass
    else:
        form = UserLoginForm()
    context['form'] = form
    context['top_errors'] = top_errors.render()

    #context.update(hotspot_identity(request))
    return context

def logout(request):
    _logout(request)
    return HttpResponseRedirect('/')

# ************************ PROFILE VIEWS *****************************

def get_now():
    "Возвращает текущее время без микросекунд"
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)

@login_required
@render_to('account/account_data_centr.html')
def account_data_centr(request):
    context = {}
    context['user'] = request.user
    context['current_view_name'] = 'account_data_centr'
    return context







@login_required
#@render_to('account/account_physical_servers.html')
@render_to('account/account_virtual_servers.html')
def account_virtual_servers(request):
    print 'ACCCOUNT VIRTUAL SERVERS'
    context = {}
    context['user'] = request.user
    
    # context = {}
    #context['pannel'] = pannel_construct(request)
    #context['pannel'] = pannel_construct(request)
    #context['user'] = request.user
    #context['current_view_name'] = 'account_data_centr'
    
    #только 1С
    soft_objs = Software.objects.filter(type__id = 1).order_by('group')
    #print soft_objs
    #context['soft_objs'] = soft_objs
    
    soft_list = []
    
    for soft_obj in soft_objs:
        s_tariff = soft_obj.tariff
        s_description = soft_obj.url_with_description
        
        if soft_obj.group != None:
            s_group = soft_obj.group.id
            s_group_name = soft_obj.group.group_name
        else:
            s_group = None
            s_group_name = ''
    
        s_cost = '%.2f' % (soft_obj.tariff.price_id.cost / 1.18)
        soft_list.append({'id':soft_obj.id, 'tariff':s_tariff, 'cost':s_cost, 'url_desc':s_description, 'group':s_group, 'group_name': s_group_name})
    
    
    
    
    
        
    #print soft_list   
    context['soft_list'] = soft_list
    context['user_count_for_software'] = UserCountForSoftware.objects.all().order_by('id')
    #context['1C_configurations'] = 
    
    
    servers = []
    server = Servers.objects.get(id = 2)
    server_hdd = "<br />".join(i.__unicode__() for i in server.hdd.exclude(interface_id=3)) or '-'
    server_ssd = "<br />".join(i.__unicode__() for i in server.hdd.filter(interface_id=3)) or '-'
    server_ram = "<br />".join(i.__unicode__() for i in server.ram.all())
    cost = '%.2f' % (server.tariff.price_id.cost / 1.18)
    servers.append({'id':server.id, 'tariff':server.name, 'cpu':server.cpu, 'ram':server_ram,
                    'hdd': server_hdd, 'ssd': server_ssd, 'cost': cost})
    context['servers'] = servers
    context['server_id'] = server.id
    context['total_cost'] = cost
    
    
    '''
    if not servers:
        request.notifications.add(u'В настоящий момент нет свободных серверов. Приносим свои извинения за доставленные неудобства.', 'info')
    cpu_qs = CPU.objects.all()
    context['cpu_qs'] = cpu_qs
    context['count_cpu'] = len(cpu_qs) - 1
    context['user'] = request.user
    context['current_view_name'] = 'account_data_centr'
    servers = []
    for server in Servers.objects.filter(count_servers__gte=1):
        server_hdd = "<br />".join(i.__unicode__() for i in server.hdd.exclude(interface_id=3)) or '-'
        server_ssd = "<br />".join(i.__unicode__() for i in server.hdd.filter(interface_id=3)) or '-'
        server_ram = "<br />".join(i.__unicode__() for i in server.ram.all())
        cost = '%.2f' % (server.tariff.price_id.cost / 1.18)
        servers.append({'id':server.id, 'tariff':server.name, 'cpu':server.cpu, 'ram':server_ram,
                        'hdd': server_hdd, 'ssd': server_ssd, 'cost': cost})
    context['servers'] = servers
    if not servers:
        request.notifications.add(u'В настоящий момент нет свободных серверов. Приносим свои извинения за доставленные неудобства.', 'info')
    cpu_qs = CPU.objects.all()
    context['cpu_qs'] = cpu_qs
    context['count_cpu'] = len(cpu_qs) - 1
    context['servers'] = servers
    '''
    
    
    context['current_view_name'] = 'account_virtual_servers' 
    return panel_base_auth(request, context)

'''
@login_required
@render_to('account/account_vds.html')
def account_vds(request):
    context = {}
    context['user'] = request.user
    context['current_view_name'] = 'account_vds'
    return context
'''

'''
@login_required
@render_to('account/account_hosting.html')
def account_hosting(request):
    context = {}
    context['user'] = request.user
    context['current_view_name'] = 'account_hosting'
    return context
'''



'''
@login_required
@render_to('account/account_communication_links.html')
def account_communication_links(request):
    context = {}
    context['user'] = request.user
    context['current_view_name'] = 'account_communication_links'
    return context
'''


@login_required
@render_to('account/my_data_centr.html')
def my_data_centr(request):
    context = {}
    bill_acc = BillserviceAccount.objects.get(username=request.user.username)
    cont_zayavki = Zakazy.objects.filter(Q(bill_account=bill_acc.id) & Q(section_type=2) & Q(status_zakaza=1) & Q(date_deactivation=None)).exclude(service_type_id=12).order_by('id')
    zayavki = []
    tariff_obj = Tariff.objects.get(id=41)
    for i in cont_zayavki:
        try:
            cost = i.cost + ((i.count_ip - i.tariff.ip) * tariff_obj.price_id.cost)
            pod_zakazy = Zakazy.objects.filter(main_zakaz=i.id)
            for pod_zakaz in pod_zakazy:
                cost += pod_zakaz.cost
            #посчитаем software по m2m
            
            software = i.software.all()
            if software :
                for sw  in software:
                    cost += sw.tariff.price_id.cost
            
            #===
            cost = '%.2f' % cost
        except:
            cost = 0
        date_create = datetime.datetime.strftime(i.date_create, "%d.%m.%Y %H:%M:%S")
        zayavki.append({"id":i.id, "service_type":i.service_type, "tariff":i.tariff, "equipment":i.equipment,
                        "unit":i.count_of_units, "port":i.count_of_port, "ip":i.count_ip, "socket":i.socket,
                        "electricity":i.electricity, "cost":cost, "date_create":date_create, "status":i.status_zakaza.status})
    if list(zayavki) == []:
        context['check_zayavki'] = 'true'
        context['zayavki'] = []
    else:
        context['zayavki'] = zayavki

    cont_zakazy = Zakazy.objects.filter((Q(status_zakaza=2) | Q(status_zakaza=4)) & Q(bill_account=bill_acc.id) & Q(section_type=2)\
                                        & Q(service_type__id__in=[1, 2, 11])).exclude(date_activation=None).order_by('id')
    zakazy = []
    spis_zakaz_id = []
    for zakaz in cont_zakazy:
        spis_zakaz_id.append(zakaz.id)
    cont_pod_zakazy = Zakazy.objects.filter((Q(status_zakaza=2) | Q(status_zakaza=4)) & Q(bill_account=bill_acc.id) & Q(main_zakaz__in=spis_zakaz_id)).exclude(date_activation=None).order_by('id')
    for i in cont_zakazy:
        try:
            cost = i.cost
            cost = '%.2f' % cost
        except:
            cost = 0
        if i.date_deactivation:
            date_deactivation = datetime.datetime.strftime(i.date_deactivation, "%d.%m.%Y")
        else:
            date_deactivation = i.date_deactivation
        date_create = datetime.datetime.strftime(i.date_create, "%d.%m.%Y %H:%M:%S")
        date_activation = datetime.datetime.strftime(i.date_activation, "%d.%m.%Y")
        zakazy.append({"id":i.id, "service": '%s' % (i.service_type), "cost":cost, "date_deactivation":date_deactivation, \
                        "date_activation":date_activation, "status_zakaza":i.status_zakaza.status})
    pod_zakazy = []
    for j in cont_pod_zakazy:
        if j.service_type.id == 10:
            ip = j.ip.all()[0]
            service = '%s<br />(%s)' % (j.service_type, ip)
        elif j.service_type.id == 12:
            dict_garant = {True:u'Гарантированный', False:u'Не гарантированный'}
            service = u'%s<br />(%s, %s Мбит/сек)' % (j.service_type, dict_garant[j.tariff.garant], j.tariff.speed_inet)
        #
        elif j.service_type.id ==17:
            service = u'%s<br/>(%s) ' %(j.service_type, j.tariff)
        
        #
        elif j.service_type.id ==18:
            service = u'%s<br/>(%s) ' %(j.service_type, j.tariff)
            
        if j.status_cost not in (3,):
            cost = j.cost
            deactivation = True
        else:
            cost = u'Входит в стоимость'
            deactivation = False
        if j.date_deactivation:
            date_deactivation = datetime.datetime.strftime(j.date_deactivation, "%d.%m.%Y")
        else:
            date_deactivation = j.date_deactivation
        date_activation = datetime.datetime.strftime(j.date_activation, "%d.%m.%Y")
        pod_zakazy.append({"id":j.id, "service":service, "cost":cost, "date_deactivation":date_deactivation, \
                           "date_activation":date_activation, "status_zakaza":j.status_zakaza.status, "main_zakaz":j.main_zakaz, 'deactivation':deactivation})
    if not list(cont_zakazy):
        context['check_zakazy'] = 'true'
        context['zakazy'] = []
        context['pod_zakazy'] = []
    else:
        context['zakazy'] = zakazy
        context['pod_zakazy'] = pod_zakazy

    context['current_view_name'] = 'my_data_centr'
    context['my_zakazy'] = True
    return context


@login_required
@render_to('account/demands_dc_archive.html')
def demands_dc_archive(request):
    context = {}
    bill_acc = BillserviceAccount.objects.get(username=request.user.username)
    now = datetime.datetime.now()
    cont_zakazy = Zakazy.objects.filter(bill_account=bill_acc.id, status_zakaza=3).exclude(date_activation=None).order_by('id')
    zakazy = []
    for i in cont_zakazy:
        ip = ''
        for ip_temp in i.ip.all():
            ip += str(ip_temp) + '<br />'
        ip = ip.strip('<br />')
        try:
            cost = i.cost / 1.18
            cost = '%.2f' % cost
        except:
            cost = 0
        if i.date_deactivation:
            date_deactivation = datetime.datetime.strftime(i.date_deactivation, "%d.%m.%Y %H:%M:%S")
        else:
            date_deactivation = i.date_deactivation
        date_create = datetime.datetime.strftime(i.date_create, "%d.%m.%Y %H:%M:%S")
        date_activation = datetime.datetime.strftime(i.date_activation, "%d.%m.%Y %H:%M:%S")
        zakazy.append({"id":i.id, "service_type":i.service_type, "tariff":i.tariff, "equipment":i.equipment,
                        "unit":i.count_of_units, "port":i.count_of_port, "ip":ip, "socket":i.socket,
                        "electricity":i.electricity, "cpu":i.cpu.name, "ram":i.ram.name, "hdd":i.hdd.name,
                        "os":i.os.name, "cost":cost, "date_create":date_create, "date_deactivation":date_deactivation,
                        "date_activation":date_activation, "status_zakaza":i.status_zakaza.status})
    if not list(cont_zakazy):
        context['check_zakazy'] = 'true'
        context['zakazy'] = []
    else:
        context['zakazy'] = zakazy
    context['current_view_name'] = 'demands_dc_archive'
    return context

@login_required
@render_to('account/my_data_centr.html')
def del_zayavka(request, hidden_id):
    try:
        profile = Profile.objects.get(user=request.user)
        bac = profile.billing_account
        zayavka = Zakazy.objects.get(id=hidden_id)
        if zayavka.bill_account == bac:
            now = datetime.datetime.now()
            zayavka.status_zakaza = Status_zakaza.objects.get(id=3)
            zayavka.date_deactivation = now
            pod_zakazy = Zakazy.objects.filter(main_zakaz=zayavka.id, status_zakaza__id=1)
            for pod_zakaz in pod_zakazy:
                pod_zakaz.date_deactivation = now
                pod_zakaz.status_zakaza_id = 3
                pod_zakaz.save()
            spis_ip = zayavka.ip.all()
            for ip in spis_ip:
                ip_obj = IP.objects.get(name=ip)
                status_ip_obj = Status_ip.objects.get(id=1)
                ip_obj.status_ip = status_ip_obj
                ip_obj.save()
            zayavka.save()
            request.notifications.add(_(u"Заявка успешно деактивирована!"), "success")
        else:
            request.notifications.add(_(u"Вы попытались удалить не существующую у Вас заявку!"), "warning")
    except UserService.DoesNotExist:
        raise Http404
    return HttpResponseRedirect("/account/demands_dc/")


@login_required
@render_to('account/my_data_centr.html')
@decorator_for_sign_applications()
def previously_del_zakaz(request, hidden_id):
    print 'previously_del_zakaz'
    try:
        package_obj = Package_on_connection_of_service.objects.get(user=request.user, activate=False, deactivate=False)
    except Package_on_connection_of_service.DoesNotExist:
        successfully_create = create_package(request.user,
                                '/account/demands_dc/zakaz/%s/' % hidden_id,
                                reverse('my_data_centr'),
                                '',
                                ['dop_soglashenie_k_dogovoru'])
        if not successfully_create:
            raise Http404
        else:
            return HttpResponseRedirect('/account/demands_dc/zakaz/%s/' % hidden_id)
    try:
        profile = Profile.objects.get(user=request.user)
        bac = profile.billing_account
        now = datetime.datetime.now()
        date_next_start_month_temp = now + relativedelta(months=1)
        date_next_start_month = datetime.datetime(date_next_start_month_temp.year, date_next_start_month_temp.month, 1, 0, 0, 0)
        zakaz = Zakazy.objects.get(id=hidden_id)
        if zakaz.bill_account == bac:
            zakaz.date_deactivation = date_next_start_month
            zakaz.save()
            pod_zakazy = Zakazy.objects.filter(main_zakaz=zakaz.id, status_zakaza__id__in=[2, 4])
            for pod_zakaz in pod_zakazy:
                pod_zakaz.date_deactivation = date_next_start_month
                pod_zakaz.save()
            package_obj.activate = True
            package_obj.save()
            request.notifications.add(_(u"Заявка успешно деактивирована!"), "success")
        else:
            request.notifications.add(_(u"Вы попытались удалить не существующий у Вас заказ!"), "warning")
    except:
        raise Http404
    return HttpResponseRedirect("/account/demands_dc/")


@login_required
@decorator_for_sign_applications()
def activation_zakaz(request):      #здесь активация заказа
    try:
        package_obj = Package_on_connection_of_service.objects.get(user=request.user, activate=False, deactivate=False)
        data_temp = eval(package_obj.data)
        request.POST = data_temp
    except Package_on_connection_of_service.DoesNotExist:
        if not request.POST.get('hidden_id'):
            raise Http404
        hidden_id = request.POST["hidden_id"]
        zakaz_obj = Zakazy.objects.get(id=hidden_id)
        spis_ip = IP.objects.filter(section_type=2, status_ip=1).order_by('price_id')
        if len(spis_ip) < zakaz_obj.tariff.ip:
            request.notifications.add(_(u"К сожалению мы не можем Вам выдать такое количество IP-адресов!"), "warning")
            return HttpResponseRedirect(reverse('my_data_centr'))
        service_type_id = zakaz_obj.service_type.id
        if service_type_id == 1:
            slugs = ['akt_priemki_peredachi_vypoln_rabot']
        else:
            slugs = ['akt_priema_peredachi_oborudovaniya', 'akt_priemki_peredachi_vypoln_rabot']
        request_post = {}
        for key, value in request.POST.iteritems():
            request_post[key.encode("utf-8")] = value.encode("utf-8")
        successfully_create = create_package(request.user,
                                reverse('activation_zakaz'),
                                reverse('my_data_centr'),
                                '%s' % request_post,
                                slugs)
        if not successfully_create:
            raise Http404
        else:
            return HttpResponseRedirect(reverse('activation_zakaz'))
    hidden_id = request.POST["hidden_id"]
    try:
        spis_zakaz = []
        now = datetime.datetime.now()
        status_obj = Status_zakaza.objects.get(id=2)
        zakaz = Zakazy.objects.get(id=hidden_id)
        
        
        
        
        
        #форимируем заказы на ПО========================================================
        software_objs = zakaz.software.all()
        if software_objs.count!=0:
            for software_obj in software_objs:
                tariff_obj = Tariff.objects.get(id=software_obj.tariff.id)
                zakaz_software = Zakazy(
                        main_zakaz=zakaz.id,
                        #status_cost=status_cost, #????
                        bill_account=zakaz.bill_account,
                        section_type=2,
                        status_zakaza_id=2,
                        service_type_id=17, #ПО
                        tariff=tariff_obj,
                        date_create=datetime.datetime.now(),
                        date_activation=datetime.datetime.now(),
                        #count_ip=1,
                        )
                zakaz_software.save()
                zakaz_software.cost = '%.2f' % tariff_obj.price_id.cost
                zakaz_software.save()
                #подсчет
        #===============================================================================
        
        
        
        
        zakaz.status_zakaza = status_obj
        zakaz.date_activation = now
        zakaz.save()
        findoc_sign_zakaz = FinDocSignedZakazy.objects.get(zakaz_id=zakaz.id, fin_doc__findoc__slug='telematic_data_centr')
        pod_zakazy_queryset = Zakazy.objects.filter(main_zakaz=zakaz.id)
        for pod_zakaz in pod_zakazy_queryset:
            pod_zakaz.date_activation = now
            pod_zakaz.status_zakaza = status_obj
            pod_zakaz.save()
            spis_zakaz.append(pod_zakaz.id)
            findoc_sign_zakaz_port = copy.copy(findoc_sign_zakaz)
            findoc_sign_zakaz_port.id = None
            findoc_sign_zakaz_port.zakaz_id = pod_zakaz.id
            findoc_sign_zakaz_port.save()
        spis_ip = IP.objects.filter(section_type=2, status_ip=1).order_by('price_id')
        tariff_obj = Tariff.objects.get(id=41)
        for i, numb_ip in enumerate(range(1, zakaz.count_ip + 1)):
            print i, numb_ip
            ip_obj = spis_ip[i]
            status_cost = 3 if zakaz.tariff.ip >= numb_ip else 1
            zakaz_ip = Zakazy(
                main_zakaz=zakaz.id,
                status_cost=status_cost,
                bill_account=zakaz.bill_account,
                section_type=2,
                status_zakaza_id=2,
                service_type_id=10, #аренда порта
                tariff=tariff_obj,
                date_create=datetime.datetime.now(),
                date_activation=datetime.datetime.now(),
                count_ip=1,
                )
            zakaz_ip.save()
            zakaz_ip.ip.add(ip_obj)
            zakaz_ip.save()
            cost = float(cost_dc(zakaz_ip.id))
            zakaz_ip.cost = '%.2f' % cost
            zakaz_ip.save()
            ip_obj.status_ip_id = 2
            ip_obj.save()

            findoc_sign_zakaz_ip = copy.copy(findoc_sign_zakaz)
            findoc_sign_zakaz_ip.id = None
            findoc_sign_zakaz_ip.zakaz_id = zakaz_ip.id
            findoc_sign_zakaz_ip.save()

            if status_cost in (1,):
                add_record_in_data_centr_payment(zakaz_ip)
                add_record_in_priority_of_services(zakaz_ip)
                spis_zakaz.append(zakaz_ip.id)
        spis_zakaz.append(zakaz.id)
        package_obj.activate = True
        package_obj.save()

        profile_obj = Profile.objects.get(user=request.user)
        dict_id_rules = {1:[1, 13], 2:[3, 13, 14], 11:[12, 13, 14]}  #11 - аренда сервера
        spis_rules = Check.group_rules(profile_obj, dict_id_rules[zakaz.service_type.id], 'type_check', zakaz.id)
        print 'spis_rules = %s' % spis_rules
        content_check_id = Check.create_check(request.user, spis_rules, False, spis_zakaz)
        print 'content = %s' % content_check_id
        dict_documents_for_send = add_document_in_dict_for_send({}, request.user.id, 'Check', content_check_id)
        print 'dict_document = %s' % dict_documents_for_send
        send_mail_check(dict_documents_for_send)

        add_record_in_data_centr_payment(zakaz)
        add_record_in_priority_of_services(zakaz)
        write_off_of_money(zakaz.bill_account, [zakaz.id])
    except Exception, e:
        print e
        pass
    return HttpResponseRedirect("/account/demands_dc/")



@login_required
@render_to('account/service_choice.html')
def service_choice(request):
    context = {}
    context['title'] = u'Выберите один из разделов для последующей работы'
    return context


@login_required
@render_to('account/profile.html')
def account(request):
    """ Shows profile dashboard information and change form for user from request"""
    context = {}
    context['account'] = True
    context['action'] = ''
    context['title'] = _(u'Account information')
    context['current_view_name'] = 'account_profile'
    context['account_page'] = True  #for menu
    context['no_value'] = '<span class="no-value">%s</span>' % ugettext(u'not set')
    #context['regions'] = REGIONS
    #context['site_id'] = settings.CURRENT_SITE
    context['username'] = request.user.username
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()
    context['profile'] = profile
    def account_true(request):
        billing_account = profile.billing_account
        Limit_connection_service.create_limit_for_new_user(billing_account)
        context['billing_account'] = billing_account  #request.user.get_profile().billing_account #??????!!!!!!!!!!


        '''
        if profile.is_card or settings.CURRENT_SITE == 3:
            cur = connections[settings.BILLING_DB].cursor()
            context['Enable'] = False
            cur.execute("SELECT minutes FROM billservice_prepaid_minutes WHERE account_id=%s;", (profile.billing_account.id,))
            minutes = cur.fetchone()

            if minutes:
                context['Enable'] = True
                context['minutes'] = minutes[0]
            else:
                context['minutes'] = 0

            cur.execute("SELECT zone_id FROM billservice_prepaid_minutes WHERE account_id=%s;", (profile.billing_account.id,))
            telzone = cur.fetchone()
            transaction.commit_unless_managed(using=settings.BILLING_DB)
            if telzone:
                context['Enable'] = True
                if telzone[0] == 404:
                    context['Moskwa'] = True
            else:
                context['Enable'] = False
            context['From_card'] = True
            context['profile_data'] = ProfileCardDataForm(instance=profile)
            context['enable'] = True
        '''   
            
            
            
            
        #else:
        if not profile.is_juridical:
            # если зарегался как физическое лицо
            context['profile_data'] = ProfilePhisicalDataForm(instance=profile)
            context['address_physical'] = profile.address(ADDRESS_TYPE_PHYSICAL)
            context['address_physical_data'] = AddressPhysicalForm(instance=context['address_physical'])
            context['enable'] = False
            # добавим тут ему телефон, если еще нету
#                if billing_account.phones.count() == 0:
#                    log.add("automatic adding phone for non-juridical user '%s'" % request.user.username)
#                    # nextnum.add_number(billing_account.id, pwgen.random_pwd())
#                    TelNumber.create(
#                        account=billing_account,
#                        is_juridical=False,
#                    )

        else:
            context['profile_data'] = ProfileJuridicalDataForm(instance=profile)
            context['address_legal'] = profile.address(ADDRESS_TYPE_LEGAL)
            context['address_postal'] = profile.address(ADDRESS_TYPE_POSTAL)
            context['address_legal_data'] = AddressLegalForm(instance=context['address_legal'])
            context['address_postal_data'] = AddressPostalForm(instance=context['address_postal'])
        return context

    if not profile.activated_at:
        # Account wasn't created
        # Create forms
        response, _context = _activate_profile(request, profile)
        if response:
            return response
        else:
            try:
                profile = Profile.objects.get(user=request.user)
            except:
                pass
            if profile.activated_at:
                return HttpResponseRedirect(".")  # ерундовое немного решение. переделаю, когда будет переделываться процесс регистрации пользователей
            context.update(_context)
    if profile.activated_at:
        try:
            package_obj = Package_on_connection_of_service.objects.get(user=request.user,
                                                                      activate=False,
                                                                      deactivate=False)
        except Package_on_connection_of_service.DoesNotExist:
            package_obj = ''
        if not (profile.is_card or profile.is_hostel):
            if package_obj:
                url = package_obj.url_after_sign
                return HttpResponseRedirect(url)
        account_true(request)
    return context

def process_profile_forms(request, profile, activate, edit_form=False):
    def add_record_in_dict_juridical(profile_dict, profile_obj, address_legal_obj, address_postal_obj, spis_slugs):
        for f in corporate_form:
            if f.name in ('company_name', 'legal_form', "general_director", \
                          "sign_face", "sign_face_in_a_genitive_case", "sign_cause", 'bank_name', \
                          'settlement_account', 'correspondent_account', 'bik', 'bank_address', "kpp", \
                          'okpo', 'phones'):
                data_new_temp = f.data
                data_old_temp = eval('profile_obj.%s' % f.name)
                if data_new_temp != data_old_temp:
                    if not profile_dict.has_key('profile'):
                        profile_dict.update({'profile':{}})
                    profile_dict['profile'].update({f.name:f.data})
        for f in legal_address_form:
            if f.name in ('country', 'state', 'zipcode', \
                           'city', 'address_line', 'phones'):
                data_new_temp = f.data
                data_old_temp = eval('address_legal_obj.%s' % f.name)
                if data_new_temp != data_old_temp:
                    if not profile_dict.has_key('address_legal'):
                        profile_dict.update({'address_legal':{}})
                    profile_dict['address_legal'].update({f.name:f.data})
        for f in postal_address_form:
            if f.name in ('country', 'state', 'zipcode', \
                           'city', 'address_line', 'phones'):
                data_new_temp = f.data
                data_old_temp = eval('address_postal_obj.%s' % f.name)
                if data_new_temp != data_old_temp:
                    if not profile_dict.has_key('address_postal'):
                        profile_dict.update({'address_postal':{}})
                    profile_dict['address_postal'].update({f.name:f.data})
        successfully_create = create_package(request.user, \
                    reverse('account_profile_edit'), \
                    reverse('account_profile_edit'), \
                    '%s' % profile_dict, \
                    spis_slugs)
        if not successfully_create:
            raise Http404
        return profile_dict

    def add_record_in_dict_physical(profile_dict, profile_obj, address_physical_obj, spis_slugs):
        for f in personal_form:
            if f.name in ('last_name', 'first_name', 'second_name', \
                          'sex', 'birthday', 'pasport_serial', \
                          'when_given_out', 'by_whom_given_out', 'phones'):
                if f.name == 'sex':
                    data_new_temp = int(f.data)
                elif f.name in ('birthday', 'when_given_out'):
                    txtdate = f.data
                    data_new_temp = datetime.datetime.strptime(txtdate, "%Y-%m-%d").date()
                else:
                    data_new_temp = f.data
                data_old_temp = eval('profile_obj.%s' % f.name)
                if data_new_temp != data_old_temp:
                    if not profile_dict.has_key('profile'):
                        profile_dict.update({'profile':{}})
                    profile_dict['profile'].update({f.name:f.data})
        for f in physical_address_form:
            if f.name in ('country', 'state', 'zipcode', \
                          'city', 'address_line', 'phones'):
                data_new_temp = f.data
                data_old_temp = eval('address_physical_obj.%s' % f.name)
                if data_new_temp != data_old_temp:
                    if not profile_dict.has_key('address_physical'):
                        profile_dict.update({'address_physical':{}})
                    profile_dict['address_physical'].update({f.name:f.data})
        successfully_create = create_package(request.user, \
                    reverse('account_profile_edit'), \
                    reverse('account_profile_edit'), \
                    '%s' % profile_dict, \
                    spis_slugs)
        if not successfully_create:
            raise Http404
        return profile_dict


    # объявление переменных
    url = ''
    saved = False
    if request.method == "POST":

        if not profile.is_juridical:  # если физическое лицо
            address_physical_obj = ''
            str_physical_address_form_base = ''
            address_temp = profile.address(ADDRESS_TYPE_PHYSICAL)
            address_physical_obj = copy.copy(address_temp)
            profile_obj = copy.copy(profile)
            # получаем форму для юр.лица исходя из данных в profile
            corporate_form = ProfileJuridicalDataForm(instance=profile, prefix='corporate')
            # получаем форму для физ.лица исходя из данных в profile
            personal_form_base = ProfilePhisicalDataForm(instance=profile, prefix='personal')
            str_personal_form_base = '%s' % personal_form_base
            # получаем форму для физ.лица исходя из данных request.POST
            personal_form = ProfilePhisicalDataForm(request.POST.copy(), request.FILES, instance=profile, prefix='personal')
            str_personal_form = '%s' % personal_form
            # получаем форму с адресом физ.лица исходя из данных request.POST
            physical_address_form = AddressPhysicalForm(request.POST.copy(), prefix='address_physical')
            str_physical_address_form = '%s' % physical_address_form
            # если у пользователя заполнен адрес, иначе у него сейчас регистрация
            if address_physical_obj:
                physical_address_form_base = AddressPhysicalForm(instance=address_physical_obj, prefix='address_physical')
                str_physical_address_form_base = '%s' % physical_address_form_base
            legal_address_form = AddressLegalForm(prefix='address_legal')
            postal_address_form = AddressPostalForm(prefix='address_postal')
            # проверяем на валидность две формы и проверяем были ли изменены хоть какие-нибудь данные
            if 2 == len(filter(lambda x: x.is_valid(), [personal_form, physical_address_form])) \
                and ((str_personal_form_base != str_personal_form) \
                or (str_physical_address_form_base != str_physical_address_form)):
                if edit_form:
                    profile_dict = {}
                    spis_slugs = []
                    if not address_temp:
                        address = physical_address_form.save()
                        profile.addresses.clear()
                        profile.addresses.add(address)
                        profile.save()
                        address_physical_obj = copy.copy(address)
                    for f in personal_form:
                        if f.name in ('last_name', 'first_name', 'second_name'):
                            data_new = f.data
                            data_old = eval('profile_obj.%s' % f.name)
                            if data_new != data_old:
                                findocsigned_queryset = FinDocSigned.objects.filter(Q(signed_by=request.user) & \
                                    (Q(findoc__slug='telematic_services_contract') | Q(findoc__slug='telematic_data_centr') | \
                                     Q(findoc__slug='localphone_services_contract') | Q(findoc__slug='dogovor_oferta')) & Q(cancellation_date=None))
                                for findocsigned_obj in findocsigned_queryset:
                                    if findocsigned_obj.findoc.slug in ['telematic_data_centr', 'telematic_services_contract', 'localphone_services_contract']:
                                        spis_slugs.append('remove_%s' % findocsigned_obj.findoc.slug)
                                    elif findocsigned_obj.findoc.slug in ['dogovor_oferta']:
                                        if profile_dict.has_key('dogovor_oferta'):
                                            spis_findoc_sign = profile_dict['dogovor_oferta']
                                            spis_findoc_sign.append(findocsigned_obj.id)
                                            profile_dict.update({'dogovor_oferta':spis_findoc_sign})
                                        else:
                                            profile_dict.update({'dogovor_oferta':[findocsigned_obj.id]})
                                        spis_slugs.append('remove_%s' % findocsigned_obj.findoc.slug)
                                if spis_slugs:
                                    profile_dict = add_record_in_dict_physical(profile_dict, profile_obj, \
                                                                      address_physical_obj, spis_slugs)
                                    return locals(), saved, reverse('account_profile_edit')
                    for f in personal_form:
                        if f.name not in ('last_name', 'first_name', 'second_name', 'sex', 'birthday'):
                            if f.name in ('when_given_out'):
                                txtdate = f.data
                                data_new = datetime.datetime.strptime(txtdate, "%Y-%m-%d").date()
                            else:
                                data_new = f.data
                            data_old = eval('profile_obj.%s' % f.name)
                            if data_new != data_old:
                                for slug in FINDOCS_NOT_TO_DELETE:
                                    findocsigned_queryset = FinDocSigned.objects.filter(signed_by=request.user, findoc__slug=slug, cancellation_date=None)
                                    if findocsigned_queryset:
                                        spis_slugs.append(slug)
                                if spis_slugs:
                                    profile_dict.update({'spis_slugs':spis_slugs})
                                    profile_dict = add_record_in_dict_physical(profile_dict, profile_obj, \
                                                                      address_physical_obj, ['change_of_requisites'])
                                    return locals(), saved, reverse('account_profile_edit')
                    for f in physical_address_form:
                        if f.name in ('country', 'state', 'zipcode', \
                                       'city', 'address_line', 'phones'):
                            data_new_temp = f.data
                            data_old_temp = eval('address_physical_obj.%s' % f.name)
                            if data_new_temp != data_old_temp:
                                for slug in FINDOCS_NOT_TO_DELETE:
                                    findocsigned_queryset = FinDocSigned.objects.filter(signed_by=request.user, findoc__slug=slug, cancellation_date=None)
                                    if findocsigned_queryset:
                                        spis_slugs.append(slug)
                                if spis_slugs:
                                    profile_dict.update({'spis_slugs':spis_slugs})
                                    profile_dict = add_record_in_dict_physical(profile_dict, profile_obj, \
                                                                      address_physical_obj, ['change_of_requisites'])
                                    return locals(), saved, reverse('account_profile_edit')


                address = physical_address_form.save()
                profile = personal_form.save(commit=False)
                if activate:
                    profile.user = request.user
                    profile.activated_at = datetime.datetime.now()
                profile.save()
                profile.addresses.clear()
                profile.addresses.add(address)
                saved = True
        else:
            # объявление переменных
            address_legal_obj = ''
            address_postal_obj = ''
            str_legal_address_form_base = ''
            str_postal_address_form_base = ''
            address_temp = profile.address(ADDRESS_TYPE_LEGAL)
            address_legal_obj = copy.copy(address_temp)
            address_temp = profile.address(ADDRESS_TYPE_POSTAL)
            address_postal_obj = copy.copy(address_temp)
            profile_obj = copy.copy(profile)
            # получаем форму для физ.лица исходя из данных в profile
            personal_form = ProfilePhisicalDataForm(instance=profile, prefix='personal')
            # получаем форму для юр.лица исходя из данных в profile
            corporate_form_base = ProfileJuridicalDataForm(instance=profile, prefix='corporate')
            str_corporate_form_base = '%s' % corporate_form_base
            # получаем форму для юр.лица исходя из данных request.POST
            corporate_form = ProfileJuridicalDataForm(request.POST.copy(), instance=profile, prefix='corporate')
            str_corporate_form = '%s' % corporate_form

            # получаем форму с юр.адресом исходя из данных request.POST
            legal_address_form = AddressLegalForm(request.POST.copy(), prefix='address_legal')
            str_legal_address_form = '%s' % legal_address_form
            # если у пользователя заполнен юр.адрес, иначе у него сейчас регистрация
            if address_legal_obj:
                legal_address_form_base = AddressLegalForm(instance=address_legal_obj, prefix='address_legal')
                str_legal_address_form_base = '%s' % legal_address_form_base
            # получаем форму с почт.адресом исходя из данных request.POST
            postal_address_form = AddressPostalForm(request.POST.copy(), prefix='address_postal')
            str_postal_address_form = '%s' % postal_address_form
            # если у пользователя заполнен почт.адрес, иначе у него сейчас регистрация
            if address_postal_obj:
                postal_address_form_base = AddressPostalForm(instance=address_postal_obj, prefix='address_postal')
                str_postal_address_form_base = '%s' % postal_address_form_base
            # получаем форму с физ.адресом исходя из данных profile
            physical_address_form = AddressPhysicalForm(prefix='address_physical')
            # проверяем на валидность две формы и проверяем были ли изменены хоть какие-нибудь данные
            if 3 == len(filter(lambda x: x.is_valid(), [corporate_form, legal_address_form, postal_address_form])) \
                and ((str_corporate_form_base != str_corporate_form) \
                     or (str_legal_address_form_base != str_legal_address_form) \
                     or (str_postal_address_form_base != str_postal_address_form)):

                if edit_form:
                    profile_dict = {}
                    spis_slugs = []
                    if not address_legal_obj:
                        address = legal_address_form.save()
                        profile.addresses.clear()
                        profile.addresses.add(address)
                        profile.save()
                        address_legal_obj = copy.copy(address)
                    if not address_postal_obj:
                        address = postal_address_form.save()
                        profile.addresses.clear()
                        profile.addresses.add(address)
                        profile.save()
                        address_postal_obj = copy.copy(address)
                    for f in corporate_form:
                        if f.name in ('company_name', 'legal_form', 'bank_address', 'kpp'):
                            data_new = f.data
                            data_old = eval('profile_obj.%s' % f.name)
                            if data_new != data_old:
                                findocsigned_queryset = FinDocSigned.objects.filter(Q(signed_by=request.user) & \
                                    (Q(findoc__slug='telematic_services_contract') | Q(findoc__slug='telematic_data_centr') | \
                                     Q(findoc__slug='localphone_services_contract')) & Q(cancellation_date=None))
                                for findocsigned_obj in findocsigned_queryset:
                                    if findocsigned_obj.findoc.slug in ['telematic_data_centr', 'telematic_services_contract', 'localphone_services_contract']:
                                        spis_slugs.append('remove_%s' % findocsigned_obj.findoc.slug)
                                if spis_slugs:
                                    profile_dict = add_record_in_dict_juridical(profile_dict, profile_obj, \
                                                                      address_legal_obj, address_postal_obj, \
                                                                      spis_slugs)
                                    return locals(), saved, reverse('account_profile_edit')
                    for f in corporate_form:
                        if f.name not in ('company_name', 'legal_form', 'bank_address', 'kpp', \
                                          "general_director", "sign_face", "sign_face_in_a_genitive_case", "sign_cause"):
                            data_new = f.data
                            data_old = eval('profile_obj.%s' % f.name)
                            if data_new != data_old:
                                for slug in FINDOCS_NOT_TO_DELETE:
                                    findocsigned_queryset = FinDocSigned.objects.filter(signed_by=request.user, findoc__slug=slug, cancellation_date=None)
                                    if findocsigned_queryset:
                                        spis_slugs.append(slug)
                                if spis_slugs:
                                    profile_dict.update({'spis_slugs':spis_slugs})
                                    profile_dict = add_record_in_dict_juridical(profile_dict, profile_obj, \
                                                                      address_legal_obj, address_postal_obj, \
                                                                      ['change_of_requisites'])
                                    return locals(), saved, reverse('account_profile_edit')
                    for f in legal_address_form:
                        if f.name in ('country', 'state', 'zipcode', \
                                       'city', 'address_line', 'phones'):
                            data_new_temp = f.data
                            data_old_temp = eval('address_legal_obj.%s' % f.name)
                            if data_new_temp != data_old_temp:
                                for slug in FINDOCS_NOT_TO_DELETE:
                                    findocsigned_queryset = FinDocSigned.objects.filter(signed_by=request.user, findoc__slug=slug, cancellation_date=None)
                                    if findocsigned_queryset:
                                        spis_slugs.append(slug)
                                if spis_slugs:
                                    profile_dict.update({'spis_slugs':spis_slugs})
                                    profile_dict = add_record_in_dict_juridical(profile_dict, profile_obj, \
                                                                      address_legal_obj, address_postal_obj, \
                                                                      ['change_of_requisites'])
                                    return locals(), saved, reverse('account_profile_edit')
                    for f in postal_address_form:
                        if f.name in ('country', 'state', 'zipcode', \
                                       'city', 'address_line', 'phones'):
                            data_new_temp = f.data
                            data_old_temp = eval('address_postal_obj.%s' % f.name)
                            if data_new_temp != data_old_temp:
                                for slug in FINDOCS_NOT_TO_DELETE:
                                    findocsigned_queryset = FinDocSigned.objects.filter(signed_by=request.user, findoc__slug=slug, cancellation_date=None)
                                    if findocsigned_queryset:
                                        spis_slugs.append(slug)
                                if spis_slugs:
                                    profile_dict.update({'spis_slugs':spis_slugs})
                                    profile_dict = add_record_in_dict_juridical(profile_dict, profile_obj, \
                                                                      address_legal_obj, address_postal_obj, \
                                                                      ['change_of_requisites'])
                                    return locals(), saved, reverse('account_profile_edit')


                # start to populate profile
                address1 = legal_address_form.save()
                address2 = postal_address_form.save()
                profile = corporate_form.save(commit=False)
                if activate:
                    profile.user = request.user
                    profile.activated_at = datetime.datetime.now()
                profile.save()
                profile.addresses.clear()
                profile.addresses.add(address1)
                profile.addresses.add(address2)
                saved = True
    else:
        personal_form = ProfilePhisicalDataForm(instance=profile, prefix='personal')
        corporate_form = ProfileJuridicalDataForm(instance=profile, prefix='corporate')
        try:
            addr_legal = profile.addresses.get(address_type=ADDRESS_TYPE_LEGAL)
        except (Address.DoesNotExist, Address.MultipleObjectsReturned):
            addr_legal = None
        try:
            addr_postal = profile.addresses.get(address_type=ADDRESS_TYPE_POSTAL)
        except (Address.DoesNotExist, Address.MultipleObjectsReturned):
            addr_postal = None
        try:
            addr_physical = profile.addresses.get(address_type=ADDRESS_TYPE_PHYSICAL)
        except (Address.DoesNotExist, Address.MultipleObjectsReturned):
            addr_physical = None
        legal_address_form = AddressLegalForm(instance=addr_legal, prefix='address_legal')
        postal_address_form = AddressPostalForm(instance=addr_postal, prefix='address_postal')
        physical_address_form = AddressPhysicalForm(instance=addr_physical, prefix='address_postal')

    return locals(), saved, url

def _activate_profile(request, profile):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        account_type_select_form = AccountTypeSelectForm(request.POST)
        if account_type_select_form.is_valid():
            profile.is_juridical = account_type_select_form.cleaned_data['account_type'] == 'id_corporate'
    else:
        if profile.activated_at:
            if profile.is_juridical:
                account_type_select_form = AccountTypeSelectFormJuridical(request.POST)
            else:
                account_type_select_form = AccountTypeSelectFormPhysical(request.POST)
        else:
            account_type_select_form = AccountTypeSelectForm()
    context = {'account_type_select_form': account_type_select_form}
    context.update(process_profile_forms(request, profile, activate=True)[0])
    return None, context




@login_required
@decorator_for_sign_applications()
@render_to('account/profile_edit.html')
def account_profile_edit(request):
    print 'account_profile_edit'
    context = {}
    def get_form_profile(context, readonly, post=None):
        context['legal_address_form'] = AddressLegalForm(post, instance=addr_legal, readonly=readonly, prefix='address_legal')
        context['postal_address_form'] = AddressPostalForm(post, instance=addr_postal, readonly=readonly, prefix='address_postal')
        context['physical_address_form'] = AddressPhysicalForm(post, instance=addr_physical, readonly=readonly, prefix='address_postal')
        if package and not edit_profile:
            if profile.is_juridical:
                context['corporate_form'] = ProfileJuridicalDataForm(post, instance=profile, prefix='corporate', readonly=readonly)
            else:
                context['personal_form'] = ProfilePhisicalDataForm(post, instance=profile, prefix='personal', readonly=readonly)
        else:
            if profile.is_juridical:
                context['corporate_form_part'] = True
                context['corporate_form_main'] = ProfileJuridicalDataMainForm(post, instance=profile, prefix='corporate', readonly=True)
                context['corporate_form_additional'] = ProfileJuridicalDataAdditionalForm(post, instance=profile, prefix='corporate', readonly=readonly)
                context['corporate_form_ignored'] = ProfileJuridicalDataIgnoredForm(post, instance=profile, prefix='corporate', readonly=readonly)
            else:
                context['personal_form_part'] = True
                context['personal_form_not_edit'] = ProfilePhisicalNotEditForm(post, instance=profile, prefix='personal', readonly=True)
                context['personal_form_additional'] = ProfilePhisicalDataAdditionalForm(post, instance=profile, prefix='personal', readonly=readonly)
        return context

    def get_variable_address(address_type):
        try:
            variable = profile.addresses.get(address_type=address_type)
        except (Address.DoesNotExist, Address.MultipleObjectsReturned):
            variable = None
        return variable

    if request.user.get_profile().is_card:
        raise Http404
    profile = request.user.get_profile()
    package = False
    edit_profile = False
    context = {}
    context['action'] = ''
    context['package'] = package
    context['title'] = u'Редактирование данных учетной записи'
    context['current_view_name'] = 'account_profile'
    context['profile'] = profile
    context['access_to_personal_information'] = False if profile.access_to_personal_information else True
    context['edit_profile_page'] = True #for menu
    addr_legal = get_variable_address(ADDRESS_TYPE_LEGAL)
    addr_postal = get_variable_address(ADDRESS_TYPE_POSTAL)
    addr_physical = get_variable_address(ADDRESS_TYPE_PHYSICAL)
    try:
        package_obj = Package_on_connection_of_service.objects.get(user=request.user, activate=False, deactivate=False)
        package = True
        if package_obj.url_after_sign in ('%s' % reverse('account_profile_edit'),):
            data_temp = eval(package_obj.data)

            spis_slugs = data_temp['spis_slugs']
            del spis_slugs[0]
            if spis_slugs:
                data_temp['spis_slugs'] = spis_slugs
                successfully_create = create_package(request.user,
                                reverse('account_profile_edit'),
                                reverse('account_profile_edit'),
                                u'%s' % data_temp,
                                ['change_of_requisites'])
                if not successfully_create:
                    raise Http404
                else:
                    return HttpResponseRedirect(reverse('account_profile_edit'))
            request.POST = data_temp['request_post']
            edit_profile = True
            package_obj.activate = True
            package_obj.save()
        if edit_profile:
            if profile.is_juridical:
                context = get_form_profile(context, False, request.POST.copy())
                address1 = context['legal_address_form'].save()
                address2 = context['postal_address_form'].save()
                profile = context['corporate_form_additional'].save(commit=False)
                profile.save()
                profile.addresses.clear()
                profile.addresses.add(address1)
                profile.addresses.add(address2)
                request.notifications.add(u"Данные успешно изменены!", "success")
                return context
    except Package_on_connection_of_service.DoesNotExist:
        pass
    context['cancel'] = True if package else False
    readonly = True if package and not edit_profile else False
    if request.POST.get('submit'):
        print 'submit'
        context = get_form_profile(context, readonly, request.POST.copy())
        if package and not edit_profile:
            if profile.is_juridical:
                if 3 == len(filter(lambda x: x.is_valid(), [context['corporate_form'], context['legal_address_form'], context['postal_address_form']])):
                    address1 = context['legal_address_form'].save()
                    address2 = context['postal_address_form'].save()
                    profile = context['corporate_form'].save(commit=False)
                    profile.access_to_personal_information = True
                    profile.save()
                    profile.addresses.clear()
                    profile.addresses.add(address1)
                    profile.addresses.add(address2)
                    return HttpResponseRedirect(reverse('account_profile'))
                else:
                    request.notifications.add(u"Пожалуйста, заполните все поля!", "error")
            else:
                print 'physical person'
                
                if 2 == len(filter(lambda x: x.is_valid(), [context['personal_form'], context['physical_address_form']])):
                    address = context['physical_address_form'].save()
                    profile = context['personal_form'].save(commit=False)
                    profile.access_to_personal_information = True
                    profile.save()
                    profile.addresses.clear()
                    profile.addresses.add(address)
                    return HttpResponseRedirect(reverse('account_profile'))
                else:
                    request.notifications.add(u"Пожалуйста, заполните все поля!", "error")
        else:
            if profile.is_juridical:
                if 5 == len(filter(lambda x: x.is_valid(), [context['corporate_form_main'], context['corporate_form_additional'], context['corporate_form_ignored'],
                                                            context['legal_address_form'], context['postal_address_form']])):
                    create_dop_sogl = False
                    for fieldname in context['corporate_form_additional'].changed_data:
                        value = getattr(profile, fieldname)
                        if value:
                            create_dop_sogl = True
                            break
                    if not create_dop_sogl:
                        for fieldname in context['legal_address_form'].changed_data:
                            value = getattr(addr_legal, fieldname)
                            if value:
                                create_dop_sogl = True
                                break
                    print 'create_dop_sogl = %s' % create_dop_sogl
                    if create_dop_sogl:
                        spis_slugs = []
                        for slug in FINDOCS_NOT_TO_DELETE:
                            findocsigned_queryset = FinDocSigned.objects.filter(signed_by=request.user, findoc__slug=slug, cancellation_date=None)
                            if findocsigned_queryset:
                                spis_slugs.append(slug)
                        if spis_slugs:
                            data = {}
                            request_post = {}
                            for key, value in request.POST.iteritems():
                                request_post[key.encode("utf-8")] = value.encode("utf-8")
                            data['spis_slugs'] = spis_slugs
                            data['request_post'] = request_post
                            successfully_create = create_package(request.user,
                                            reverse('account_profile_edit'),
                                            reverse('account_profile_edit'),
                                            u'%s' % data,
                                            ['change_of_requisites'])
                            if not successfully_create:
                                raise Http404
                            else:
                                return HttpResponseRedirect(reverse('account_profile_edit'))
                    address1 = context['legal_address_form'].save()
                    address2 = context['postal_address_form'].save()
                    profile = context['corporate_form_additional'].save(commit=False)
                    profile.access_to_personal_information = True
                    profile.save()
                    profile.addresses.clear()
                    profile.addresses.add(address1)
                    profile.addresses.add(address2)
                    request.notifications.add(u"Данные успешно изменены!", "success")
                    return HttpResponseRedirect(reverse('account_profile_edit'))
                else:
                    request.notifications.add(u"Пожалуйста, заполните все поля!", "error")
            else:
                #if 3 == len(filter(lambda x: x.is_valid(), [context['personal_form_not_edit'], context['personal_form_additional'], context['physical_address_form']])):
                if 2 == len(filter(lambda x: x.is_valid(), [context['personal_form_not_edit'], context['personal_form_additional'], context['physical_address_form']])):
                    #address = context['physical_address_form'].save()
                    profile = context['personal_form_additional'].save(commit=False)
                    profile.access_to_personal_information = True
                    profile.save()
                    #profile.addresses.clear()
                    #profile.addresses.add(address)
                    request.notifications.add(u"Данные успешно изменены!", "success")
                    return HttpResponseRedirect(reverse('account_profile_edit'))
                else:
                    request.notifications.add(u"Пожалуйста, заполните все поля!", "error")
    elif request.POST.get('cancel'):
        package_obj.deactivate = True
        package_obj.save()
        return HttpResponseRedirect(reverse('account_profile'))
    else:
        context = get_form_profile(context, readonly)
    return context


@login_required
@render_to('account/change_password.html')
def account_change_password(request):
    if request.user.get_profile().is_card:
        raise Http404
    context = {'user':request.user}
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST.copy(), request=request)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            request.notifications.add(force_unicode(_(u'New password saved.')), 'success')
            return HttpResponseRedirect(get_base_url(request.user))
        else:
            request.notifications.add(force_unicode(_(u'Check form data.')), 'error')
            context['form'] = form
    else:
        form = ChangePasswordForm(request=request)
        context['form'] = form
    context['current_view_name'] = 'account_profile'
    context['change_password_page'] = True
    return context


class RQ2QS:  # @todo: Переделывать это. убрать нафиг и сделать обычный queryset
    def __init__(self, account_id, datetime, session_end,
                 caller_number=None, called_number=None,
                 download=None, filename=None, record=None,
                 group=None, call_length_type=1, call_type=1,
                 order_by='datetime', order_type='DESC',
                 tel_number=None):
        print 'filename = %s' % filename
        self.raw_query = ""
        self.account_id = account_id
        self.datetime = datetime
        self.session_end = session_end
        self.caller_number = caller_number
        self.called_number = called_number
        self.results = []
        self.count = 0
        self.have_results = False
        self.download = download
        self.group = group
        self.call_length_type = call_length_type
        self.call_type = call_type
        self.order_by = order_by
        self.order_type = order_type
        self.link = "/media/billed_calls_files/balance.csv"
        self.filename = filename
        self.record = record
        self.tel_number = tel_number

    def make_query2(self):
        where = ""
        if self.record:
            table = "billservice_recordtransaction"
        else:
            table = "billservice_phonetransaction"
        if self.datetime:
            where += "\"%s\".\"datetime\" >= '%s'" % (table, self.datetime)

        if self.session_end:
            if where: where += " AND"
            where += " \"%s\".\"session_end\" <= '%s'" % (table, self.session_end)

        if self.group:
            if where: where += " AND"
            where += (" (\"%s\".\"caller_group_number\" LIKE '%s' ) ") % (table, self.group)

        if self.caller_number:
            if where:
                where += " AND"
            where += " \"%s\".\"caller_number\" LIKE '%s'" % (table, RQ2QS.double_proc(self.caller_number))

        if self.called_number:
            if where:
                where += " AND"
            where += " \"%s\".\"called_number\" LIKE '%s'" % (table, RQ2QS.double_proc(self.called_number))

        if self.account_id:
            if where:
                where += " AND"
            where += " (\"%s\".\"account_id\" = %s OR \"%s\".\"called_account_id\" = %s) " % (table,self.account_id,
                                                                                              table, self.account_id)

        if self.call_type:
            if self.call_type == "2":
                if where:
                    where += " AND"
                where += " \"%s\".\"account_id\" <> %s" % (table, self.account_id)
            elif self.call_type == "3":
                if where:
                    where += " AND"
                where += " \"%s\".\"account_id\" = %s" % (table, self.account_id)

        if self.call_length_type:
            if self.call_length_type == "2":
                if where:
                    where += " AND"
                where += " \"%s\".\"billable_session_length\" = 0" % table
            elif self.call_length_type == "3":
                if where:
                    where += " AND"
                where += " \"%s\".\"billable_session_length\" > 0" % table
        return where

    @staticmethod
    def double_proc(s):
            res = ""
            for i in xrange(len(s)):
                if s[i] == "*":
                    res += "%%"
                else:
                    res += s[i]
            return res

    def make_query(self, limit=None, offset=None, count=False):
        def get_query_from_array(first_text, separator, array):
            if len(array) > 0:
                query = first_text
                for index, item in enumerate(array):
                    if index > 0:
                        query += " %s" % separator
                    query += " %s" % item
                return query
            else:
                return ""
        ###################### Параметры ########################
        where_list = []
        sub_where_list = []
        order = []
        sub_join = []
        sub_select = []
        params = {}
        select = []
        ##################### Запрос ############################
        query = "SELECT %(select)s FROM (SELECT %(sub_select)s FROM %(table)s %(sub_join)s %(sub_where)s) AS main_table %(where)s %(order)s"
        if self.record:
            params.update(table="billservice_recordtransaction AS sub_table")
        else:
            params.update(table="billservice_phonetransaction AS sub_table")
        if count:
            # Статистика
            if not self.record:
                select.append("""count(main_table.*) AS call_count,
                                 sum(main_table.billable_session_length) AS call_time,
                                 sum(CASE WHEN main_table.is_800 THEN
                                         CASE WHEN main_table.account_id = %(account_id)s THEN 0.0 ELSE main_table.summ END
                                     ELSE
                                         CASE WHEN main_table.account_id = %(account_id)s THEN main_table.summ ELSE 0.0 END
                                     END) AS call_price,
                                 sum(CASE WHEN main_table.billable_session_length > 0 THEN 1 ELSE 0 END ) AS call_held
                              """)
            else:
                select.append("""count(main_table.*) AS call_count,
                                 sum(main_table.billable_session_length) AS call_time,
                                 sum(main_table.summ) AS call_price,
                                 sum(CASE WHEN main_table.billable_session_length > 0 THEN 1 ELSE 0 END ) AS call_held
                              """)
        else:
            # если called_account_id != нашему => summ=price=0.0
            if not self.record:
                select.append("""*,
                    CASE WHEN main_table.is_800 THEN
                        CASE WHEN main_table.account_id = %(account_id)s THEN 0.0 ELSE main_table.price END
                    ELSE
                        CASE WHEN main_table.account_id = %(account_id)s THEN main_table.price ELSE 0.0 END
                    END AS price,
                    CASE WHEN main_table.is_800 THEN
                        CASE WHEN main_table.account_id = %(account_id)s THEN 0.0 ELSE main_table.summ END
                    ELSE
                        CASE WHEN main_table.account_id = %(account_id)s THEN main_table.summ ELSE 0.0 END
                    END AS summ""")
            else:
                select.append("""*,
                    main_table.price AS price,
                    main_table.summ AS summ""")
            if not self.record:  # Редиректы
                select.append("""(SELECT record_talk.id
                                  FROM billservice_phonetransaction
                                  LEFT OUTER JOIN record_talk
                                  ON record_talk.billing_account_id = %(account_id)s
                                     AND record_talk.number = CASE WHEN billservice_phonetransaction.flag_record_out
                                                                   THEN billservice_phonetransaction.caller_number
                                                                   ELSE CASE WHEN billservice_phonetransaction.answer_number <> null
                                                                                  AND billservice_phonetransaction.answer_number <> ''
                                                                                  AND char_length(billservice_phonetransaction.answer_number) = 7
                                                                             THEN billservice_phonetransaction.answer_number
                                                                             ELSE billservice_phonetransaction.called_number
                                                                        END
                                                              END
                                  WHERE (billservice_phonetransaction.answer_number = main_table.answer_number
                                         OR billservice_phonetransaction.caller_number = main_table.caller_number)
                                        AND billservice_phonetransaction.datetime >= (main_table.datetime - "time"('00:00:02'))
                                        AND billservice_phonetransaction.datetime <= (main_table.datetime + "time"('00:00:02'))
                                        AND (char_length(billservice_phonetransaction.caller_number) = 7
                                             OR char_length(billservice_phonetransaction.called_number) = 7
                                             OR char_length(billservice_phonetransaction.answer_number) = 7)
                                        AND billservice_phonetransaction.id <> main_table.id
                                  LIMIT 1
                                 ) AS redirect_record_id
                              """)
                select.append("""(SELECT record_talk.enabled
                                  FROM billservice_phonetransaction
                                  LEFT OUTER JOIN record_talk
                                  ON record_talk.billing_account_id = %(account_id)s
                                     AND record_talk.number = CASE WHEN billservice_phonetransaction.flag_record_out
                                                                   THEN billservice_phonetransaction.caller_number
                                                                   ELSE CASE WHEN billservice_phonetransaction.answer_number <> null
                                                                                  AND billservice_phonetransaction.answer_number <> ''
                                                                                  AND char_length(billservice_phonetransaction.answer_number) = 7
                                                                             THEN billservice_phonetransaction.answer_number
                                                                             ELSE billservice_phonetransaction.called_number
                                                                        END
                                                              END
                                  WHERE (billservice_phonetransaction.answer_number = main_table.answer_number
                                         OR billservice_phonetransaction.caller_number = main_table.caller_number)
                                        AND billservice_phonetransaction.datetime >= (main_table.datetime - "time"('00:00:02'))
                                        AND billservice_phonetransaction.datetime <= (main_table.datetime + "time"('00:00:02'))
                                        AND (char_length(billservice_phonetransaction.caller_number) = 7
                                             OR char_length(billservice_phonetransaction.called_number) = 7
                                             OR char_length(billservice_phonetransaction.answer_number) = 7)
                                        AND billservice_phonetransaction.id <> main_table.id
                                  LIMIT 1
                                 ) AS redirect_record_enabled
                              """)
                select.append("""(SELECT file FROM billservice_phonetransaction
                                  WHERE billservice_phonetransaction.datetime >= '%(datetime)s'
                                        AND (billservice_phonetransaction.answer_number = main_table.answer_number
                                             OR billservice_phonetransaction.caller_number = main_table.caller_number)
                                        AND billservice_phonetransaction.datetime >= (main_table.datetime - "time"('00:00:02'))
                                        AND billservice_phonetransaction.datetime <= (main_table.datetime + "time"('00:00:02'))
                                        AND billservice_phonetransaction.id <> main_table.id
                                  LIMIT 1
                                 ) AS redirect_file
                              """)
                select.append("""(SELECT answer_number FROM billservice_phonetransaction
                                  WHERE billservice_phonetransaction.datetime >= '%(datetime)s'
                                        AND (billservice_phonetransaction.answer_number = main_table.answer_number
                                             OR billservice_phonetransaction.caller_number = main_table.caller_number)
                                        AND billservice_phonetransaction.datetime >= (main_table.datetime - "time"('00:00:02'))
                                        AND billservice_phonetransaction.datetime <= (main_table.datetime + "time"('00:00:02'))
                                        AND billservice_phonetransaction.id <> main_table.id
                                  LIMIT 1
                                 ) AS redirect_answer_user
                              """)
        ######################## ?sub_where ######################
        if self.record:
            sub_where_list.append("sub_table.answer_user IN (SELECT username FROM internal_numbers as n WHERE n.account_id = %(account_id)s)")
        else:
            sub_where_list.append("(sub_table.account_id = %(account_id)s OR sub_table.called_account_id = %(account_id)s)")
        params.update(account_id=self.account_id)
        sub_where_list.append("sub_table.datetime >= '%(datetime)s'")
        params.update(datetime=self.datetime)
        sub_where_list.append("sub_table.session_end <= '%(session_end)s'")
        params.update(session_end=self.session_end)
        # Вызывающий абонент
        if self.caller_number:
            sub_where_list.append("sub_table.caller_number = '%(caller_number)s'")
            params.update(caller_number=self.caller_number)
        # Вызываемый абонент
        if self.called_number:
            sub_where_list.append("sub_table.called_number = '%(called_number)s'")
            params.update(called_number=self.called_number)
        # Звонки С нулевой продолжительностью
        if self.call_length_type == '2':
            sub_where_list.append("sub_table.billable_session_length = 0")
        # Звонки Состоявшиеся
        if self.call_length_type == '3':
            sub_where_list.append("sub_table.billable_session_length > 0")
        if self.tel_number:
            sub_where_list.append("(sub_table.caller_number = '%(tel_number)s' OR sub_table.called_number = '%(tel_number)s')")
            params.update(tel_number=self.tel_number)
        ####################### ?sub_join #############################
        if not count:
            if not self.record:
                sub_join.append("""LEFT OUTER JOIN record_talk
                                   ON record_talk.billing_account_id = %(account_id)s
                                      AND record_talk.number = CASE WHEN sub_table.flag_record_out
                                                                    THEN sub_table.caller_number
                                                                    ELSE CASE WHEN sub_table.answer_number <> null
                                                                                   AND sub_table.answer_number <> ''
                                                                                   AND char_length(sub_table.answer_number) = 7
                                                                              THEN sub_table.answer_number
                                                                              ELSE sub_table.called_number
                                                                         END
                                                              END
                                """)
                sub_select.append("record_talk.enabled AS record_enabled")
        ######################## ?sub_select ##########################
        sub_select.append("sub_table.*")
        # Имя группы
        sub_select.append("""CASE WHEN sub_table.account_id = %(account_id)s
                                  THEN sub_table.caller_group_number
                                  ELSE sub_table.called_group_number
                             END AS group_name
                          """)
        # Исходящий
        if not count:
            sub_select.append("CASE WHEN sub_table.called_account_id = %(account_id)s THEN FALSE ELSE TRUE END AS outgoing")
            # Зона или answer_number
            if self.record:
                sub_select.append("""CASE WHEN sub_table.account_id = %(account_id)s
                                          THEN (SELECT tel_zones.name
                                                FROM tel_zones
                                                WHERE  tel_zones.id = sub_table.tel_zone_id)
                                          ELSE sub_table.answer_user
                                     END AS zone
                                  """)
            else:
                sub_select.append("""CASE WHEN sub_table.account_id = %(account_id)s
                                          THEN (SELECT tel_zones.name
                                                FROM tel_zones
                                                WHERE  tel_zones.id = sub_table.tel_zone_id)
                                          ELSE sub_table.answer_number
                                     END AS zone
                                  """)
            # id записываемого номера в record_talk
            if not self.record and not count:
                sub_select.append("record_talk.id AS record_id")
        ######################## ?where ###############################
        # Группа
        if self.group:
            if self.group == u"без группы":
                where_list.append("main_table.group_name ISNULL")
            else:
                where_list.append("main_table.group_name LIKE '%%%%%(group)s%%%%'")
                params.update(group=self.group)
        # Тип звонка (все/вх/исх)
        # Входящий
        if self.call_type == "2":
            where_list.append("main_table.account_id <> %(account_id)s")
        # Исходящий
        if self.call_type == "3":
            where_list.append("main_table.account_id = %(account_id)s")
        ###################### ?order #################################
        if not count:
            if self.order_by in ("caller_number", "called_number", "zone", "group_name", "datetime", "session_end", "billable_session_length", "price", "summ"):
                if self.order_type == "DESC":
                    order.append("main_table.%(order_by)s DESC")
                else:
                    order.append("main_table.%(order_by)s")
                params.update(order_by=self.order_by)
            order.append("main_table.id")
        where_q = get_query_from_array("WHERE", "AND", where_list) % params
        sub_where_q = get_query_from_array("WHERE", "AND", sub_where_list) % params
        order_q = get_query_from_array("ORDER BY", ",", order) % params
        sub_join_q = get_query_from_array("", "", sub_join) % params
        sub_select_q = get_query_from_array("", ",", sub_select) % params
        select_q = get_query_from_array("", ",", select) % params
        params.update(where=where_q)
        params.update(sub_where=sub_where_q)
        params.update(order=order_q)
        params.update(sub_join=sub_join_q)
        params.update(sub_select=sub_select_q)
        params.update(select=select_q)
        query = query % params
        if limit:
            query += " LIMIT %s" % limit
        if offset:
            offset += " OFFSET %s" % offset
        return query
    '''
    def get_results(self):
        self.raw_query = self.make_query()
        try:
            # print "############################################ RAW = ", self.raw_query
            #self.results = BillservicePhoneTransaction.objects.db_manager(settings.BILLING_DB).raw(self.raw_query)[:]
            if self.order_by in ("caller_number", "called_number", "zone", "group_name", "datetime", "session_end", "billable_session_length", "price", "summ"):
                if self.order_type == "DESC":
                    order = "-" + self.order_by
                else:
                    order = self.order_by
            else:
                order = "id"
            if self.record:
                self.results = BillserviceRecordTransaction.objects.db_manager(settings.BILLING_DB).prefetch_related("tel_zone").\
                                    extra(
                                          where=[self.make_query2()],
                                          select={"caller_group_number": "caller_group_number",
                                                  "file": "file",
                                                  "answer_user": "answer_user"
                                                  },
                                          order_by=[order]
                                         )
            else:
                self.results = BillservicePhoneTransaction.objects.db_manager(settings.BILLING_DB).prefetch_related("tel_zone").\
                                    extra(
                                          where=[self.make_query2()],
                                          select={"caller_group_number":"caller_group_number",
                                                  "disconnect_code" : """SELECT disconnect_rus FROM disconnect_code
                                                    WHERE disconnect_code.disconnect_eng=billservice_phonetransaction.disconnect_code"""},
                                          order_by=[order]
                                         )

        except Exception, e:
            print "tyt"
            print e
       
        if not self.record:
            for res in self.results:
                try:
                    new_code = Disconnect_code.objects.get(disconnect_eng=res.disconnect_code).disconnect_rus
                    res.disconnect_code = new_code
                except Disconnect_code.DoesNotExist:
                    res.disconnect_code = u"Неизвестно"
        

        if self.download:
            fname = self.filename
            full_fname = settings.MEDIA_ROOT + os.sep + "billed_calls_files" + os.sep + fname
            link = "/media/billed_calls_files/" + fname
            all_session_length = 0
            all_summ = 0
            call_count = 0
            time = 0
            f = open(full_fname, "w")
#             if not self.record:
            text = 'Вызывающий абонент;  Вызываемый абонент; Зона / Номер, принявший звонок; Группа; Начало звонка; Конец звонка; Длительность разговора(сек.); Цена за минуту; Списано(RUR); \n'
            for tex in self.results:
                text += "%s" % str(tex.caller_number) + "; "
                text += "%s" % str(tex.called_number) + "; "
                if tex.zone:
                    try:
                        text += "%s" % str(tex.zone) + "; "
                    except:
                        text += tex.zone.encode('utf8') + "; "
                else:
                    text += "; "
                if tex.group_name:
                    try:
                        text += "%s" % str(tex.group_name) + "; "
                    except:
                        text += tex.group_name.encode('utf8') + "; "
                else:
                    text += "; "
                text += "%s" % str(tex.datetime) + "; "
                text += "%s" % str(tex.session_end) + "; "
                text += "%s" % str(tex.billable_session_length) + "; "
                text += "%s" % str(tex.price) + "; "
                text += "%s" % str(tex.summ) + "; " + "\n"
                all_session_length += float(tex.billable_session_length)
                time += tex.billable_session_length
                all_summ += float(tex.summ)
                call_count += 1
#             else:
#                 text = u'Вызывающий абонент;  Вызываемый абонент; Начало звонка; Конец звонка; Длительность разговора(сек.); Цена за минуту; Списано(RUR); \n'
#                 for tex in self.results:
#                     text += "%s" % str(tex.caller_number) + "; " + "%s" % str(tex.called_number) + "; " + "%s" % str(tex.datetime) + "; " + "%s" % str(tex.session_end) + "; " + "%s" % str(tex.billable_session_length) + "; " + "%s" % str(tex.price) + "; " + "%s" % str(tex.summ) + "; " + "\n"
#                     all_session_length += float(tex.billable_session_length)
#                     all_summ += float(tex.summ)
#                     call_count += 1
            time_sec = int(round(time % 60));
            if time_sec < 10:
                time_sec = "0%s" % time_sec
            text += '\n\n\nВсего звонков:; ' + str(call_count) + ";\n"
            text += 'Средняя продолжительность разговора:; ' + (str(datetime.timedelta(seconds=int(all_session_length / call_count))) if call_count > 0 else '0') + ";\n"
            text += 'Общая продолжительность разговора:; ' + str(datetime.timedelta(seconds=int(all_session_length))) + ";\n"
            text += 'Всего списано(RUR):; '
            text += str(round(all_summ, 2)) + ";\n"
            f.write(text.decode('utf8').encode('cp1251'))
            f.close()
        self.count = self.results.count()
        self.have_results = True
    '''
    def __getitem__(self, *args, **kwargs):
        sl = args[0]
        if type(sl) is slice:
            min = sl.start
            max = sl.stop
            if not self.have_results:
                self.get_results()
            return self.results[min:max]
        else:
            raise Exception("RQ2QS.__getitem__() have'nt a valid parameters!")

    def __len__(self):
        if not self.have_results:
            self.get_results()
        return self.count

@login_required
@render_to('account/balance.html')
def account_balance(request):

    profile = request.user.get_profile()
    if 'filter' in request.GET:
        form = BalanceFilterForm(request.GET)
    else:
        form = BalanceFilterForm()
    filename = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + "%s" % request.user + ".csv"
    link = "/media/billed_calls_files/%s" % filename
    date_from = first_date()
    date_to = last_date()
    caller_number = called_number = group = call_type = call_length_type = ""
    order_by = "datetime"
    order_type = "DESC"
    if "order_by" in request.GET:
            order_by = request.GET.get("order_by")
    if "order_type" in request.GET:
            order_type = request.GET.get("order_type")
    download = False
    if request.GET.get("download"):
        download = True
    if form.is_valid():
        date_from = form.cleaned_data["date_from"]
        date_to = form.cleaned_data["date_to"]
        if date_from and date_to:
            if date_from > date_to:
                request.notifications.add(_(u"You have selected an incorrect date interval!"), "warning")
                return HttpResponseRedirect("/account/balance/")
            else:
                if (date_to.month - date_from.month) > 2:
                    request.notifications.add("Разница между 'дата с' и  'дата по' должна быть не более двух месяцев!", "warning")
                    return HttpResponseRedirect("/account/balance/")
                if date_from < (datetime.date.today() - timedelta(days=365)):
                    request.notifications.add("'Дата с' должна быть не более чем год назад!", "warning")
                    return HttpResponseRedirect("/account/record_balance/")
        caller_number = form.cleaned_data["caller_number"]
        called_number = form.cleaned_data["called_number"]
        group = form.cleaned_data["group"]
        call_length_type = form.cleaned_data["call_length_type"]
        call_type = form.cleaned_data["call_type"]

    if date_to:
        date_to += timedelta(days=1)

    rq = RQ2QS(# !!!!!!!!!! вероятно здесь все же стоит использовать обычный QuerySet,
               # но со всякими дополнительными параметрами, вроде QuerySet.extra(...)
               # (для увеличения производительности)
        profile.billing_account_id,
        date_from,
        date_to,
        caller_number=caller_number,
        called_number=called_number,
        download=download,
        filename=filename,
        group=group,
        call_length_type=call_length_type,
        call_type=call_type,
        order_by=order_by,
        order_type=order_type
    )
    '''
    record_tarif = Record_talk_activated_tariff.objects.filter(Q(billing_account_id=profile.billing_account_id) & \
                                                                            Q(date_activation__lt=datetime.datetime.now()) & \
                                                                            (Q(date_deactivation=None) | \
                                                                              Q(date_deactivation__gt=datetime.datetime.now())))
    '''
    user_with_record_tarif = False
    '''
    if record_tarif:
        user_with_record_tarif = True
    '''
    ######################### ?подсчет статистики ################################
    statistics = {}
    cur = connections[settings.BILLING_DB].cursor()
    cur.execute("""SELECT count(id) as call_count, sum(billable_session_length) as call_time, sum(summ) as call_price,
                sum(CASE WHEN billable_session_length > 0 THEN 1 ELSE 0 END ) AS call_held FROM
                  billservice_phonetransaction """ + ("WHERE " + rq.make_query2() if rq.make_query2() else ""))
    rq_stat = cur.fetchone()
    transaction.commit_unless_managed(using=settings.BILLING_DB)

    if rq_stat[0] > 0:
        stat_count = rq_stat[0]
        stat_time = "%s:%s" % divmod(int(rq_stat[1] / rq_stat[0]), 60)
        stat_price = rq_stat[2]
        stat_count_held = 100.0 / float(stat_count) * rq_stat[3]
        stat_total_time = "%s" % (rq_stat[1] / 60)

        statistics = {
                      'count' : stat_count,
                      'count_held' : stat_count_held,
                      'time' : stat_time,
                      'price' : stat_price,
                      'total_time' : stat_total_time
                      }
    else:
        statistics = None
    query = get_query_string(request, exclude=("page",))
    paginator = SimplePaginator(rq, 50, "?page=%%s&%s" % query)
    paginator.set_page(request.GET.get("page", 1))
    if request.GET.get("download"):
        fun = paginator.get_page()  # @UnusedVariable не знаю каким образом, но при помощи этого создается файл
        return HttpResponseRedirect(link)

    return {
        "title": _(u"Calls specification"),
        "form": form,
        "transactions": paginator.get_page(),
        "paginator": paginator,
        "language": "ru",  # TODO: implement some algorithm if needed
        "is_juridical": profile.is_juridical,
        "current_view_name": "account_show_tariffs",
        "statistics" : statistics,
        "use_record" : user_with_record_tarif
    }



@staff_member_required
@render_to("account/change_billing_group.html")
def change_customers_billing_group(request):
    """
Это view-функция для изменения биллинговой группы у нескольких пользователей
    """
    context = {}
    context["request"] = request
    context["user"] = request.user
    context["csrf_token"] = request.COOKIES.get("csrftoken")

    from account.admin import CustomerAccount
    context["app_label"] = CustomerAccount._meta.app_label
    context["app_section"] = CustomerAccount._meta.verbose_name_plural
    context["change_billing_group_title"] = _(u"Change tariff group for selected users").__unicode__()
    context["title"] = context["change_billing_group_title"]

    if request.GET:
        ids_s = request.GET.get("ids")
        if ids_s:
            ids = ids_s.split(",")
            users = []
            for id in ids:
                users += [User.objects.get(id=int(id))]

            context["users"] = users
            if request.POST:
                form = ChangeBillingGroupForm(request.POST)
                context["form"] = form
                if form.is_valid():
                    ch = request.POST.get("Change")
                    if ch:
                        grp_id = form.cleaned_data.get("billing_group")
                        if grp_id:
                            for user in users:
                                ba = user.get_profile().billing_account
                                ba.group_id = int(grp_id)
                                ba.save()
                            return HttpResponseRedirect("/admin/account/customeraccount/")
                    else:
                        return HttpResponseRedirect("/admin/account/customeraccount/")
            else:
                form = ChangeBillingGroupForm()
                context["form"] = form
    else:
        return HttpResponseForbidden()
    return context


@login_required
@render_to("account/account_block.html")
def account_block(request):
    context = {}
    return context


@login_required
@decorator_for_sign_applications()
def change_our_requisites(request):
    try:
        package_obj = Package_on_connection_of_service.objects.get(user=request.user, activate=False, deactivate=False)
    except Package_on_connection_of_service.DoesNotExist:
        raise Http404
    package_obj.activate = True
    package_obj.save()
    return HttpResponseRedirect(reverse('account_profile'))


@render_to('admin/user_statistics.html')
def users_statistic(request):
    if request.user.is_superuser:
        now = datetime.datetime.now()
        date_start_now_month = datetime.datetime(now.year, now.month, 1, 0, 0, 0)
        date_start_next_month = date_start_now_month + relativedelta(months=1)
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        context = dict()
        context["count_all_users"] = count_users()
        context["count_month_user"] = count_users(date_start_now_month, date_start_next_month)
        context["count_week_user"] = count_users(start_week, end_week)
        context["count_today_user"] = count_users(date, now)
        context['count_all_zakazy'] = count_zakazy2()
        context['count_all_active_zakazy'] = count_zakazy2([2],)
        context['count_all_blocked_zakazy'] = count_zakazy2([4],)
        context['count_all_deactivate_zakazy'] = count_zakazy2([3, 5],)
        context['count_all_current_month_zakazy'] = count_zakazy2([], date_start_now_month, date_start_next_month)
        context['count_all_current_active_month_zakazy'] = count_zakazy2([2], date_start_now_month, date_start_next_month)
        context['count_all_blocked_current_month_zakazy'] = count_zakazy2([4], date_start_now_month, date_start_next_month)
        context['count_all_deactivate_current_month_zakazy'] = count_zakazy2([3, 5], date_start_now_month, date_start_next_month)
        context['count_all_current_week_zakazy'] = count_zakazy([], start_week, end_week)
        context['count_all_active_current_week_zakazy'] = count_zakazy2([2], start_week, end_week)
        context['count_all_blocked_current_week_zakazy'] = count_zakazy2([4], start_week, end_week)
        context['count_all_deactivate_current_week_zakazy'] = count_zakazy2([3, 5], start_week, end_week)
        context['count_all_today_zakazy'] = count_zakazy2([], date, now)
        context['count_all_active_today_zakazy'] = count_zakazy2([2], date, now)
        context['count_all_blocked_today_zakazy'] = count_zakazy2([4], date, now)
        context['count_all_deactivate_today_zakazy'] = count_zakazy2([3, 5], date, now)

        context['count_all_zakazy1'] = count_zakazy()
        context['count_all_active_zakazy1'] = count_zakazy([2],)
        context['count_all_blocked_zakazy1'] = count_zakazy([4],)
        context['count_all_deactivate_zakazy1'] = count_zakazy([3, 5],)
        context['count_all_current_month_zakazy1'] = count_zakazy([], date_start_now_month, date_start_next_month)
        context['count_all_active_current_month_zakazy1'] = count_zakazy([2], date_start_now_month, date_start_next_month)
        context['count_all_blocked_current_month_zakazy1'] = count_zakazy([4], date_start_now_month, date_start_next_month)
        context['count_all_deactivate_current_month_zakazy1'] = count_zakazy([3, 5], date_start_now_month, date_start_next_month)
        context['count_all_current_week_zakazy1'] = count_zakazy([], start_week, end_week)
        context['count_all_active_current_week_zakazy1'] = count_zakazy([2], start_week, end_week)
        context['count_all_blocked_current_week_zakazy1'] = count_zakazy([4], start_week, end_week)
        context['count_all_deactivate_current_week_zakazy1'] = count_zakazy([3, 5], start_week, end_week)
        context['count_all_today_zakazy1'] = count_zakazy([], date, now)
        context['count_all_active_today_zakazy1'] = count_zakazy([2], date, now)
        context['count_all_blocked_today_zakazy1'] = count_zakazy([4], date, now)
        context['count_all_deactivate_today_zakazy1'] = count_zakazy([3, 5], date, now)
        context['count_all_paid_zakazy1'] = count_zakazy_paid()
        context['count_all_paid_today_zakazy1'] = count_zakazy_paid([], date, now)
        context['count_all_paid_current_month_zakazy1'] = count_zakazy_paid([], date_start_now_month, date_start_next_month)
        context['count_all_paid_current_week_zakazy1'] = count_zakazy_paid([], start_week, end_week)

        regch = RegistrationCharts()
        #print getattr(regch)

        return context
    else:
        raise Http404


def count_zakazy(status_zakaza=[], start_range='', end_range=''):
        if status_zakaza:
            if start_range and end_range:
                zakazy = Zakazy.objects.filter(date_activation__range=[start_range, end_range], status_zakaza__id__in=status_zakaza, service_type_id=3)
            else:
                zakazy = Zakazy.objects.filter(status_zakaza__id__in=status_zakaza, service_type_id=3)
        else:
            if start_range and end_range:
                zakazy = Zakazy.objects.filter(date_activation__range=[start_range, end_range], service_type_id=3)
            else:
                zakazy = Zakazy.objects.filter(service_type_id=3)

        return zakazy.count()


def count_zakazy2(status_zakaza=[], start_range='', end_range=''):
        if status_zakaza:
            if start_range and end_range:
                zakazy = Zakazy.objects.filter(date_activation__range=[start_range, end_range], status_zakaza__id__in=status_zakaza)
            else:
                zakazy = Zakazy.objects.filter(status_zakaza__id__in=status_zakaza)
        else:
            if start_range and end_range:
                zakazy = Zakazy.objects.filter(date_activation__range=[start_range, end_range])
            else:
                zakazy = Zakazy.objects.all()
        return zakazy.count()


def count_zakazy_paid(status_zakaza=[], start_range='', end_range=''):
        if status_zakaza:
            if start_range and end_range:
                zakazy = Zakazy.objects.filter(date_activation__range=[start_range, end_range], status_zakaza__id__in=status_zakaza, service_type_id=3)
            else:
                zakazy = Zakazy.objects.filter(status_zakaza__id__in=status_zakaza, service_type_id=3)
        else:
            if start_range and end_range:
                zakazy = Zakazy.objects.filter(date_activation__range=[start_range, end_range], service_type_id=3)
            else:
                zakazy = Zakazy.objects.filter(service_type_id=3)
        z_ids = zakazy.values_list('id', flat=True)
        z_bill_accounts = zakazy.values_list('bill_account', flat=True)
        now = datetime.datetime.now()
        payment_objs = Data_centr_payment.objects.filter(((Q(year=now.year) & Q(month=now.month) & Q(bill_account__id__in=z_bill_accounts) & Q(zakaz__id__in=z_ids) & Q(every_month=True))\
                                                      | (Q(bill_account__id__in=z_bill_accounts) & Q(zakaz__id__in=z_ids) & Q(every_month=False) & Q(payment_date=None)) \
                                                      | (Q(year=now.year) & Q(month=now.month) & Q(bill_account__id__in=z_bill_accounts) & Q(zakaz__id__in=z_ids) & Q(every_month=False))) &
                                                        Q(payment_date__isnull=False))
        return payment_objs.count()


def count_users(start_range='', end_range=''):
        if start_range and end_range:
            users = User.objects.filter(is_active=True, date_joined__range=[start_range, end_range])
        else:
            users = User.objects.filter(is_active=True)
        return users.count()



#====================================================================

#@login_required
def account_ajax_change_pas(request):
    new_password = request.POST.get("new_password")
    repeat_new_password = request.POST.get("repeat_new_password")
    new_pas = 0
    new_pas_rep = 0
    
    import re
    reg_ex = re.match(r"((.?)[A-Z]{1,}(.*?)[0-9]{1,}(.*?))|((.*?)[0-9]{1,}(.*?)[A-Z]{1,}(.?))", new_password)
    if reg_ex == None or len(new_password)<6:
            new_pas = 1
    
    if new_password != repeat_new_password:
        new_pas_rep = 1

    if new_pas == 0 and new_pas_rep == 0:
        request.user.set_password(new_password)
        request.user.save()
    
    res_str = ''
    res_str = res_str +  str(new_pas) + ',' + str(new_pas_rep)
    
    return HttpResponse(res_str)






