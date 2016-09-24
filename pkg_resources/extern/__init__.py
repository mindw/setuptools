import sys

# Define a small helper function to alias our vendored modules to the real ones
# if the vendored ones do not exist. This idea of this was taken from
# https://github.com/kennethreitz/requests/pull/2567.


def vendored(root_name, modulename, vendor_pkg=None):
    extern_name = '{0}.{1}'.format(root_name, modulename)

    vendor_pkg = vendor_pkg or root_name.replace('extern', '_vendor')
    vendored_name = '{0}.{1}'.format(vendor_pkg, modulename)

    try:
        __import__(vendored_name, globals(), locals(), level=0)
        sys.modules[extern_name] = sys.modules[vendored_name]
        base, head = extern_name.rsplit('.', 1)
        setattr(sys.modules[base], head, sys.modules[vendored_name])

    except ImportError:
        __import__(modulename, globals(), locals(), level=0)
        sys.modules[extern_name] = sys.modules[modulename]
        base, head = extern_name.rsplit('.', 1)
        setattr(sys.modules[base], head, sys.modules[modulename])


# then we want to go ahead and trigger the aliasing of our vendored libraries
# as well as looking for wheels to add to our sys.path. This will cause
# all of this code to be a no-op typically however downstream redistributors
# can enable it in a consistent way across all platforms.
# Actually alias all of our vendored dependencies.
vendored(__name__, 'six')
vendored(__name__, 'six.moves')
vendored(__name__, 'six.moves.urllib')
vendored(__name__, 'pyparsing')
vendored(__name__, 'appdirs')
vendored(__name__, 'packaging')
vendored(__name__, 'packaging.markers')
vendored(__name__, 'packaging.requirements')
vendored(__name__, 'packaging.specifiers')
vendored(__name__, 'packaging.utils')
vendored(__name__, 'packaging.version')
