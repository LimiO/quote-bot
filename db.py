from typing import Optional, Union, List

from peewee import Model

from utils import db
from models import models, User, Template


def connection(function):
    def wrapper(*args):
        with db.connection():
            return function(*args)
    return wrapper
    

@connection
def create_table(*args: Model):
    for model in args:
        if not model.table_exists():
            model.create_table()


@connection
def drop_table(*args: Model):
    for model in reversed(args):
        if model.table_exists():
            model.drop_table()
            

@connection
def get_user(user_id: int) -> User:
    return User.get_or_create(id=user_id)[0]


@connection
def get_users() -> List[User]:
    return list(User.select())


@connection
def get_template(temp_id: int) -> Union[Template, None]:
    return Template.get_or_none(id=temp_id)


@connection
def get_templates() -> List[Template]:
    return list(Template.select())


@connection
def set_template(pic_file_id: str, file_path: str, font_size: int,
                 width: int, left_x: int, left_y: int, right_x: int,
                 right_y: int, name: str, font_path: str, font_color: str,
                 rectangle_color: str, offset: Union[int, None],
                 shadow_color: Union[str, None]) -> Template:
    return Template.create(
        pic_file_id=pic_file_id, file_path=file_path, font_size=font_size, width=width,
        left_x=left_x, left_y=left_y, right_x=right_x, right_y=right_y, name=name,
        font_path=font_path, font_color=font_color, rectangle_color=rectangle_color,
        offset=offset, shadow_color=shadow_color
    )


if __name__ == '__main__':
    drop_table(*models)
    create_table(*models)