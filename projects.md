---
layout: default
title: Projects
---
{% for p in site.projects %}

## <a href="{{ p.url }}">{{ p.title }}</a>

{{ p.content | truncatewords: 70 | markdownify }}

{% assign wc = p.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ p.url }}">See Full</a>
{% endif %}

{% endfor %}
