from flask_admin.contrib import sqla
from flask_login import current_user

class FundedAdmin(sqla.ModelView):

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
        'status',
    ]

    column_filters = [
        'name',
        'status',
        'funder',
        'amount',
        'createdon',
        'payout',
        'units'
    ]

    column_default_sort = ('createdon', True)
    create_modal = True
    edit_modal = True


