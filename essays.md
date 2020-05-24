---
layout: default
title: Essays
permalink: /essays
---
<h2 class="no_break_title" style="text-align: center">longform essays on various topics</h2>
<h3 style="text-align: center">sometimes updated and revised</h3>

{% assign sorted = site.essays | sort: 'last_modified' | reverse %}
{% for e in sorted %}

<div class="index_item_title">
<h2 class="no_break_title inline"><a href="{{ e.url }}">{{ e.title }}</a></h2>
<div class="metadata inline">-- Last Updated: {{ e.last_modified | date: '%B %d, %Y' }}</div>
</div>

{% endfor %}
{% comment %}
{{ e.content | truncatewords: 70 | markdownify }}

{% assign wc = e.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ e.url }}">See Full</a>
{% endif %}

{% endfor %}
{% endcomment %}
