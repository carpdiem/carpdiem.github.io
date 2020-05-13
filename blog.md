---
layout: default
title: Blog
---
<h2 style="text-align: center">shortform blog entries</h2>

{% assign sorted = site.blog | sort: 'last_modified' | reverse %}
{% for b in sorted %}

## <a href="{{ b.url }}">{{ b.title }}</a>

{{ b.content | truncatewords: 70 | markdownify }}

{% assign wc = b.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ b.url }}">See Full</a>
{% endif %}

{% endfor %}
