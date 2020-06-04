---
layout: home
title: recent updates
permalink: /
---

{% for c in site.collections %}

{% if c.label != "posts" %}

## <a href="{{ c.label }}">{{ c.label }}</a>
<div>
{% assign sorted = site[c.label] | sort: 'last_modified' | reverse | slice: 0, 3 %}
{% for item in sorted %}
<div class="index_left_indent">
<div class="index_item_title">
<h3 class="no_break_title"><a href="{{ item.url }}">{{ item.title }}</a></h3>
{% assign written_date = item.date | date: '%s' %}
{% assign updated_date = item.last_modified | date: '%s' %}
{% if written_date < updated_date %}
<div class="metadata">Last Updated: {{ item.last_modified | date: '%B %d, %Y' }}</div>
{% else %}
<div class="metadata">Written: {{ item.date | date: '%B %d, %Y' }}</div>
{% endif %}
</div>
{% if item.image %}
<img src="{{ site.baseurl }}/images/{{ item.image }}" class="excerpt_image">
{% endif %}
{% assign wc = item.content | number_of_words %}
{% if wc > 70 %}
{% assign link = '<a href="' | append: item.url | append: '"> See Full</a>' %}
{{ item.content | truncatewords: 70 | append: link | markdownify }}
{% else %}
{{ item.content | truncatewords: 70 | markdownify }}
{% endif %}
</div>
{% endfor %}
<a href="{{ c.label }}">See More</a>
<hr>
</div>
{% endif %}

{% endfor %}
