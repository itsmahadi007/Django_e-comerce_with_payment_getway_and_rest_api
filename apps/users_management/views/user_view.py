# from allauth.account.utils import complete_signup
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users_management.models import UserManage
from apps.users_management.serializers.basic_users_serializer import UserSerializerShort
from backend.utils.email_queue_manager import email_queue_overhauler
from backend.utils.text_choices import EmailPriorityStatus

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2"),
)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def user_update(request, user_id):
    try:
        user_profile = UserManage.objects.get(id=user_id)
    except UserManage.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    excluded_fields = ["password", "pk", "id"]

    for field in user_profile._meta.get_fields():
        field_name = field.name
        if field_name not in excluded_fields:
            if field_name in request.data:
                value = request.data[field_name]
                if value == "true":
                    value = True
                elif value == "false":
                    value = False
                setattr(user_profile, field_name, value)

    for field in ["profile_image"]:
        if field in request.FILES:
            current_image = getattr(user_profile, field)
            if current_image:
                current_image.delete()
            setattr(user_profile, field, request.FILES[field])

    user_profile.save()

    email_queue_overhauler(
        subject="User Profile Change",
        body="Hello! You just have changed your profile.",
        to_email=user_profile.email,
        priority=EmailPriorityStatus.NORMAL,
        context=None,
    )

    serializer_obj = UserSerializerShort(user_profile, context={"request": request})

    return Response(
        serializer_obj.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_information(request):
    user = request.user
    serializer_obj = UserSerializerShort(user, context={"request": request})

    return Response(
        serializer_obj.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def check_unique_username(request):
    username = request.GET.get("username")
    if username:
        try:
            UserManage.objects.get(username=username)
            return Response(
                {"username": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UserManage.DoesNotExist:
            return Response(
                {"username": "Username is available."}, status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"username": "Username is required."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def check_unique_email(request):
    email = request.GET.get("email")
    if email:
        try:
            UserManage.objects.get(email=email)
            return Response(
                {"email": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST
            )
        except UserManage.DoesNotExist:
            return Response({"email": "Email is available."}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"email": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
        )

class TestMail(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        print(request.data["email"])
        # sent_mail(
        #     "Testing subject",
        #     "Testing body 007",
        #     [request.data["email"]],
        # )
        priority_set = request.data["priority"]
        if priority_set == "LOW":
            priority = EmailPriorityStatus.LOW
        elif priority_set == "NORMAL":
            priority = EmailPriorityStatus.NORMAL
        elif priority_set == "HIGH":
            priority = EmailPriorityStatus.HIGH
        else:
            priority = EmailPriorityStatus.HIGH
        email_queue_overhauler(
            subject="Testing subject",
            body="Testing body 007",
            to_email=request.data["email"],
            priority=priority,
            context=None,
        )
        return Response({"message": "mail sent"})


