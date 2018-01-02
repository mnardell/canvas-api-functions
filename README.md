# canvas-api-functions

Development of functions for retrieving data from Canvas. The primary tool, the api_wrapper_function (and its inner function items_from_enpoint) provide a Python generator interface for an enpoint. Generators allow the client code to access the endpoint as an iteraterable thing (e.g. we can pull items out of the endpoint from a for loop). 

Files:
api_functions.py - This is where the good stuff is.

~ api_wrapper_function (endpoint=None, authorization=None, direct_url='', filter_fn=(lambda x: True), context_id=0):
    The wrapper purpose is to provide a closure around an inner function, items_from_enpoint, and return it with 
    all the connection,authorization, filtering baked-into the function. 
    
     :param endpoint: The endpoint function created by specify_endpoint, this is partial function with parameters
    for the endpoint URL. This partial function keeps one parameter open for item_id (usually an int)
    :param authorization: Dictionary with the accesss token, in the form {'Authorization':'Bearer <access token>'}
    :param filter_fn: OPTIONAL a filter predicate function (should return T/F) based on aspects of the item.
    If no predicate set the default is a function that always return true.
    :param context_id: OPTIONAL set if you only want to extract from a single item, rather thn interrating over multiple
    contexts
    :return: an innter function with above paramters bound to it. This function takes an id and access endpoint items
    under that item
    
~ items_from_endpoint (id=context_id, direct_url=direct_url):

setup_api_call.py - example of how to specify api_wrapper_functions with endpoints 

report_all_xtools - example of use, in this case using Courses api to get all courses and the iterate over, looking for exteranal tools 


    




