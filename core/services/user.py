from core.models import BaleMessengerUser, User


def upsert_bale_user(
    bale_id: int,
    username: str,
    first_name: str,
    last_name: str,
) -> BaleMessengerUser:
    user, _ = BaleMessengerUser.objects.get_or_create(
        bale_id=bale_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    return user


def is_employee(phone_number: str) -> bool:
    return User.objects.filter(phone_number=phone_number, is_employee=True).exists()


def update_bale_user_phone_number(bale_id: int, phone_number: str) -> None:
    BaleMessengerUser.objects.filter(bale_id=bale_id).update(phone_number=phone_number)


def link_bale_user_to_employee(phone_number: str) -> None:
    employee = User.objects.get(phone_number=phone_number)
    BaleMessengerUser.objects.filter(phone_number=phone_number).update(employee_profile=employee)
