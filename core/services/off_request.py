from datetime import datetime

from core.models.off_request import OffRequest


def get_or_create_temp_off_request(employee_id: int) -> OffRequest:
    off_request, _ = OffRequest.objects.get_or_create(
        state=OffRequest.State.TEMP,
        employee_id=employee_id,
    )
    return off_request


def set_off_request_date(off_request_id: int, off_date: datetime) -> OffRequest:
    off_request = OffRequest.objects.get(id=off_request_id)
    off_request.off_at = off_date
    off_request.state = OffRequest.State.EMPLOYER_WAITING
    off_request.save()
    return off_request


def accept_off_request(off_request_id: int) -> OffRequest:
    off_request = OffRequest.objects.get(id=off_request_id)
    off_request.state = OffRequest.State.ACCEPTED
    off_request.save()
    return off_request


def reject_off_request(off_request_id: int) -> OffRequest:
    off_request = OffRequest.objects.get(id=off_request_id)
    off_request.state = OffRequest.State.REJECTED
    off_request.save()
    return off_request
