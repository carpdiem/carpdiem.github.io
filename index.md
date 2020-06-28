---
layout: home
permalink: /
---

<h2 class="page-heading" style="text-align: center">recent updates</h2>

{% assign sorted = site.documents | sort: 'last_modified' | reverse | slice: 0, 10 %}
{% for item in sorted %}
<div class="index_left_indent">
<div class="index_whole_title">
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
<div class="collection_title">
<h2 class="no_break_title"><a href="{{ site.url }}/{{ item.collection }}">{{ item.collection }}</a></h2>
</div>
</div>
<div>
{% if item.image %}
<img src="{{ site.baseurl }}/images/{{ item.image }}" class="excerpt_image">
{% endif %}

{% if item.content contains '<!--more-->' %}
{{ item.content | split:'<!--more-->' | first | markdownify }}
{% else %}
{{ item.excerpt | markdownify }}
{% endif %}
<a href="{{ item.url }}" class="read_more_link">…read more</a>

{% comment %}
{% assign wc = item.content | number_of_words %}
{% if wc > 70 %}
{% assign link = '<a href="' | append: item.url | append: '"> Read More</a>' %}
{{ item.content | truncatewords: 70 | append: link | markdownify }}
{% else %}
{{ item.content | truncatewords: 70 | markdownify }}
{% endif %}
{% endcomment %}

</div>
</div>
<hr>
{% endfor %}
