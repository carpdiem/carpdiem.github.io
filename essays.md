---
layout: default
title: Essays
---
{% for e in site.essays %}

## <a href="{{ e.url }}">{{ e.title }}</a>

{{ e.content | truncatewords: 70 | markdownify }}

{% assign wc = e.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ e.url }}">See Full</a>
{% endif %}

{% endfor %}
