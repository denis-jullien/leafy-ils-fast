from database import global_engine
from starlette_admin.contrib.sqlmodel import Admin, ModelView
from starlette_admin.views import Link

from .models import User, BookTable


dbadmin = Admin(
    global_engine,
      base_url="/dbadmin",
      title="Leafy ILS Database Admin"
  )

dbadmin.add_view(ModelView(User, icon="fa fa-users"))
# dbadmin.add_view(ModelView(BookTable, icon="fa fa-book"))
dbadmin.add_view(Link(label="Go Back to Home", icon="fa fa-link", url="/"))

