---
layout: default
title: Blog
permalink: /blog
---
<h2 style="text-align: center">shortform blog entries</h2>

{% assign sorted = site.blog | sort: 'date' | reverse %}
{% for b in sorted %}
<div class="index_item_title">
<h2 class="no_break_title"><a href="{{ b.url }}">{{ b.title }}</a></h2>
<div class="metadata">Written: {{ b.date | date: '%B %d, %Y' }}</div>
</div>
<div class="indent_from_left">{{ b.content | markdownify }}</div>
<hr>
{% endfor %}
{% comment %}
{{ b.content | truncatewords: 70 | markdownify }}

{% assign wc = b.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ b.url }}">See Full</a>
{% endif %}

{% endfor %}
{% endcomment %}
