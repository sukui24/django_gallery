from graphql import GraphQLError
from phonenumbers import parse as parse_phone_number
from users_app.models import User
from api_graphql.user.inputs import UserRegisterInput
from graphql.type.definition import GraphQLResolveInfo


class UserRegisterService:
    """
    Class has only one method - `register_user(input_, info)`. This method
    takes user `input` and graphql request `info` and after some validation
    create and return instance of `User`
    """
    @classmethod
    def register_user(cls, input_, info: GraphQLResolveInfo) -> User:
        """
        Input:
        - `info` - `GraphQLResolveInfo` instance obj. Usually it's automatically
                    collect all needed data and transfer it as `info` object, but it's also mutable
        - `input_` - User input from mutation. Should match the `UserRegisterInput` fields

        Output:
        - created `User` instance

        Permissions: Anyone can register; Authenticated users can not
        """
        context = info.context

        if cls._validate_request(input_, context):
            return cls._create_user(input_, context)

    @staticmethod
    def _validate_request(input_, context) -> bool:

        if context.method != "POST":
            raise GraphQLError(
                f"Only 'POST' method is available, not {context.method}")

        if not UserRegisterInput.clean_password(input_.password, input_.password_2):
            raise GraphQLError("Passwords didn't match, try again")

        return True

    @classmethod
    def _create_user(cls, input_, context) -> User:

        avatar = context.FILES['0'] if context.FILES else None

        phone_number = parse_phone_number(
            input_.phone_number) if input_.phone_number else ""

        email = UserRegisterInput.clean_email(input_.email)

        user_data = {
            "first_name": input_.first_name,
            "last_name": input_.last_name or "",
            "username": input_.username,
            "email": email,
            "bio": input_.bio or "",
            "city": input_.city or "",
            "country": input_.country or "",
            "adress": input_.adress or "",
            "password": input_.password,
            "phone_number": phone_number,
            "avatar": avatar,
        }

        user = User(**user_data)
        user.save()
        return cls._check_user_creation(user)

    @staticmethod
    def _check_user_creation(user: User) -> User:
        latest = User.objects.latest('id')

        if latest.id == user.id:
            return user
        else:
            raise GraphQLError(f"Obj {latest} aren't equal to obj {user}")


class UserDeleteService:

    @classmethod
    def delete_account(cls, info: GraphQLResolveInfo, id: int) -> bool:
        """
        Input:
        - `info` - `GraphQLResolveInfo` instance obj. Usually it's automatically
                    collect all needed data and transfer it as `info` object, but it's also mutable
        - `id` - ID of account that should be deleted

        Output:
        - Boolean, indicates if user is deleted (`True`) or not (`False`)

        Permissions: Only user itself or admins can delete user
        """
        context = info.context

        if cls._validate_request(context):
            user = cls._get_user_or_error(context, id)
            user.delete()
            return True

        return False

    @staticmethod
    def _validate_request(context) -> bool:

        if context.method != "POST":
            raise GraphQLError(
                f"Only 'POST' method is available, not {context.method}")

        return True

    @staticmethod
    def _get_user_or_error(context, id) -> User:
        """
        Return users instance if request made by user itself or by admin

        Otherwise raises GraphQLError
        """
        try:
            user = User.objects.get(pk=id)
            if context.user.id == int(id) or context.user.is_staff:
                return user
            else:
                raise GraphQLError(
                    "Only user itself or admins can delete account")
        except User.DoesNotExist:
            raise GraphQLError("User with this id does not exists")


class UserUpdateService:

    @classmethod
    def update_account(cls, info: GraphQLResolveInfo, input_, id: int) -> User:
        """
        Function to update users account. It works like `PATCH` request, can update
        only one of fields, or every field. (fields `is_staff` and `is_active` is also
        updateable, but only for admins)

        Input:
        - `info` - `GraphQLResolveInfo` instance obj. Usually it's automatically
                    collect all needed data and transfer it as `info` object, but it's also mutable
        - `input_` - Input data that should be changed on
        - `id` - ID of account that should be deleted

        Output:
        - Updated `User` instance

        Permissions: Only user itself or admins can update user
        """

        context = info.context

        cls._validate_request(context)
        user_instance = cls._get_user_or_error(context, id)
        user_updated = cls._apply_user_updates(context, input_, user_instance)
        return user_updated

    @staticmethod
    def _validate_request(context) -> bool:

        if context.method != "POST":
            raise GraphQLError(
                f"Only 'POST' method is available, not {context.method}")

        if len(context.FILES) > 1:
            raise GraphQLError("You should send only one image for avatar!")

        return True

    @staticmethod
    def _get_user_or_error(context, id: str) -> User:
        """
        Return users instance if request made by user itself or by admin

        Otherwise raises GraphQLError
        """
        try:
            user = User.objects.get(pk=id)
            if context.user.id == int(id) or context.user.is_staff:
                return user
            else:
                raise GraphQLError(
                    "Only user itself or admins can update account")
        except User.DoesNotExist:
            raise GraphQLError("User with this id does not exists")

    @staticmethod
    def _apply_user_updates(context, input_, user: User) -> User:

        avatar = context.FILES['0'] if context.FILES else user.avatar

        attributes_to_update = {
            'first_name': input_.first_name,
            'last_name': input_.last_name,
            'username': input_.username,
            'email': input_.email,
            'bio': input_.bio,
            'city': input_.city,
            'country': input_.country,
            'adress': input_.adress,
            'phone_number': input_.phone_number,
            'avatar': avatar,
        }

        for attribute, value in attributes_to_update.items():
            if value is not None:
                setattr(user, attribute, value)

        if user.is_staff:
            user.is_staff = input_.is_staff if input_.is_staff else user.is_staff
            user.is_active = input_.is_active if input_.is_active else user.is_active

        user.save()

        return user
