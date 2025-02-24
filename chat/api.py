from django.contrib.auth import get_user_model
from django.http import JsonResponse
from ninja import NinjaAPI

from .models import Contact
from .utils import get_something

api = NinjaAPI(
    title="Chat Application API Gateway",
)

User = get_user_model()


@api.get("/get-contacts/{slug}")
def get_user_contacts(request, slug: str):
    user = get_something(User, slug=slug)

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
    """
    Get the contacts of user, and if user is doesn't ext
    """
    user = get_something(User, slug=slug)
    contact = get_something(User, username=contact_username)

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
            "contact__photo": new_contact.contact.photo,
        },
        safe=False,
    )
