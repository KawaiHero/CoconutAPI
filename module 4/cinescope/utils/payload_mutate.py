from cinescope.models.base_models import TestUser


def mutate_payload(user: TestUser, field, value):
    payload = user.model_dump(mode="json")

    if value is None:
        payload.pop(field)
    else:
        payload[field] = value

    return payload