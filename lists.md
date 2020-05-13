---
layout: default
title: Lists
---
<h2 style="text-align: center">curious collections</h2>

{% assign sorted = site.lists | sort: 'last_modified' | reverse %}
{% for l in sorted %}

## <a href="{{ l.url }}">{{ l.title }}</a>

{{ l.content | truncatewords: 70 | markdownify }}

{% assign wc = l.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ l.url }}">See Full</a>
{% endif %}

{% endfor %}
