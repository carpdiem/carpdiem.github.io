---
layout: default
title: Essays
---
<h2 style="text-align: center">longform essays on various topics</h2>
<h2 style="text-align: center">sometimes updated and revised</h2>

{% assign sorted = site.essays | sort: 'last_modified' | reverse %}
{% for e in sorted %}

## <a href="{{ e.url }}">{{ e.title }}</a>

{{ e.content | truncatewords: 70 | markdownify }}

{% assign wc = e.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ e.url }}">See Full</a>
{% endif %}

{% endfor %}
