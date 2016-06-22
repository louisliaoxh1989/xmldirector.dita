################################################################
# xmldirector.dita
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


import io
import six
import os
import plac
import shutil
import tempfile
import pkg_resources
import lxml.etree
import lxml.html
import tidylib

try:
    from shutil import which
except ImportError:
    from shutilwhich import which

from xmldirector.dita import util


for name in ('saxon9', 'saxon8', 'saxon7', 'saxon'):
    saxon = which(name)
    if saxon:
        break

h2d_xsl = pkg_resources.resource_filename('xmldirector.dita.converters.h2d', 'h2d.xsl')
info_types = ('topic', 'concept', 'reference', 'task')


@plac.annotations(
    html_filename=("Input HTML filename", 'option', 'i', str),
    output_filename=("Output DITA filename", 'option', 'o', str),
    converter=('Converter to be used (saxon or lxml', 'option', 'c', str),
    infotype=("DITA type (topic, concept, reference, task)", "option", 'f', str))
def html2dita(html_filename, infotype='topic', output_filename=None, converter='saxon'):

    if converter not in ('saxon', 'lxml'):
        raise ValueError('Unsupported converter (use "lxml" or "saxon")')

    if not infotype in info_types:
        raise ValueError('Unsupported infotype "{}"'.format(infotype))

    if not output_filename:
        output_filename = tempfile.mktemp(suffix='.dita')

    if not html_filename:
        raise ValueError('No HTML input filename given')

    if not os.path.exists(html_filename):
        raise ValueError('No HTML input filename {} does not exist'.format(html_filename))

    with io.open(html_filename, 'r') as fp:
        html = fp.read()

    if converter == 'saxon':
        result = html2dita_saxon(html, infotype)
    elif converter == 'lxml':
        result = html2dita_lxml(html, infotype)

    with io.open(output_filename, 'w') as fp:
        fp.write(result)


def html2dita_lxml(html, infotype='topic'):

    if not isinstance(html, six.text_type):
        raise TypeError('HTML must be str/unicode')

    with io.open(h2d_xsl, 'rb') as fp:
        xslt_root = lxml.etree.XML(fp.read())
        transform = lxml.etree.XSLT(xslt_root)

    html_out, errors = tidylib.tidy_document(
        html.encode('utf8'),
        options={
            'doctype': 'omit',
            'output_xhtml': 1,
            'input-encoding': 'utf8',
            'output-encoding': 'utf8',
            'char-encoding': 'utf8',
        })

    html_out = html_out.replace(b' xmlns="http://www.w3.org/1999/xhtml"', b'')
    html_out = html_out.decode('utf8')

    root = lxml.html.fromstring(html_out)
    transform_result= transform(root)
    if transform.error_log:
        raise RuntimeError('XSLT transformation failed: {}'.format(transform.error_log))
    return lxml.etree.tostring(transform_result, encoding='unicode', pretty_print=True)


def html2dita_saxon(html, infotype='topic'):

    if not isinstance(html, six.text_type):
        raise TypeError('HTML must be str/unicode')

    html_out, errors = tidylib.tidy_document(
    html.encode('utf8'),
    options={
        'doctype': 'omit',
        'output_xhtml': 1,
        'input-encoding': 'utf8',
        'output-encoding': 'utf8',
        'char-encoding': 'utf8',
    })
    html_out = html_out.replace(b' xmlns="http://www.w3.org/1999/xhtml"', b'')

    html_filename = tempfile.mktemp(suffix='.html')
    with io.open(html_filename, 'wb') as fp:
        fp.write(html_out)

    output_filename = tempfile.mktemp(suffix='.html')
    cmd = '"{saxon}" "{html_filename}" "{h2d_xsl}" infotype={infotype} >"{output_filename}"'.format(
            saxon=saxon,
            html_filename=html_filename,
            h2d_xsl=h2d_xsl,
            infotype=infotype,
            output_filename=output_filename)

    status, output = util.runcmd(cmd)
    if status != 0:
        raise RuntimeError('html2dita() failed: {}'.format(output))

    with io.open(output_filename, 'r') as fp:
        topic_out = fp.read()

    os.unlink(html_filename)
    os.unlink(output_filename)
    return topic_out


def main():
    import plac; plac.call(html2dita)


if __name__ == '__main__':
    main()
