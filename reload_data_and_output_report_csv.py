import pickle
from gather_account_xtools import get_xtool_map, read_xtool_context, get_term_map

"""Here is the code we need to recover the report data
"""
with open('xtool_report_dec10_2017.pickle','rb') as f:
    xtool_report = pickle.load(f)

xtool_map = get_xtool_map()
term_map = get_term_map()

with open('xtoolz_use_report.csv','w') as file_out:

    file_out.write("Teacher name(s),Teacher email(s),Course code,Course id,Term,Tool placement,Label,Tool identifier\n")

    for xc in xtool_report:
        #Handle multiple teachers by compiling

        if 'TEACHERS' in xc:
            teacher_names = ''
            teacher_emails = ''
            for t in xc['TEACHERS']:
                try:
                    teacher_names += '{name};'.format(name=t['name'])
                except KeyError:
                    teacher_names += '{name};'.format(name="--;")
                try:
                    teacher_emails += '{email};'.format(email=t['login_id'])
                except KeyError:
                    teacher_emails += '{email};'.format(email="--;")
        else:
            teacher_names = "--NA--"
            teacher_emails = "--NA--"

        course_and_teacher_info = "{teacher_names},{teacher_emails},{course_name},{course_id},{term},".format(
                    teacher_names=teacher_names[:-1], teacher_emails=teacher_emails[:-1],
                    course_name=xc['COURSE_INFO']['course_code'], course_id=xc['COURSE_INFO']['id'],
                    term=term_map[xc['COURSE_INFO']['enrollment_term_id']])

        if 'XTOOL_INSTALLS' in xc:
            for i in xc['XTOOL_INSTALLS']:
                if i['course_navigation']:
                    nav_label = i['course_navigation']['label']
                else:
                    nav_label = '--NA--'
                xtool_install_info ="INSTALLED XTOOL,{label},{url}".format(label=nav_label, url=i['url'])
                if i['url']:
                    url = i['url']
                else:
                    url = "--NA--"
                xtool_map[i['id']] = str("[COURSE INSTALL] " + url)
                print(course_and_teacher_info + xtool_install_info)
                file_out.write(course_and_teacher_info + xtool_install_info + '\n')

        if 'TABS' in xc:
            for t in xc['TABS']:
                tab_info = "NAVIGATION,{label},{context_id}".format(label=t['label'],
                                                                    context_id=read_xtool_context(t['id'], xtool_map))
                print(course_and_teacher_info + tab_info)
                file_out.write(course_and_teacher_info + tab_info + '\n')

        if 'MODULES' in xc:

            for m in xc['MODULES']:
                mod_info = "MODULE,{title},{url}".format(title=m['title'], url=m['external_url']) #previously used html
                                                                                                #url but no realinfo there
                print(course_and_teacher_info + mod_info)
                file_out.write(course_and_teacher_info + mod_info + '\n')

        if 'ASSIGNMENTS' in xc:

            for a in xc['ASSIGNMENTS']:
                assign_info = "ASSIGMENT,{name},{url}".format(url=a['external_tool_tag_attributes']['url'],
                                                              name=a['name'])
                print(course_and_teacher_info + assign_info)
                file_out.write(course_and_teacher_info + assign_info + '\n')


