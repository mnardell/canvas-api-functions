import json
import urllib.request
from urllib.error import URLError
import links_from_header  # pip install links-from-link-header
import time


def get_links (httpResponse='None', start=''):
    """
    Handles the extraction of the pagination links from the HTTP Response Header
    :param httpResponse:
    :param start:
    :return: a tuple with the current and next links
    """
    currentLink = 'current'
    if start:
        return tuple([currentLink, start])

    try:
        links = links_from_header.extract(httpResponse.info()['Link'])
    except AttributeError as e:
        return tuple(['blank','blank'])

    if 'current' in links:
        currentLink = links['current']

    if 'next' in links:
        nextLink = links['next']
    else:
        nextLink = currentLink

    return tuple([currentLink, nextLink])


def wait_on_exception (e):
    """
    Gives a nice pause when an excpetion is thrown
    :param e:
    :return:
    """
    print(e)
    print('#' * 80)
    print("sleepig for 5 seconds")
    time.sleep(5)


def specify_endpoint (url, system, service, items_perpage=100, options=None):
    """
    Closure around a function that gives the endpoint URL, with the one changeaable parameter
    for item. The other required paramters are bound to the closure
    :param url: pattern of the endpoint URL with slots for {server}, {service}, and {item}
    :param system: connection info for Beta, Test and Prod.
    :param service: the service used
    :return: an inner function with the url, system and service paramaters bound to it. This function the takes
    an item_id argument which is slotted into the URL in the proper place
    """

    def get_endpoint_by_id (item_id):
        endpoint_str = url.format(server=system.server, service=service, item=item_id)
        if items_perpage and options:
            endpoint_str += "/?per_page={number}&{options}".format(number=items_perpage,options=options)
        elif items_perpage:
            endpoint_str += "/?per_page={number}".format(number=items_perpage)
        elif options:
            endpoint_str += "/?{options}".format(options=options)

        return endpoint_str

    return get_endpoint_by_id


def build_authorization(system):
    """

    :param system:
    :return:
    """
    return {'Authorization':'Bearer {0}'.format(system.access_token)}


def api_wrapper_function (endpoint=None, authorization=None, direct_url='', filter_fn=(lambda x: True), context_id=0):
    """Clojure around the following paramters
     :param endpoint: The endpoint function created by specify_endpoint, this is partial function with parameters
    for the endpoint URL. This partial function keeps one parameter open for item_id (usually an int)
    :param authorization: Dictionary with the accesss token, in the form {'Authorization':'Bearer <access token>'}
    :param filter_fn: OPTIONAL a filter predicate function (should return T/F) based on aspects of the item.
    If no predicate set the default is a function that always return true.
    :param context_id: OPTIONAL set if you only want to extract from a single item, rather thn interrating over multiple
    contexts
    :return: an innter function with above paramters bound to it. This function takes an id and access endpoint items
    under that item
    """

    def items_from_endpoint (id=context_id, direct_url=''):

        if direct_url:
            start_url = direct_url
        else:
            start_url = endpoint(id)

        links = get_links(start=start_url)
        while links[0] != links[1]:
            try:
                req = urllib.request.Request(links[1], headers=authorization)
                response = urllib.request.urlopen(req)
                f = response.read()
                items = json.loads(f.decode('utf-8'))
                #In the case where a single data item is returned (as a dict) return it and halt iteration
                if isinstance(items, dict):
                    yield items
                    raise StopIteration
                else:
                    for i in items:
                        if filter_fn(i): # The filter function (filter_fn) has
                            # anon function that always returns True by default, so if no filter set, always return item
                            yield i

                    links = get_links(response)
            except (ConnectionResetError, URLError) as e:
                wait_on_exception(e)

    return items_from_endpoint