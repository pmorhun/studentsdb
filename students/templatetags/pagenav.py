from django import template

register = template.Library()

# Usage: {% pagenav students is_paginated paginator %}
@register.tag
def pagenav(parser, token):
    # parse tag arguments
    try:
        # split_contents knows how to split quoted strings
        tag_name, object_list, is_paginated, paginator = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires 3 arguments" %

    token.contents.split()[0])
    # create PageNavNode object passing tag arguments
    return PageNavNode(object_list, is_paginated, paginator)