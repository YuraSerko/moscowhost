from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'moscowhost.views.home', name='home'),
    # url(r'^moscowhost/', include('moscowhost.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# my urls
# account
#my_var = '1sss'



urlpatterns += patterns('',

    url(r'^add_name_to_url/$', 'page.views.add_name_to_url', name='add_name_to_url'),
    url(r'^$', 'page.views.homepage', name='homepage'),
    url(r'^search/$', 'page.views.search', name='search'),
    url(r'^admin/page/sender/add/', 'page.views.send_msg'),
    url(r'^users/(?P<name_user>[-\w\ \.\@]+)/$', 'page.views.view_user', name='view_user'),
    url(r'^admin/users_statistic/', 'account.views.users_statistic', name='users_statistic'),
    #url(r'^admin/send_sms/sms/add/', 'send_sms.views.send_sms', name='send_sms'),
    #url(r'^admin/send_sms/sms/add_done/','send_sms.views.Send_SMS', name="add_sms"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^djangocontrib/jsi18n', 'django.views.i18n.javascript_catalog', name='djangocontrib_jsi18n'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FILES_ROOT}),
    #url(r'^fax/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FAX_ROOT}),
#    url(r'^helpdesk/', include('helpdesk.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    
)





urlpatterns += patterns('account.views',
    url(r'^login/$', 'login', name='account_login'),
    url(r'^logout/$', 'logout', name='account_logout'),
#    url(r'^(?P<ref_code>[a-z0-9]{6})/registration/$', 'referral_registration', name='account_referral_registration'),
    url(r'^registration/$', 'registration', name='account_registration'),
    url(r'^registred/$', 'registration_completed', name='account_registration_completed'),
    url(r'^resetpassword/$', 'password_reset_request', name='account_password_reset_request'),
    url(r'^activation/(?P<action_key>[-_\d\w]+)/$', 'activation', name='account_activation'),
    url(r'^resend_activation_code/$', 'resend_activation_code', name='resend_activation_code'),
    url(r'^account/block/$', 'account_block', name='account_block'),

#    url("^account/service_choice/$", "service_choice", name="service_choice"),
    url("^account/demands_dc/$", "my_data_centr", name="my_data_centr"),
    url("^account/demands_dc/zayavka/(?P<hidden_id>\d+)/$", "del_zayavka", name="del_zayavka"),
    url("^account/demands_dc/zakaz/(?P<hidden_id>\d+)/$", "previously_del_zakaz", name="previously_del_zakaz"),
    url("^account/demands_dc/activation_zakaz/", "activation_zakaz", name="activation_zakaz"),
    url("^account/demands_dc/demands_dc_archive/", "demands_dc_archive", name="demands_dc_archive"),
    url('^account/$', 'account', name='account_profile'),
    url('^account/profile/$', 'account_profile_edit', name='account_profile_edit'),
    url("^account/data_centr/$", "account_data_centr", name="account_data_centr"),
    #url("^account/rack/$", "account_rack", name="account_rack"),
    #url("^account/colocation/$", "account_colocation", name="account_colocation"),
    #url("^account/dedicated/$", "account_dedicated", name="account_dedicated"),
    #url("^account/vds/$", "account_vds", name="account_vds"),
    #url("^account/hosting/$", "account_hosting", name="account_hosting"),
    #url("^account/communication_links/$", "account_communication_links", name="account_communication_links"),

    url('^account/changepassword/$', 'account_change_password', name='account_change_password'),
#    url('^account/balance/$', 'account_balance', name='account_balance'),
#    url('^account/fax/$', 'account_fax', name='account_fax'),
#    url('^account/fax/dajax/$', 'fax_dajax', name='fax_dajax'),
    url("^content/complaint/$", "complaint_phone", name="complaint_phone"),
    url("^content/wish-complaint/$", "complaint_int", name="complaint_int"),
    url("^change_our_requisites/$", "change_our_requisites", name="change_our_requisites"),
    url("^account/user_reg_check_ajax/$", "user_reg_check_ajax", name="user_reg_check_ajax"),
    url('^account_ajax_change_pas/$', 'account_ajax_change_pas', name = 'account_ajax_change_pas'),
    
    # url("^add_equipment_rent/$", "add_equipment_rent", name="add_equipment_rent"),
    
    
    
    #virtual 1c starting
    url("^account/virtual_servers_1C/$", "account_virtual_servers", name="account_virtual_servers"),
    
    
)

