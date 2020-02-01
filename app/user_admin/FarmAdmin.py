from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from app.models import Farm
from flask_login import current_user

class FarmAdmin(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']

    form_widget_args = {
        'id': {
            'readonly': True
        },
        'person': {
            'readonly': True
        }
    }
    column_searchable_list = [
        'name',
        'stage',
        'location',
        'active',
    ]

    column_default_sort = ('createdon', True)

    column_filters = [
        'name',
        'stage',
        'location',
        'active',
        'duration',
        'units',
        'margin',
        'price',
        'active',
        'farmer'
    ]
