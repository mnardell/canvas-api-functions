from api_functions import specify_endpoint, build_authorization, api_wrapper_function
from api_connection import Test
from filter_functions import is_active_xtool

authZ = build_authorization(Test)

course_endpoint_url = 'https://{server}/api/v1/courses/{item}/{service}'
accounts_endpoint_url = 'https://{server}/api/v1/accounts/{item}/{service}'


#---- Bind Enppoint URLs to servers and services -------------------------------------------------------------------

all_courses_endpoint = specify_endpoint(accounts_endpoint_url,
                                        system=Test,
                                        service='courses')

account_tools_endpoint = specify_endpoint(accounts_endpoint_url,
                                  system=Test,
                                  service='external_tools')

account_terms_endpoint = specify_endpoint(accounts_endpoint_url,
                                          system=Test,
                                          service='terms')

course_tools_endpoint = specify_endpoint(course_endpoint_url,
                                         system=Test,
                                         service='external_tools')

course_tabs_endpoint = specify_endpoint(course_endpoint_url,
                                        system=Test,
                                        service='tabs',
                                        options='include="external"')

course_modules_endpoint = specify_endpoint(course_endpoint_url,
                                           system=Test,
                                           service='modules')

course_assignments_endpoint = specify_endpoint(course_endpoint_url,
                                               system=Test,
                                               service='assignments')

course_instructor_enrollments_endpoint = specify_endpoint(course_endpoint_url,
                                                 system=Test,
                                                 service='enrollments',
                                                 options='role=TeacherEnrollment')


#---- Specify API Generators -------------------------------------------------------------------
all_courses = api_wrapper_function(all_courses_endpoint, authorization=authZ, context_id='self')
account_xtools = api_wrapper_function(account_tools_endpoint,authorization=authZ,context_id='self')
account_terms = api_wrapper_function(account_terms_endpoint,authorization=authZ,context_id='self')

course_tabs = api_wrapper_function(course_tabs_endpoint, authZ,
                                   filter_fn=is_active_xtool)
course_xtools = api_wrapper_function(course_tools_endpoint,authZ, )
course_modules = api_wrapper_function(course_modules_endpoint, authZ, )
course_assignments = api_wrapper_function(course_assignments_endpoint, authZ,
                                          filter_fn=is_active_xtool)

# this one is setup to consume direct urls n.b. it does not have an endpoint specified; client code will provide
# direct URL to the item.
module_items = api_wrapper_function(authorization=authZ, filter_fn=is_active_xtool)
course_instructors = api_wrapper_function(course_instructor_enrollments_endpoint, authorization=authZ)

