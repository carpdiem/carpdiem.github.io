---
layout: default
title: Projects
---
<h2 style="text-align: center">projects I'd like to share with you</h2>

{% assign sorted = site.projects | sort: 'last_modified' | reverse %}
{% for p in sorted %}

## <a href="{{ p.url }}">{{ p.title }}</a>

{{ p.content | truncatewords: 70 | markdownify }}

{% assign wc = p.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ p.url }}">See Full</a>
{% endif %}

{% endfor %}
