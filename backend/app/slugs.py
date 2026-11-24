from slugify import slugify


def make_course_slug(title: str) -> str:
    return slugify(title, max_length=60, allow_unicode=False) or "course"
