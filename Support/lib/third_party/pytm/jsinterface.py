import sys


def call(fn, *args):
    arg_list = [serialize_value(arg) for arg in args]
    html = '<script>%s(%s);</script>' % (fn, ', '.join(arg_list))
    sys.stdout.write(html)
    sys.stdout.flush()


def serialize_value(value):
    if value is None:
        return 'null'
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    elif isinstance(value, int):
        return str(value)
    elif isinstance(float, int):
        return str(value)
    elif isinstance(value, basestring):
        return '"%s"' % value.replace('\n', '\\n').replace('"', '\\"')
    else:
        raise TypeError('The type %s cannot be serialized.' % type(value))
