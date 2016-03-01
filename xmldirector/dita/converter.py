
import os
import tempfile
import subprocess
import plac

from xmldirector.dita import util

cwd = os.path.abspath(os.path.dirname(__file__))
DITA = os.path.join(cwd, 'converters', 'dita', 'bin', 'dita')
DITAC = os.path.join(cwd, 'converters', 'ditac', 'bin', 'ditac')


def dita2html(ditamap, output=None, converter='dita'):

    if converter not in ('dita', 'ditac'):
        raise ValueError('Unknown DITA converter "{}"'.format(converter))

    if converter == 'dita':
        if not output:
            output = tempfile.mkdtemp()
        cmd = '"{}" -f html5 -i "{}" -o "{}" -Droot-chunk-override=to-content'.format(DITA, ditamap, output)
    else:
        cmd = '"{}" -c single  -f xhtml "{}" "{}"'.format(DITAC, output, ditamap)

    print cmd
    status, output = util.runcmd(cmd)
    print status
    print output

if __name__ == '__main__':
    import plac; plac.call(dita2html)
