# Project level helper function for slug generation
# Why project level and separate folder: because many others app may need same logic



from django.utils.text import slugify

def generate_unique_slug(model, name, field='slug'):

    base_slug = slugify(name)
    slug = base_slug
    counter = 1 
    while model.objects.filter(**{field:slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug