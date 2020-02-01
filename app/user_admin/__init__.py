from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla import filters
from app import admin
from app import db
from . import UserAdmin, FarmAdmin, FundedAdmin

from app.models import User, Farm, FundedFarm

admin.add_view(UserAdmin.UserAdmin(User, db.session))
admin.add_view(FarmAdmin.FarmAdmin(Farm, db.session))
admin.add_view(FundedAdmin.FundedAdmin(FundedFarm, db.session))

