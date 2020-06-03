---
layout: default
title: Lists
permalink: /lists
---
<h2 style="text-align: center">curious collections</h2>

{% assign sorted = site.lists | sort: 'last_modified' | reverse %}
{% for l in sorted %}
<div class="index_item_title">
<h2 class="no_break_title inline"><a href="{{ l.url }}">{{ l.title }}</a></h2>
<div class="metadata inline">-- Last Updated: {{ l.last_modified | date: '%B %d, %Y' }}</div>
</div>
{{ l.content | truncatewords: 70 | markdownify }}

{% assign wc = l.content | number_of_words %}

{% if wc > 70 %}
<a href="{{ l.url }}">See Full</a>
{% endif %}
<hr>
{% endfor %}
