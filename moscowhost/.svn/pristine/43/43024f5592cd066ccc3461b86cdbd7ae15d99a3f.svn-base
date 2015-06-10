from django.db import models
from django.conf import settings

class BillingManager(models.Manager):
    def get_query_set(self):
        #return super(BillingManager, self).get_query_set().using(settings.BILLING_DB)
        return super(BillingManager, self).get_query_set()

    def using(self, *args, **kwargs):
        return self.get_query_set()


