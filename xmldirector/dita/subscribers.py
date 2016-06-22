# -*- coding: utf-8 -*-

################################################################
# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from xmldirector.dita.html2dita import html2dita_lxml


def topic_modified(topic, event):
    topic_html = topic.body.output
    topic.xml_set('xml_body', html2dita_lxml(topic_html, infotype='topic'))

