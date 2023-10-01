from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('你的姓名？', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('个人说明')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]*$', 0,
               "用户名只能包含汉字、数字、字母、下划线且不能以下划线开头和结尾")])
    confirmed = BooleanField('确定')
    role = SelectField('身份', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('个人说明')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册。')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被占用。')


class PostForm(FlaskForm):
    body = PageDownField("想要说点啥？", validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('输入你的评论', validators=[DataRequired()])
    submit = SubmitField('提交')
