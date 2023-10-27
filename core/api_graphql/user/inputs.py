import graphene

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class UserBaseInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    username = graphene.String()
    email = graphene.String()
    phone_number = graphene.Int()
    city = graphene.String()
    country = graphene.String()
    adress = graphene.String()
    bio = graphene.String()
    avatar = graphene.String()

    @staticmethod
    def clean_email(value):
        email_validator = EmailValidator(message='Enter valid email')
        try:
            email_validator(value)
            return value
        except ValidationError as e:
            raise ValidationError(f'{e.messages[0]}')


class UserRegisterInput(UserBaseInput):
    """
    This class has 2 methods that are recommended to use:
    - `clean_email(value)` - provides email validation with exception
    raising

    - `clean_password(password_1, password_2)` - take password and
    password confirmation and compare them. Method doesn't raise exceptions
    and just return `True` if passwords the same, `False` otherwise. So make sure
    to raise exception if something going wrong
    """

    first_name = graphene.String(required=True)
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    password_2 = graphene.String(required=True)

    @staticmethod
    def clean_password(password_1, password_2):
        if password_1 == password_2:
            return True
        else:
            return False


class UserUpdateInput(UserBaseInput):
    is_staff = graphene.Boolean()
    is_active = graphene.Boolean()
