from django import template

register = template.Library()

@register.filter
def role_badge(role):
    role = (role or "").lower()
    mapping = {
        "admin":    ("bg-danger", "bi-shield-lock-fill"),
        "manager":  ("bg-warning text-dark", "bi-briefcase-fill"),
        "staff":    ("bg-primary", "bi-person-badge-fill"),
        "viewer":   ("bg-secondary", "bi-eye-fill"),
    }
    css, icon = mapping.get(role, ("bg-secondary", "bi-question-circle"))
    # return both css and icon separated with |||
    return f"{css}|||{icon}"


@register.filter
def split(value, delimiter="|||"):
    """
    Split a string by delimiter into a list, so you can use it in templates.
    Example: {{ "a|||b"|split }}
    """
    return value.split(delimiter)
