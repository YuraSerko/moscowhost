# -*- coding=utf-8 -*-
# $Id: models.py 288 2011-01-13 14:01:58Z site $

import datetime
from django.conf import settings
from django.db import models
# from django import template
from django.utils.translation import ugettext_lazy as _
import math
# from telnumbers.consts import *
from managers import BillingManager
# from prices.models import PricesGroup
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from tariffs.models import TelZone


class BillserviceAccountTarif(models.Model):
    account_id = models.IntegerField()
    tarif_id = models.IntegerField()
    datetime = models.DateTimeField()
    periodical_billed = models.BooleanField(default=False)

    objects = BillingManager()

    def save(self, *args, **kwargs):
        #kwargs['using'] = settings.BILLING_DB
        if not self.tarif_id:
            self.tarif_id = settings.DEFAULT_TARIFF_ID
        if not self.datetime:
            self.datetime = datetime.datetime.now()
        return super(BillserviceAccountTarif, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'billservice_accounttarif'


class BillserviceAccount(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200, default='')
    fullname = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')
    address = models.TextField(default='')

    group_id = models.IntegerField(default=1, null=False, blank=False)
    # group = models.ForeignKey(TariffGroup, verbose_name = _(u"Tariff group"))

    prices_group_id = models.IntegerField(default=1, null=False, blank=False)

    # nas_id = models.IntegerField()
    # vpn_ip_address = models.IPAddressField(default='0.0.0.0')
    # assign_ipn_ip_from_dhcp = models.BooleanField(default=False)
    # ipn_ip_address = models.IPAddressField(default='0.0.0.0')
    # ipn_mac_address = models.CharField(max_length=32)
    # ipn_status = models.BooleanField(default=False)
    suspended = models.BooleanField(default=False)
    created = models.DateTimeField()
    ballance = models.DecimalField(default='0', max_digits=14, decimal_places=2)
    credit = models.DecimalField(default='0', max_digits=20, decimal_places=2)
    disabled_by_limit = models.BooleanField()
    balance_blocked = models.BooleanField()
    # ipn_speed = models.CharField(max_length=96)
    # vpn_speed = models.CharField(max_length=96)
    # netmask = models.IPAddressField()
    # ipn_added = models.BooleanField()
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    house_bulk = models.CharField(max_length=255)
    entrance = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    vlan = models.IntegerField()
    allow_webcab = models.BooleanField()
    allow_expresscards = models.BooleanField()
    # assign_dhcp_null = models.BooleanField()
    # assign_dhcp_block = models.BooleanField()
    # allow_vpn_null = models.BooleanField()
    # allow_vpn_block = models.BooleanField()
    passport = models.CharField(max_length=255)
    passport_given = models.CharField(max_length=255)
    phone_h = models.CharField(max_length=255,)
    phone_m = models.CharField(max_length=255)
    # vpn_ipinuse_id = models.IntegerField(null=True)
    # ipn_ipinuse_id = models.IntegerField(null=True)
    # associate_pptp_ipn_ip = models.BooleanField()
    # associate_pppoe_mac = models.BooleanField()
    contactperson_phone = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    row = models.CharField(max_length=255)
    elevator_direction = models.CharField(max_length=255)
    contactperson = models.CharField(max_length=255)
    status = models.IntegerField()
    passport_date = models.CharField(max_length=255)
    contract = models.TextField()
    assigned_to = models.IntegerField()
    idle_time = models.IntegerField(default=4)
    idle_time_for_every_month = models.IntegerField(default=15)
    idle_time_for_internet = models.IntegerField(default=4)
    auto_paid = models.BooleanField(default=True)
    notification_balance = models.IntegerField(default=50)
    #prev_balance = models.DecimalField(default='0', max_digits=14, decimal_places=2, null=True, null=True)
    bonus_ballance = models.DecimalField(default='0', max_digits=14, decimal_places=2, blank = True, null=True)

    class Meta:
        db_table = u'billservice_account'
        managed = True

    objects = BillingManager()

    def save(self, *args, **kwargs):
        #kwargs['using'] = settings.BILLING_DB
        # if not self.nas_id:
        #    self.nas_id = settings.DEFAULT_NAS_ID
        if not self.created:
            self.created = datetime.datetime.now()

        return super(BillserviceAccount, self).save(*args, **kwargs)

    @property
    def prices_group(self):
        try:
            g = PricesGroup.objects.get(id=self.prices_group_id)
        except Exception, e:
            g = None
        return g

    def get_user(self):
        try:
            return User.objects.get(username=self.username)
        except:
            return None

    def adv_company_name(self):
        # from account.admin import CustomerAccount
        # u = CustomerAccount.objects.get(username = self.username)
        # return u.adv_company_name()
        try:
            user = User.objects.get(username=self.username)
            result = user.get_profile().get_display_name()
        except:
            result = self.username
        return result

    @staticmethod
    def get_sum_telematic(bill_acc_id=None):
        now = datetime.datetime.now()
        start_for_telematic = datetime.datetime(now.year if now.month > 1 else now.year - 1, now.month - 1 if now.month > 1 else 12, 1).date()
        end_for_telematic = datetime.datetime(now.year, now.month, 1).date()
        if bill_acc_id:
            sum_temp = BillservicePhoneTransaction.objects.filter(Q(account__id=bill_acc_id) & Q(datetime__gte=start_for_telematic) & Q(datetime__lt=end_for_telematic)).aggregate(total_sum=Sum('summ'))
            if sum_temp['total_sum']:
                sum_telematic = float('%.2f' % float(sum_temp['total_sum']))
            else:
                sum_telematic = None
            return sum_telematic
        else:
            dict_bill_account_in_phone_transaction = BillservicePhoneTransaction.objects.filter(Q(datetime__gte=start_for_telematic) & Q(datetime__lt=end_for_telematic) & \
                                                                  Q(summ__gt=0)).exclude(account=None).order_by('account').distinct().values('account')
            spis_id_account = []
            for i in dict_bill_account_in_phone_transaction:
                spis_id_account.append(i['account'])
            return spis_id_account

    @staticmethod
    def get_sum_record(bill_acc_id=None):
        now = datetime.datetime.now()
        start_for_record = datetime.datetime(now.year if now.month > 1 else now.year - 1, now.month - 1 if now.month > 1 else 12, 1).date()
        end_for_record = datetime.datetime(now.year, now.month, 1).date()
        if bill_acc_id:
            sum_temp = BillserviceRecordTransaction.objects.filter(Q(record_acc__id=bill_acc_id) & Q(datetime__gte=start_for_record) & Q(datetime__lt=end_for_record)).aggregate(total_sum=Sum('summ'))
            if sum_temp['total_sum']:
                sum_record = float('%.2f' % float(sum_temp['total_sum']))
            else:
                sum_record = None
            return sum_record
        else:
            dict_bill_account_in_record_transaction = BillserviceRecordTransaction.objects.filter(Q(datetime__gte=start_for_record) & Q(datetime__lt=end_for_record) & \
                                                                                      Q(summ__gt=0)).exclude(record_acc=None).order_by('record_acc').distinct().values('record_acc')
            spis_id_account = []
            for i in dict_bill_account_in_record_transaction:
                spis_id_account.append(i['record_acc'])
            return spis_id_account

    @staticmethod
    def get_sum_hotspot(bill_acc_id=None, all_summ=False):
        from payment.models import Billservice_transaction
        now = datetime.datetime.now()
        start_for_hotspot = datetime.datetime(now.year if now.month > 1 else now.year - 1, now.month - 1 if now.month > 1 else 12, 1).date()
        end_for_hotspot = datetime.datetime(now.year, now.month, 1).date()
        if bill_acc_id:
            sum_temp = Billservice_transaction.objects.filter(Q(account__id=bill_acc_id) & Q(created__gte=start_for_hotspot) & \
                                                              Q(created__lt=end_for_hotspot) & Q(type_id='HOTSPOT_PAY')).aggregate(total_sum=Sum('summ'))
            if sum_temp['total_sum']:
                sum_record = float('%.2f' % float(sum_temp['total_sum']))
            else:
                sum_record = None
            return -sum_record
        elif all_summ:
            sum_temp = Billservice_transaction.objects.filter(Q(created__gte=start_for_hotspot) & Q(created__lt=end_for_hotspot) & \
                                                              Q(type_id='HOTSPOT_PAY')).aggregate(total_sum=Sum('summ'))
            if sum_temp['total_sum']:
                sum_record = float('%.2f' % float(sum_temp['total_sum']))
            else:
                sum_record = None
            return -sum_record
        else:
            dict_bill_account_in_hotspot_transaction = Billservice_transaction.objects.filter(Q(created__gte=start_for_hotspot) & Q(created__lt=end_for_hotspot) & \
                                                                                      Q(summ__lt=0) & Q(type_id='HOTSPOT_PAY')).order_by('account').distinct().values('account')
            spis_id_account = []
            for i in dict_bill_account_in_hotspot_transaction:
                spis_id_account.append(i['account'])
            return spis_id_account


    def set_tariff(self, tarif, start_date):
        from internet.billing_models import AccountTarif
        new_tarifs = AccountTarif.objects.filter(account=self, datetime__gte=start_date)
        if new_tarifs:
            for tarif in new_tarifs:
                tarif.delete()
        acc_tarif = AccountTarif(account=self, tarif=tarif, datetime=start_date)
        acc_tarif.save()
        return acc_tarif


    def __unicode__(self):
        return self.username


'''
from telnumbers.models import TelNumber, TelNumbersGroup
# from tariffs.models import TariffGroup


@property
def phones(self):
    return TelNumber.objects.filter(account=self)

BillserviceAccount.phones = phones

@property
def external_phone_groups(self):
    """
    Returns list of external phone groups for current account
    In order to get a list of internal numbers in group use
     >> group.telnumbersgroupnumbers_set.all()
    In order to get external phone number use
    >> group.external_number
    """
    groups = list(TelNumbersGroup.objects.filter(account=self))
    
    for g in groups:
        try:
            nums = ExternalNumber.objects.filter(phone_numbers_group = g, account = self)
            for num in nums:
                g.external_number =
        except ExternalNumber.DoesNotExist:
            g.external_number = None
    
    return groups

BillserviceAccount.external_phone_groups = external_phone_groups
'''

'''
@property
def has_external_numbers(self):
    return self.externalnumber_set.all().count() > 0
BillserviceAccount.has_external_numbers = has_external_numbers
'''


def create_billing_account(user):
    """
    user is auth.User object
    """
    billservice_account, created = BillserviceAccount.objects.get_or_create(username=user.username)
    
        
    if created:
        # first time populate fields # !!!!!!!! зачем тут хранить копии их паролей?????? и всего остального???
        billservice_account.password = user.password
        billservice_account.email = user.email
        billservice_account.status = 1
        billservice_account.save()
        billservice_account_tariff = BillserviceAccountTarif(account_id=billservice_account.id)
        billservice_account_tariff.save()

        profile = user.get_profile()
        profile.billing_account_id = billservice_account.id
        profile.save()

        #                                                    # !!!!!!!! ну кто же так делает то??????!!!!!!!!!!!!!!!
        # add phone to phisical user
        # if not user.get_profile().is_juridical:
        #    if 0 == billservice_account.phones.count():
        #        # create one phone for phisical user
        #        log.add("automatic adding phone for non-juridical user %s" % user.username)
        #        nextnum.add_number(billservice_account.id, pwgen.random_pwd())
        # log.add("billing account created for user %s" % user.username)

    return billservice_account


'''

class BillservicePhoneTransactionManager(models.Manager):
    def get_query_set(self):
        return super(BillservicePhoneTransactionManager, self).get_query_set().using('billing')


class BillservicePhoneTransaction(models.Model):

    account = models.ForeignKey(BillserviceAccount)
    called_account = models.ForeignKey(BillserviceAccount, related_name="called_account_id")

    caller_number = models.TextField(verbose_name=u'Вызывающий абонент')
    called_number = models.TextField(verbose_name=u'Вызываемый абонент')
    answer_number = models.TextField()
    session_id = models.TextField(verbose_name=u'Идентификатор сессии')
    tel_zone = models.ForeignKey(TelZone, verbose_name=u'Телефонная зона')
    datetime = models.DateTimeField(verbose_name=u'Дата и время начала звонка')
    session_end = models.DateTimeField(verbose_name=u'Дата и время конца звонка')
    session_length = models.IntegerField(verbose_name=u'Длительность звонка')
    price = models.DecimalField(max_digits=64, decimal_places=32, verbose_name=u'Цена за минуту')
    summ = models.DecimalField(max_digits=64, decimal_places=32, verbose_name=u'Списано средств')
    billable_session_length = models.DecimalField(max_digits=64, decimal_places=32, verbose_name=u'Оплачиваемое время')

    answer_time = models.DateTimeField(verbose_name=u'Дата и время ответа')
    read_codec = models.TextField(verbose_name=u'Кодек')
    disconnect_code = models.TextField(verbose_name=u'Код дисконнекта')
    ip_freeswitch = models.TextField(verbose_name=u'IP FreeSwitch')

    objects = BillservicePhoneTransactionManager()

    @property
    def get_answer_time(self):
        if self.answer_time:
            return self.answer_time.strftime("%d.%m.%Y %H:%M:%S")
        else:
            return "-"


    def get_tel_zone_name(self):
        return unicode(self.tel_zone)

    @property
    def test_field(self):
        return "test value"

    @property
    def get_datetime(self):
        return self.datetime.strftime("%d.%m.%Y %H:%M:%S")

    @property
    def get_session_end(self):
        return self.session_end.strftime("%d.%m.%Y %H:%M:%S")

    @property
    def billable_session_length_in_min(self):
        if self.billable_session_length > 3:
            return int(math.ceil(self.billable_session_length / 60))
        else:
            return 0

    @property
    def caller_account_name(self):
        try:
            name = self.account.username.encode("utf-8")
        except BillserviceAccount.DoesNotExist:
            name = "-"
        return name

    @property
    def called_account_name(self):
        try:
            name = self.called_account.username.encode("utf-8")
        except BillserviceAccount.DoesNotExist:
            name = "-"
        return name

    @property
    def price_with_nds(self):
        return float(self.price)

    @property
    def price_without_nds(self):
        return float(self.price) / 1.18

    @property
    def billable_summ_with_nds(self):
        return self.price_with_nds * self.billable_session_length_in_min

    @property
    def billable_summ_without_nds(self):
        return self.price_without_nds * self.billable_session_length_in_min

    @property
    def billable_nds_summ(self):
        return self.billable_summ_with_nds - self.billable_summ_without_nds



    def __unicode__(self):
        s = str(self.id) + " : " + self.caller_number + " -> " + self.called_number + " " + \
        str(self.datetime) + " ... " + str(self.session_end)
        return s

    class Meta:
        # ordering = ['-datetime']
        verbose_name = _("Billed call")
        verbose_name_plural = _("Billed calls")
        managed = False
        db_table = 'billservice_phonetransaction'


class BillserviceRecordTransaction(models.Model):
    account = models.ForeignKey(BillserviceAccount, related_name="account_id")
    called_account = models.ForeignKey(BillserviceAccount)
    caller_number = models.TextField(verbose_name=u'Вызывающий абонент')
    called_number = models.TextField(verbose_name=u'Вызываемый абонент')
    datetime = models.DateTimeField(verbose_name=u'Дата и время начала звонка')
    session_end = models.DateTimeField(verbose_name=u'Дата и время конца звонка')
    session_length = models.IntegerField(verbose_name=u'Длительность звонка')
    price = models.DecimalField(max_digits=64, decimal_places=32, verbose_name=u'Цена за минуту')
    summ = models.DecimalField(max_digits=64, decimal_places=32, verbose_name=u'Списано средств')
    billable_session_length = models.DecimalField(max_digits=64, decimal_places=32, verbose_name=u'Оплачиваемое время')
    answer_time = models.DateTimeField(verbose_name=u'Дата и время ответа')
    record_acc = models.ForeignKey(BillserviceAccount, related_name="record_acc_id")
    tel_zone = models.ForeignKey(TelZone, verbose_name=u'Телефонная зона')
    objects = BillingManager()

    def save(self, *args, **kwargs):
        kwargs['using'] = settings.BILLING_DB
        return super(BillserviceRecordTransaction, self).save(*args, **kwargs)

    def __unicode__(self):
        s = str(self.id) + " : " + self.caller_number + " -> " + self.called_number + " " + \
        str(self.datetime) + " ... " + str(self.session_end)
        return s

    class Meta:
        # ordering = ['-datetime']
        managed = False
        db_table = 'billservice_recordtransaction'

'''


class BillserviceSubAccount(models.Model):
    account = models.ForeignKey(BillserviceAccount)
    username = models.CharField(max_length=512, blank=True)
    password = models.CharField(max_length=512, blank=True)

    #def save(self, *args, **kwargs):
    #    kwargs['using'] = settings.BILLING_DB

    def __unicode__(self):
        return u"%s" % self.account
    class Meta:
        managed = False
        db_table = 'internal_numbers'

'''

class BillservicePrepaidMinutes(models.Model):
    id = models.AutoField(primary_key=True)
    zone_id = models.IntegerField()
    minutes = models.IntegerField(default=0)
    account_id = models.IntegerField(default=0)
    service_id = models.IntegerField()
    date_of_accrual = models.DateTimeField(null=True, blank=True)
    zakaz_id = models.IntegerField(null=True, blank=True)
    blocked = models.BooleanField(default=False)

    objects = BillingManager()

    def save(self, *args, **kwargs):
        kwargs['using'] = settings.BILLING_DB
        return super(BillservicePrepaidMinutes, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'billservice_prepaid_minutes'


class Disconnect_code(models.Model):
    disconnect_eng = models.CharField(max_length=255, null=True, blank=True)
    disconnect_rus = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.disconnect_eng

    class Meta:
        app_label = 'fsmanage'
        db_table = 'disconnect_code'
        managed = True
        ordering = ("disconnect_eng",)
        verbose_name = _(u"Коды дисконнекта")
        verbose_name_plural = _(u"Коды дисконнекта")
'''

class BalanceHistory(models.Model):
    account = models.ForeignKey(BillserviceAccount, verbose_name=_(u"Аккаунт"))
    balance = models.DecimalField(max_digits=30, decimal_places=20, verbose_name=_(u"Баланс"))
    summ = models.DecimalField(max_digits=30, default=0, decimal_places=6, verbose_name=_(u"Сумма"))
    datetime = models.DateTimeField()

    objects = BillingManager()

    class Meta:
        db_table = 'billservice_balancehistory'
        verbose_name = 'баланс за дату'
        verbose_name_plural = "История по балансу"
