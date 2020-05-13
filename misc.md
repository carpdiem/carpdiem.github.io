---
layout: default
title: Misc
---
<h2 style="text-align: center">various things that don't fit elsewhere</h2>

{% assign sorted = site.misc | sort: 'last_modified' | reverse %}
{% for m in sorted %}

## <a href="{{ m.url }}">{{ m.title }}</a>

{{ m.content | truncatewords: 70 | markdownify }}

{% assign wc = m.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ m.url }}">See Full</a>
{% endif %}

{% endfor %}
