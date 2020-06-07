---
layout: default
title: Misc
permalink: /misc
---
<h2 style="text-align: center">various things that don't fit elsewhere</h2>

{% assign sorted = site.misc | sort: 'last_modified' | reverse %}
{% for m in sorted %}
<div class="index_item_title">
<h2 class="no_break_title inline"><a href="{{ m.url }}">{{ m.title }}</a></h2>
<div class="metadata inline">-- Last Updated: {{ m.last_modified | date: '%B %d, %Y' }}</div>
</div>
{% if m.image %}
<img src="{{ site.baseurl }}/images/{{ m.image }}" class="excerpt_image">
{% endif %}
{{ m.content | truncatewords: 70 | markdownify }}

{% assign wc = m.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ m.url }}">See Full</a>
{% endif %}
<hr>
{% endfor %}
