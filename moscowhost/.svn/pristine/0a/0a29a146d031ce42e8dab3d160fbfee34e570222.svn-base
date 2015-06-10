# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Zakazy.delivery_address'
        db.add_column('data_centr_zakazy', 'delivery_address',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Zakazy.delivery_telephone'
        db.add_column('data_centr_zakazy', 'delivery_telephone',
                      self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Zakazy.delivery'
        db.add_column('data_centr_zakazy', 'delivery',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='delivery_tariff', null=True, db_column='delivery', to=orm['data_centr.Tariff']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Zakazy.delivery_address'
        db.delete_column('data_centr_zakazy', 'delivery_address')

        # Deleting field 'Zakazy.delivery_telephone'
        db.delete_column('data_centr_zakazy', 'delivery_telephone')

        # Deleting field 'Zakazy.delivery'
        db.delete_column('data_centr_zakazy', 'delivery')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_juridical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'site_reg': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'billing.billserviceaccount': {
            'Meta': {'object_name': 'BillserviceAccount', 'db_table': "u'billservice_account'"},
            'address': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'allow_expresscards': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_webcab': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigned_to': ('django.db.models.fields.IntegerField', [], {}),
            'auto_paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'balance_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ballance': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '14', 'decimal_places': '2'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contactperson': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contactperson_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contract': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'credit': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '20', 'decimal_places': '2'}),
            'disabled_by_limit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'elevator_direction': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'entrance': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fullname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'group_id': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'house_bulk': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idle_time': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'idle_time_for_every_month': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'idle_time_for_internet': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'notification_balance': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'passport': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'passport_date': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'passport_given': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'phone_h': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone_m': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prices_group_id': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'vlan': ('django.db.models.fields.IntegerField', [], {})
        },
        'content.variableset': {
            'Meta': {'ordering': "('name',)", 'object_name': 'VariableSet', 'db_table': "'content_varsets'"},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_centr.add_free_internet_zakaz': {
            'Meta': {'object_name': 'Add_free_internet_zakaz', 'managed': 'False'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'data_centr.address_dc': {
            'Meta': {'object_name': 'Address_dc'},
            'date_close': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Rack']"})
        },
        u'data_centr.blocks_of_socket': {
            'Meta': {'object_name': 'Blocks_of_socket'},
            'count_sockets': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Rack']"})
        },
        u'data_centr.cpu': {
            'Meta': {'object_name': 'CPU'},
            'data_bus_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_clock_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'processor_family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'quantity_of_kernels': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'volume_cache_of_memory_1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'volume_cache_of_memory_2': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'volume_cache_of_memory_3': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'data_centr.data_centr_payment': {
            'Meta': {'object_name': 'Data_centr_payment', 'db_table': "'data_centr_payment_for_service'"},
            'bill_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.BillserviceAccount']"}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'every_month': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_on_warning': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'postdate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {}),
            'zakaz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Zakazy']"})
        },
        u'data_centr.hdd': {
            'Meta': {'object_name': 'HDD'},
            'buffer_volume': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'data_transmission_rate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'form_factor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'hdd_capacity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Type_hdd']", 'null': 'True'}),
            'max_level_of_noise': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'max_power_consumption': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'physical_sizes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'rotational_speed_of_a_spindle': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type_hdd': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'data_centr.ip': {
            'Meta': {'object_name': 'IP'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Price']"}),
            'section_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'status_ip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Status_ip']"})
        },
        u'data_centr.limit_connection_service': {
            'Meta': {'unique_together': "(('bill_acc', 'service_type'),)", 'object_name': 'Limit_connection_service'},
            'bill_acc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.BillserviceAccount']"}),
            'count_limit': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Service_type']"})
        },
        u'data_centr.motherboards': {
            'Meta': {'object_name': 'Motherboards'},
            'built_in_audio': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'built_in_video': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'chipset': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'connector_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'external_connectors': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'form_factor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_ram': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'physical_sizes': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slots': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slots_hdd': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data_centr.Slots_hdd']", 'symmetrical': 'False'}),
            'slots_ram': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data_centr.Slots_ram']", 'symmetrical': 'False'}),
            'supply_connector': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'data_centr.os': {
            'Meta': {'object_name': 'OS'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Price']"})
        },
        u'data_centr.ports': {
            'Meta': {'object_name': 'Ports'},
            'adrress': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['data_centr.Address_dc']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number_port': ('django.db.models.fields.IntegerField', [], {}),
            'prefix_interface': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'speed': ('django.db.models.fields.FloatField', [], {'default': '100'}),
            'status_port': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'switch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Switchs']"}),
            'vlan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data_centr.price': {
            'Meta': {'object_name': 'Price'},
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_centr.price_connection': {
            'Meta': {'object_name': 'Price_connection'},
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_centr.priority_of_services': {
            'Meta': {'object_name': 'Priority_of_services', 'db_table': "'priority_of_services'"},
            'bill_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.BillserviceAccount']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'zakaz_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data_centr.rack': {
            'Meta': {'object_name': 'Rack'},
            'count_unit': ('django.db.models.fields.IntegerField', [], {}),
            'depth': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_unit_for_server': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ups': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'data_centr.ram': {
            'Meta': {'object_name': 'RAM'},
            'assignment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'cooling': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'effective_throughput': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_frequency': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'memory_size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'type_ram': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Type_ram']", 'null': 'True', 'blank': 'True'})
        },
        u'data_centr.restore_zakaz': {
            'Meta': {'object_name': 'Restore_zakaz', 'managed': 'False'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'data_centr.server_assembly': {
            'Meta': {'object_name': 'Server_assembly'},
            'cpu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.CPU']"}),
            'hdd': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ram': ('django.db.models.fields.IntegerField', [], {}),
            'ssd': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data_centr.servers': {
            'Meta': {'object_name': 'Servers'},
            'count_port': ('django.db.models.fields.IntegerField', [], {}),
            'count_servers': ('django.db.models.fields.IntegerField', [], {}),
            'count_sockets': ('django.db.models.fields.IntegerField', [], {}),
            'count_unit': ('django.db.models.fields.IntegerField', [], {}),
            'cpu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.CPU']"}),
            'depth': ('django.db.models.fields.FloatField', [], {}),
            'electricity': ('django.db.models.fields.IntegerField', [], {}),
            'hdd': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data_centr.HDD']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motherboard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Motherboards']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ram': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data_centr.RAM']", 'symmetrical': 'False'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Tariff']", 'null': 'True', 'blank': 'True'})
        },
        u'data_centr.service_type': {
            'Meta': {'object_name': 'Service_type'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'data_centr.slots_hdd': {
            'Meta': {'object_name': 'Slots_hdd'},
            'count_slots': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_hdd': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Type_hdd']", 'null': 'True'})
        },
        u'data_centr.slots_ram': {
            'Meta': {'object_name': 'Slots_ram'},
            'count_slots': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_ram': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Type_ram']", 'null': 'True'})
        },
        u'data_centr.sockets': {
            'Meta': {'object_name': 'Sockets'},
            'adrress': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['data_centr.Address_dc']", 'null': 'True', 'blank': 'True'}),
            'block_of_socket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Blocks_of_socket']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number_socket': ('django.db.models.fields.IntegerField', [], {}),
            'status_socket': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'data_centr.software': {
            'Meta': {'object_name': 'Software'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.SoftwareGroup']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Tariff']", 'null': 'True', 'blank': 'True'}),
            'template_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.SoftwareTemplateInfo']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.SoftwareType']", 'null': 'True', 'blank': 'True'}),
            'url_with_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'data_centr.softwaregroup': {
            'Meta': {'object_name': 'SoftwareGroup'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'data_centr.softwaretemplateinfo': {
            'Meta': {'object_name': 'SoftwareTemplateInfo', 'db_table': "'data_centr_software_template_info'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'variablesets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.VariableSet']", 'null': 'True', 'blank': 'True'})
        },
        u'data_centr.softwaretype': {
            'Meta': {'object_name': 'SoftwareType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data_centr.status_ip': {
            'Meta': {'object_name': 'Status_ip'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'data_centr.status_zakaza': {
            'Meta': {'object_name': 'Status_zakaza'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        u'data_centr.switchs': {
            'Meta': {'object_name': 'Switchs'},
            'count_port': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prefix_interface': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Rack']"}),
            'speed': ('django.db.models.fields.FloatField', [], {'default': '100'})
        },
        u'data_centr.tariff': {
            'Meta': {'object_name': 'Tariff'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.Tariff']", 'null': 'True', 'blank': 'True'}),
            'cpu': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electricity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'for_person': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['internet.Internet_persons_for_connection']", 'null': 'True', 'blank': 'True'}),
            'free_minutes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'garant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hdd': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ip': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'port': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'price_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Price']"}),
            'ram': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'section_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'service_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Service_type']"}),
            'socket': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'speed_inet': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tel_zone': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tower_casing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'data_centr.type_hdd': {
            'Meta': {'object_name': 'Type_hdd'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'data_centr.type_ram': {
            'Meta': {'object_name': 'Type_ram'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'data_centr.units': {
            'Meta': {'object_name': 'Units'},
            'address': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['data_centr.Address_dc']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number_unit': ('django.db.models.fields.IntegerField', [], {}),
            'rack': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Rack']"}),
            'status_unit': ('django.db.models.fields.IntegerField', [], {'default': '2'})
        },
        u'data_centr.usercountforsoftware': {
            'Meta': {'object_name': 'UserCountForSoftware'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Servers']"}),
            'user_count_text': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'data_centr.zakazy': {
            'Meta': {'object_name': 'Zakazy'},
            'about': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_dc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Address_dc']", 'null': 'True', 'blank': 'True'}),
            'bill_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['billing.BillserviceAccount']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'connection_cost': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['data_centr.Price_connection']"}),
            'cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'count_ip': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count_of_port': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'count_of_units': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_activation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_deactivation': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_end_test_period': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'delivery_tariff'", 'null': 'True', 'db_column': "'delivery'", 'to': u"orm['data_centr.Tariff']"}),
            'delivery_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'delivery_telephone': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'electricity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['data_centr.IP']", 'symmetrical': 'False', 'blank': 'True'}),
            'main_zakaz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'section_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Servers']", 'null': 'True', 'blank': 'True'}),
            'server_assembly': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Server_assembly']", 'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Service_type']"}),
            'socket': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'software': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['data_centr.Software']", 'null': 'True', 'blank': 'True'}),
            'status_cost': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status_zakaza': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Status_zakaza']"}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.Tariff']", 'null': 'True', 'blank': 'True'}),
            'user_count': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data_centr.UserCountForSoftware']", 'null': 'True', 'blank': 'True'})
        },
        u'internet.accessparameters': {
            'Meta': {'object_name': 'AccessParameters', 'db_table': "'billservice_accessparameters'"},
            'access_time': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.TimePeriod']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'access_type': ('django.db.models.fields.CharField', [], {'default': "'PPTP'", 'max_length': '255', 'blank': 'True'}),
            'burst_rx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'burst_time_rx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'burst_time_tx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'burst_treshold_rx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'burst_treshold_tx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'burst_tx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipn_for_vpn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_rx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'max_tx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'min_rx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'min_tx': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '8', 'blank': 'True'}),
            'sessionscount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'internet.internet_persons_for_connection': {
            'Meta': {'object_name': 'Internet_persons_for_connection', 'db_table': "'internet_persons_for_connection'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'persons': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'internet.ippool': {
            'Meta': {'ordering': "['name']", 'object_name': 'IPPool', 'db_table': "'billservice_ippool'"},
            'end_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'next_ippool': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.IPPool']", 'null': 'True', 'blank': 'True'}),
            'start_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'internet.radiustraffic': {
            'Meta': {'object_name': 'RadiusTraffic', 'db_table': "'billservice_radiustraffic'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.IntegerField', [], {'default': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prepaid_direction': ('django.db.models.fields.IntegerField', [], {'default': '2', 'blank': 'True'}),
            'prepaid_value': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'reset_prepaid_traffic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rounding': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tarification_step': ('django.db.models.fields.IntegerField', [], {'default': '1024', 'blank': 'True'})
        },
        u'internet.settlementperiod': {
            'Meta': {'ordering': "['name']", 'object_name': 'SettlementPeriod', 'db_table': "'billservice_settlementperiod'"},
            'autostart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'length_in': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'internet.tariff': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tariff', 'db_table': "'billservice_tariff'"},
            'access_parameters': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.AccessParameters']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_ballance_transfer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_express_pay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_userblock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'ps_null_ballance_checkout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'radius_traffic_transmit_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.RadiusTraffic']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'require_tarif_cost': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reset_tarif_cost': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'settlement_period': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.SettlementPeriod']", 'null': 'True', 'blank': 'True'}),
            'time_access_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.TimeAccessService']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'traffic_transmit_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internet.TrafficTransmitService']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'userblock_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '30', 'decimal_places': '2', 'blank': 'True'}),
            'userblock_max_days': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'userblock_require_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'vpn_guest_ippool': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tariff_guest_vpn_ippool_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['internet.IPPool']"}),
            'vpn_ippool': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tariff_vpn_ippool_set'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['internet.IPPool']"})
        },
        u'internet.timeaccessservice': {
            'Meta': {'object_name': 'TimeAccessService', 'db_table': "'billservice_timeaccessservice'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prepaid_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'reset_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rounding': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'tarification_step': ('django.db.models.fields.IntegerField', [], {'default': '60', 'blank': 'True'})
        },
        u'internet.timeperiod': {
            'Meta': {'ordering': "['name']", 'object_name': 'TimePeriod', 'db_table': "'billservice_timeperiod'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'internet.traffictransmitservice': {
            'Meta': {'object_name': 'TrafficTransmitService', 'db_table': "'billservice_traffictransmitservice'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reset_traffic': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['data_centr']