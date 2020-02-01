from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla import filters
from app import admin
from app import db
from app.admin_models import FarmAdmin

from app.models import User, Farm, FundedFarm

from flask_admin.contrib import sqla

class UserAdmin(sqla.ModelView):

    can_view_details = True  # show a modal dialog with records details
    action_disallowed_list = ['delete', ]

    form_widget_args = {
        'id': {
            'readonly': True
        }
    }
    column_list = [
        'email',
        'bank_name',
        'bank_account_num',
        'bank_account_name',
        'role',
        'admin',
        'confirmed',
        'createdon'
    ]
    column_searchable_list = [
        'email',
        'role',
        'confirmed',
        'bank_name',
        'admin'
    ]
    column_editable_list = ['confirmed', 'admin', 'role']

    # column details list
    column_auto_select_related = True

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        'createdon',
        'email',
        'bank_name',
        'role',
        'admin',
    ]


admin.add_view(UserAdmin(User, db.session))
admin.add_view(FarmAdmin(Farm, db.session))
admin.add_view(ModelView(FundedFarm, db.session))

