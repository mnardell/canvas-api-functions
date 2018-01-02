from setup_api_calls import account_xtools, account_terms

# for x in account_xtools():
#     if 'course_navigation' in x and x['course_navigation']:
#         label = x['course_navigation']['label']
#     elif 'link_selection' in x and x['link_selection']:
#         label = x['link_selection']['label']
#     else:
#         label = '--NA--'
#
#     print(x['id'],x['name'])

def get_xtool_map():
    xtool_map = {}
    for x in account_xtools():
        xtool_map[x['id']] = str("[ACCOUNT INSATALL] " + x['url'])

    return xtool_map

def get_term_map():
    term_map = {}
    for l in account_terms():
        term_list = l['enrollment_terms']
    for t in term_list:
        term_map[t['id']] = t['name']
    return term_map

def read_xtool_context (con_str, mapping):

    context_token = "context_external_tool_"
    if con_str.startswith(context_token):
        id = int(con_str.replace(context_token, ''))
        if id in mapping:
            return mapping[id]

    return con_str




