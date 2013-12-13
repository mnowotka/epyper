__author__ = 'mnowotka'

try:
    __version__ = __import__('pkg_resources').get_distribution('epyper').version
except Exception as e:
    __version__ = 'development'