urlpatterns = urlpatterns + patterns('helpdesk.views.account',
    url(r'^account/helpdesk/$', 'list_tickets', name='helpdesk_account_tickets'),  # list user's tickets
#    url(r'^account/helpdesk/add/$', 'create_ticket', name='helpdesk_account_tickets_add'),  # create new ticket
#    url(r'^account/helpdesk/(?P<ticket_id>[\d]+)/$', 'view_ticket', name='helpdesk_account_tickets_view'),  # change/post comment,
)

urlpatterns += patterns('internet.views',
    url("^account/internet/vpn/$", "vpn_users", name="vpn_users"),
    url("^account/internet/vpn/add/$", "vpn_users_add", name="vpn_users_add"),
    url("^account/internet/vpn/edit/(?P<vpn_id>\d+)/$", "vpn_users_edit", name="vpn_users_edit"),
    url("^account/internet/vpn/delete/(?P<vpn_id>\d+)/$", "vpn_users_del", name="vpn_users_del"),
    url("^account/internet/vpn/deleting/(?P<vpn_id>\d+)/$", "vpn_users_deleting", name="vpn_users_deleting"),
)

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)




urlpatterns += patterns('data_centr.views',
    #url("^content/main_rack/send_zakaz/$", "main_rack_zakaz", name="main_rack_zakaz"),
    #url("^content/vds/$", "vds", name="vds"),
    url("^account/priority_of_services/$", "priority_of_services", name="priority_of_services"),
    url("^step_change_method_auth/$", "step_change_method_auth", name="step_change_method_auth"),
    #url("^dedicated/step_zakaz/(?P<account>[-\w]+)/(?P<server_id>\d+)/$", "ajax_dedicated_step_zakaz", name="ajax_dedicated_step_zakaz"),
    #url("^dedicated/step_conf/(?P<account>[-\w]+)/$", "ajax_dedicated_step_conf", name="ajax_dedicated_step_conf"),
    #url("^dedicated/step_registration/$", "ajax_dedicated_step_registration", name="ajax_dedicated_step_registration"),  
    #url("^dedicated/cost_calculation/(?P<server_id>\d+)/$", "ajax_dedicated_cost_calculation", name="ajax_dedicated_cost_calculation"),
    #url("^account/add_dedicated_final/$", "add_dedicated_final", name="add_dedicated_final"),
    url("^account/demands_dc/view_zayavka/(?P<zayavka_id>\d+)/$", "view_dc_zayavka", name="view_dc_zayavka"),
    url("^account/demands_dc/view_zakaz/(?P<zayavka_id>\d+)/$", "view_dc_zayavka", name="view_dc_zayavka"),
    url("^account/demands_dc/configuration/(?P<zakaz_id>\d+)/$", "ajax_dc_configuration", name="ajax_dc_configuration"),
    url("^account/demands_dc/apply_configuration/(?P<zakaz_id>\d+)/$", "apply_dc_configuration", name="apply_dc_configuration"),
)




urlpatterns += patterns('data_centr.views',
   # url("^service/colocation-server/$", "colocation", name="colocation"),
    #url("^service/dedicated-server/$", "dedicated", name="dedicated"),
    #url("^service/server-rack/$", "rack", name="rack"),
    #1c started
    url("^service/virtual_server_1C/$", "virtual_server_1C", name = "virtual_server_1C"),
    url("^virtual_server/get_info/$", "get_single_server_ajax", name = "get_single_server_ajax"),
    url("^virtual_server/recount_cost/$", 'virtual_server_recount_cost', name = 'virtual_server_recount_cost'), 
    url("^virtual_server/step_zakaz/(?P<account>[-\w]+)/(?P<server_id>\d+)/$", "ajax_virtual_server_step_zakaz", name="ajax_virtual_server_step_zakaz"),
    url("^virtual_server/change_type_inet/(?P<type_inet>[-\w]+)/$", "ajax_virtual_server_change_type_inet", name="ajax_virtual_server_change_type_inet"),
    url("^virtual_server/step_auth/(?P<account>[-\w]+)/$", "ajax_virtual_server_step_auth", name="ajax_virtual_server_step_auth"),
    
    url("^virtual_server/step_login/$", "ajax_virtual_server_step_login", name="ajax_virtual_server_step_login"),
    ##########wtf
    url("^account/add_virtual_server_final/$", "add_virtual_server_final", name="add_virtual_server_final"),
    url("^virtual_server/ajax_software_get_template_info/(?P<software_id>\d+)/$", "ajax_software_get_template_info", name = "ajax_software_get_template_info"),
    #activation from admin...
    url("^account/virtual_server_zakazy_admin_activate/$", "virtual_server_zakazy_admin_activate", name = "virtual_server_zakazy_admin_activate"),
    
    #registration
    url("^virtual_server/step_registration/$", "ajax_virtual_server_step_registration", name="ajax_virtual_server_step_registration"),
    
    #change activated zakaz
    #url("^ajax_change_activated_zakaz_soft_type/$", "ajax_change_activated_zakaz_soft_type", name = "ajax_change_activated_zakaz_soft_type"),
    #url("^ajax_change_activated_zakaz_soft/$", "ajax_change_activated_zakaz_soft", name = "ajax_change_activated_zakaz_soft"),
    url("^ajax_zakaz_change_apply_changes/(?P<zakaz_id>\d+)/$", "ajax_zakaz_change_apply_changes", name = "ajax_zakaz_change_apply_changes"),
)


