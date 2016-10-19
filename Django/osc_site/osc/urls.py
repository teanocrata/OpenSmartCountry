from django.conf.urls import url, include

from osc.views import google
from osc.views import inforiego
from osc.views import cadastre

urlpatterns = [
    url(r'^altitud/$', google.altitud, name='altitud'),
    url(r'^inforiego_daily/update$', inforiego.update_inforiego_daily, name='update_inforiego_daily'),
    url(r'^cadastral/parcel$', cadastre.obtain_cadastral_parcels, name='get_cadastral_parcels'),
    url(r'^', include('django.contrib.auth.urls')),
    # url(r'^inforiego_daily/cancel/($P<process_id>[0-9]*)/$', inforiego.cancel_inforiego_daily, name='cancel_inforiego_daily'),
    # url(r'^update/inforiego_hourly/$', views.update_inforiego_hourly, name='update_inforiego_hourly'),
]