from cinescope.models.base_models import TestUser, TestMovie


def mutate_payload(user: TestUser, field, value):
    payload = user.model_dump(mode="json")

    if value is None:
        payload.pop(field)
    else:
        payload[field] = value

    return payload

def mutate_payload_movie(user: TestMovie, field, value):
    payload = user.model_dump(mode="json")

    if value is None:
        payload.pop(field)
    else:
        payload[field] = value

    return payload