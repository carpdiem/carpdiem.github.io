---
layout: home
title: Recent Updates
permalink: /
---

{% for c in site.collections %}

{% if c.label != "posts" %}
	
## <a href="{{ c.label }}">{{ c.label }}</a>

{% assign sorted = site[c.label] | sort: 'last_modified' | reverse | slice: 0, 3 %}
{% for item in sorted %}
	
### <a href="{{ item.url }}">{{ item.title }}</a>

{{ item.content | truncatewords: 70 | markdownify }}
{% assign wc = item.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ item.url }}">See Full</a>
{% endif %}
{% endfor %}
<a href="{{ c.label }}">See More</a>
<hr>

{% endif %}

{% endfor %}
