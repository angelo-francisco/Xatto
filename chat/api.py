from django.contrib.auth import get_user_model
from django.http import JsonResponse
from ninja import NinjaAPI

from .models import Contact

api = NinjaAPI(
    title="Chat Application API Gateway",
)

User = get_user_model()


def get_user(**kwargs):
    try:
        return User.objects.get(**kwargs)
    except User.DoesNotExist:
        return None


@api.get("/get-contacts/{slug}")
def get_user_contacts(request, slug: str):
    user = get_user(slug=slug)

    if user is None:
        return JsonResponse({"error": "User not found"}, status=404)

    contacts = (
        Contact.objects.filter(owner=user)
        .select_related("contact")
        .values("owner__username", "contact__username", "contact__photo")
    )
    return JsonResponse(list(contacts), safe=False)


@api.get("/get-or-create-contact/{slug}/{contact_username}")
def get_or_create_contacts(request, slug: str, contact_username: str):
    user = get_user(slug=slug)
    contact = get_user(username=contact_username)

    if user is None:
        return JsonResponse({"error": "User not found"}, status=404)

    if contact is None:
        return JsonResponse({"error": "Contact user not found"}, status=404)

    contact_object = Contact.objects.filter(owner=user, contact=contact).values(
        "contact__username", "contact__slug", "contact__photo"
    )

    if contact_object.exists():
        return JsonResponse(list(contact_object), safe=False)

    new_contact = Contact.objects.create(owner=user, contact=contact)
    return JsonResponse(
        {
            "contact__username": new_contact.contact.username,
            "contact__slug": new_contact.contact.slug,
        },
        safe=False,
    )


