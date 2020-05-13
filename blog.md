---
layout: default
title: Blog
---
<h2 style="text-align: center">shortform blog entries</h2>


{% for b in site.blog %}

## <a href="{{ b.url }}">{{ b.title }}</a>

{{ b.content | truncatewords: 70 | markdownify }}

{% assign wc = b.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ b.url }}">See Full</a>
{% endif %}

{% endfor %}
