{% extends "microblog/base.html" %}

{% load i18n microblog_utils %}

{% block title %}{{ usuario_actual }}{{ block.super }}{% endblock title %}

{% block body %}{{ block.super }}

{% if user.is_authenticated %}

{% ifequal user usuario_actual %}
    {% trans "Invalido. No puedes conectarte contigo mismo." %}
{% else %}
    {% if user|tiene_conexion:usuario_actual %}
        {% trans "Tu ya estas conectado con este usuario" %}
    {% else %}
        {{ usuario_actual.username}} <a href="{{ MICROBLOG_URL_BASE }}c/adicionar/{{ usuario_actual.username }}/">{% trans "Conectar como amigo" %}</a>
    {% endif %}
{% endifequal %}

<div class"conexiones">
    {% if conexiones.count %}
    <h2>Conexiones</h2>

    {% include "microblog/lista_conexiones.html" %}
    {% else %}
    <p>{% trans "Conexiones no encontradas" %}</p>
    {% endif %}
</div>

{% endif %}

{% endblock body %}
