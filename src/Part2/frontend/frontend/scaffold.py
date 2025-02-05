'Test harness code'

from django_plotly_dash import DjangoDash
from django.utils.module_loading import import_string

def stateless_app_loader(app_name):

    # Load a stateless app
    return import_string("myapp.scaffold." + app_name)

demo_app = DjangoDash(name="BDSE2")