# findocs
urlpatterns += patterns("findocs.views",
    #url("^account/findocs/signed/$", "findocs_list_signed", name="signed_financial_documents_list"),
    url("^account/findocs/signed/(?P<signed_id>\d+)/$", "findocs_show_signed", name="show_signed_financial_document"),
    url("^account/findocs/applications/sign/(?P<app_id>\d+)/$", "findocs_application_sign", name="signing_application_to_financial_document"),
    #url('^account/findocs/contract_cancellation/$', 'contract_cancellation', name='contract_cancellation'),
    url('^account/findocs/resigning_of_contracts/$', 'resigning_of_contracts', name='resigning_of_contracts'),
)



urlpatterns += patterns('content.views',
#    url("^hostel/$", "hostelinform", name="hostelinform"),
#    url("^content/(?P<number_id>\d+)/$", "check_view", name="check_view"),
#    url("^content_send_to_email/(?P<number_id>\d+)/$", "send_to_emai", name="send_to_emai"),
#    url("^content_receipt/$", "check_receipt", name="check_receipt"),
#    url("^content/type_service/$", "type_service", name="type_service"),
#    url("^content/data_centr/$", "data_centr", name="data_centr"),
#    url("^content/sim_card/$", "sim_card", name="sim_card"),
#    url("^content/webphone/$", "webphone", name="webphone"),
#    url("^content/phone_service/$", "phone_service", name="phone_service"),
#    url("^content/payment/$", "payment", name="payment"),
     #how to use vps
     url("^content/help/$", "help", name = "help"),
     
)



# content_varset
urlpatterns += patterns("",
    url(r"^content_variables/(?P<varset_id>\d+)/$", "content_variables.views.show_vars"),
    url(r"^content_variables/show_many/$", "content_variables.views.show_many_vars"),
)






# payment methods
urlpatterns += patterns("payment.views",
    url(r"^payment/card/$", "payment_card", name="card_payment"),
    url(r"^account/payment/$", "payment_list", name="payment_list"),
    url(r"^account/payment/comepay/process/$", "payment_comepay_process", name="comepay_payment_process"),
    # url(r"^account/payment/cyberplat/process/$", "payment_cyberplat_process", name="cyberplat_payment_process"),
    
    
    #url("^payment/step_auth/(?P<account>[-\w]+)/$", "ajax_virtual_server_step_auth", name="ajax_virtual_server_step_auth"),
    #url("^payment/step_auth/(?P<account>[-\w]+)/$", "ajax_payment_step_auth", name="ajax_payment_step_auth"),
    #url("^payment/step_pay/step_login/$", "ajax_payment_step_login", name="ajax_payment_step_login"),
    #url("^payment/step_pay/(?P<account>[-\w]+)/(?P<sum>\d+)/$", "ajax_payment_step_pay", name="ajax_payment_step_pay"),
)



urlpatterns += patterns("payment.qiwi.views",
    url(r"^payment/card/qiwi/$", "payment_qiwi_card", name="qiwi_payment_card"),
    url(r"^account/payment/qiwi/$", "payment_qiwi", name="qiwi_payment"),
    url(r"^payment/card/qiwi/(?P<paytype>all|mobile)/$", "payment_qiwi_card", name="qiwi_payment_card"),
    url(r"^account/payment/qiwi/(?P<paytype>all|mobile)/$", "payment_qiwi", name="qiwi_payment"),
)



urlpatterns += patterns("payment.netpay.views",
    # url(r"^payment/card/qiwi/$", "payment_qiwi_card", name="qiwi_payment_card"),
    url(r"^payment/netpay/process/$", "payment_netpay_process", name="payment_netpay_process"),
    url(r"^account/payment/netpay/$", "payment_netpay", name="netpay_payment"),
)


