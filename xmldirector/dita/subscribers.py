# -*- coding: utf-8 -*-

################################################################
# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from xmldirector.dita.html2dita import html2dita_lxml


def topic_modified(topic, event):
    language = topic.Language() or 'en'
    topic_html = topic.body.raw
    topic.xml_set('xml_body', html2dita_lxml(
        html=topic_html, 
        infotype='topic',
        lang=language))

