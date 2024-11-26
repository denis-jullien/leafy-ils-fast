from sqlalchemy.orm import Mapped, mapped_column

from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.views import Link

from app.db import engine, Base, User
from app.admin.views import HomeView

__all__ = ["admin"]

# Define your model
class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str]

# Create admin
admin = Admin(
    engine, 
    title="Leafy ILS Admin", 
    templates_dir="templates/admin",
    index_view=HomeView(label="Home", icon="fa fa-home"),
  )

# Add view
admin.add_view(CustomView(label="Quick add books", icon="fa fa-plus", path="/add", template_path="add.html"))
admin.add_view(ModelView(Post, label="Blog Posts", icon="fa fa-blog"))
admin.add_view(ModelView(User, icon="fa fa-users"))
admin.add_view(Link(label="Go Back to Home", icon="fa fa-link", url="/"))