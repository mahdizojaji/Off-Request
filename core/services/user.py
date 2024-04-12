from core.models import BaleMessengerUser


def upsert_bale_user(bale_id: int, username: str, first_name: str, last_name: str) -> bool:
    return BaleMessengerUser.objects.get_or_create(
        bale_id=bale_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
