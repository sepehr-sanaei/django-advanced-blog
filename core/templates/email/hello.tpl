{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}
This is an <strong>html</strong> part.
<img src='https://www.google.com/url?sa=i&url=https%3A%2F%2Fbuffer.com%2Flibrary%2Ffree-images%2F&psig=AOvVaw1nrI4ep5MJWZw7_-FQ16Fz&ust=1705169039506000&source=images&cd=vfe&ved=0CBMQjRxqFwoTCOiCtOm32IMDFQAAAAAdAAAAABAE'>
{% endblock %}