urlpatterns += patterns("payment.webmoney.views",
    url(r"^payment/card/webmoney/$", "payment_wm_card_start", name="wm_payment_card_start"),
    url(r"^account/payment/webmoney/$", "payment_wm", name="wm_payment"),
    url(r"^account/payment/webmoney/success/$", "payment_wm_success", name="wm_payment_success"),
    url(r"^account/payment/webmoney/error/$", "payment_wm_error", name="wm_payment_error"),
    url(r"^account/payment/webmoney/process/$", "payment_wm_process", name="wm_payment_process"),
)

'''
urlpatterns += patterns("payment.robokassa.views",
    url(r"^account/payment/robokassa/$", "robokassa_pay", name="robokassa_pay"),
    url(r"^account/payment/robokassa/card/(?P<type_pay>bank|mobile)/$", "payment_rk_card_start", name="payment_rk_card_start"),
    url(r"^account/payment/robokassa/card/$", "payment_rk_card_start", name="payment_rk_card_start"),
    url(r"^account/payment/robokassa/result/$", "robokassa_result", name="robokassa_result"),
    url(r"^account/payment/robokassa/success/$", "robokassa_success", name="robokassa_success"),
    url(r"^account/payment/robokassa/fail/$", "robokassa_fail", name="robokassa_fail"),
)
'''


#webmoney merchant !!! oplata
urlpatterns += patterns("payment.webmoney_merchant.views",
    url(r"^account/payment/webmoney_merchant/$", "payment_wm_merchant", name="payment_wm_merchant"),
    url(r"^payment/webmoney_merchant/$", "payment_wm_merchant_public", name = "payment_wm_merchant_public"),
    #url(r"^payment/webmoney_merchant_auth/$", "payment_wm_merchant_public_auth", name = "payment_wm_merchant_public_auth"),
    
    #views for loggining
    url("^payment/step_auth/(?P<account>[-\w]+)/$", "ajax_payment_step_auth", name="ajax_payment_step_auth"),
    url("^payment/step_pay/step_login/$", "ajax_payment_step_login", name="ajax_payment_step_login"),
    url("^payment/step_pay/step_registration/$", "ajax_payment_step_registration", name="ajax_payment_step_registration"),
    # url(r"^account/payment/webmoney_merchant/process/$", "payment_wm_merchant_process", name="wm_wm_merchant_process"),
    # url(r"^account/payment/webmoney_merchant/error/$", "payment_wm_merchant_error", name="wm_payment_merchant_error"),
    # url(r"^account/payment/webmoney_merchant/success/$", "payment_wm_merchant_success", name="wm_payment_merchant_success"),                     
)




urlpatterns += patterns('devices.views',

#     url("^account/invoices_and_payment/$", "invoices_and_payment", name="invoices_and_payment"),
# 
#     url("^account/invoices_and_payment/(?P<type_document>[-\w]+)/(?P<number_id>\d+)/$", "check_user_view", name="check_user_view"),

    url("^account/advance_invoice/$", "advance_invoice", name="advance_invoice"),
    url("^account/write_offs_and_account_replenishment/$", "write_offs_and_account_replenishment", name="write_offs_and_account_replenishment"),

)







urlpatterns += patterns('content.views',
#    url(r'^content/article/$', 'article_list', name='article_list'),
    #url(r'^content/article/(?P<id>\d+)/$', 'article', name='article'),
    url(r'^content/article/(?P<slug>[-\w]+)/$', 'article_by_slug', name='article_by_slug'),
#    url(r'^content/article/raw/(?P<slug>[-\w]+)/$', "raw_article_by_slug"),
    url(r'^content/news/$', 'news_list', name='news_list'),
    url(r'^content/news/(?P<id>\d+)/$', 'news', name='news'),
    url("^content/data_centr/$", "data_centr", name="data_centr"),
    url("^content/payment/$", "payment", name="payment"),
    url("^content/type_service/$", "type_service", name="type_service"),
    
    
    
    url(r'^(?P<prefix>[-\w]+)/(?P<slug>[-\w]+)/$', 'moscow_article_by_slug', name='moscow_article_by_slug'), #moscowdata only
    url("^type_service/$", "type_service", name="type_service"), #moscowdata only
    url("^service/$", "data_centr", name="data_centr"), #moscowdata only
    url("^payment/$", "payment", name="payment"), #moscowdata only
    url(r'^news/$', 'news_list', name='news_list'), #moscowdata only
)







































