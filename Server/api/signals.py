from apscheduler.schedulers.background import BackgroundScheduler
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

from .lib import SSControl
from .models import Account
from .models import Traffic


# signal for remove ss port
@receiver(pre_delete, sender=Account, )
def delete(sender, **kwargs):
    instance = kwargs.get('instance')
    c = SSControl()
    c.remove(instance.port)


# sync ss ports with account records in databases
c = SSControl()
c.sync()

# background job
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


@register_job(scheduler, "interval", seconds=60)
def collect_traffic():
    c = SSControl()
    for port, stat in c.get_status().items():
        account = Account.objects.get(port=port)
        traffic_log = account.traffics.last().traffic_log if account.traffics.last() else 0
        # print('account:', account, )
        stat = int(stat / 1024)

        if stat == traffic_log:
            # no traffic used skipped
            # print('no traffic used skip')
            continue

        elif stat < traffic_log:
            # ss port has been reset
            traffic_log = stat
            traffic_used = stat
            # print('ss port has been rest')
            # print('log traffic_log:', traffic_log, "kb")
            # print('log traffic_used:', traffic_used, "kb")

        else:
            # traffic used
            traffic_used = (stat - traffic_log)
            traffic_log = stat
            # print('log traffic_log:', traffic_log, "kb")
            # print('log traffic_used:', traffic_used, "kb")

        Traffic.objects.create(traffic_used=traffic_used, traffic_log=traffic_log, account=account).save()


register_events(scheduler)
scheduler.start()
