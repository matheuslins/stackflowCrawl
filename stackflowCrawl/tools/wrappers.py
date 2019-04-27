import os


def property_collection(func):
    def _wrapper(*args):
        element = func(*args)
        if element is not None:
            element = '_'.join([hunk.lower() for hunk in element.split()])
            os.environ['COLLECTION_NAME'] = 'jobs_crawled_from_{}'.format(
                element)
            return element
        else:
            return ''
    return _wrapper
