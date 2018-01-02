
def is_xtool(item):
    result = 0
    exclude_list = ['Google Drive','Chat']
    if "type" in item:
        result += "external" in item['type'].lower()
    elif "external_tool_tag_attributes" in item:
        result += item['external_tool_tag_attributes'] is not 'none'

    if "label" in item and item['label'] in exclude_list:
        result = 0
    return result

def is_active_xtool (item):

    #result = is_xtool(item)

    if "hidden" in item:
        if item['hidden']:
            return False
            #result = False
        else:
            return is_xtool(item)

def is_xtool_assignment(item):
    return  'external_tool_tag_attributes' in item and item['external_tool_tag_attributes'] is not 'none'
