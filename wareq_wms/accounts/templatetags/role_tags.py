from django import template

register = template.Library()

@register.filter
def role_badge(role):
    colors = {
        "admin": "bg-danger",
        "manager": "bg-warning text-dark",
        "staff": "bg-primary",
        "viewer": "bg-secondary",
    }
    return colors.get(role, "bg-secondary")
