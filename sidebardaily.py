# coding=utf8
import sublime
import sublime_plugin
import os
import re

main_dailymotion_folder = 'dailymotion'
main_dailymotion_controller = {'1': {'prefix': 'Pg', 'controller_path': 'Page'}, '2': {'prefix': 'Sd', 'controller_path': 'Shared'}}

from dailytools import DailyTools

# Support Long path with /
# ?

def parseint(string):
    return int(''.join([x for x in string if x.isdigit()]))

class Example2Command(sublime_plugin.TextCommand):
    def run(self, edit):
        print "Coucou"
        DailyTools().test()


class DailyGoTo:
    def js(self,path):
        print "To continue"


class DailyViewTools():

    def get_main_path(self):
        open_folders = sublime.active_window().folders()
        for i in open_folders:
            if i.rpartition('/')[2] == main_dailymotion_folder:
                return i
                break
        return False

    def check_env(self):
        window = sublime.active_window()
        if not window:
            return False
        view = window.active_view()
        if view is None:
            return False
        return view

    def get_dir(self, path):
        return path.rpartition('/')[2]

    def get_parent_name(self, path):
        return os.path.dirname(path).rpartition('/')[2]

    def get_second_parent_name(self, path):
        return os.path.dirname(os.path.dirname(path)).rpartition('/')[2]

    def get_third_parent_name(self, path):
        return os.path.dirname(os.path.dirname(os.path.dirname(path))).rpartition('/')[2]

    def is_correct_folder(self, path):
        correct_folders = ['views', 'js', 'css']
        if correct_folders.count(self.get_dir(path)):
            return True
        else:
            return False

    def prompt(self, message, default, function, arg1):
        import functools
        sublime.active_window().run_command('hide_panel')
        sublime.active_window().show_input_panel(message.decode('utf-8'), default.decode('utf-8'), functools.partial(function, arg1, True), None, None)


class DailyCreateJsCssCommand(sublime_plugin.WindowCommand):
    def run(self, paths=[], input=False, content=''):
        view = DailyViewTools().check_env()
        if view == False:
            return
        selected_file = paths[0]
        if selected_file.endswith('.html') and DailyViewTools().get_second_parent_name(selected_file) == 'views':
            folder_path = os.path.dirname(selected_file)
            folder_name = DailyViewTools().get_dir(folder_path)
            base_path = os.path.dirname(os.path.dirname(folder_path))
            for i in ['js', 'css']:
                new_path = os.path.join(base_path, i, 'views', folder_name, folder_name + '.' + i)
                print new_path
                if not os.path.exists(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                if not os.path.exists(new_path):
                    DailyTools().createBasicTemplate(new_path)

    def is_enabled(self):
        view = DailyViewTools().check_env()
        if view == False:
            return
        selected_file = view.file_name()
        #Do we get a 'views' folder by looking at ../../ ?
        if selected_file.endswith('.html') and DailyViewTools().get_second_parent_name(selected_file) == 'views':
            return True


class DailyCreateControllerAllCommand(sublime_plugin.WindowCommand):
    def run(self, dirs=[], input=False, content=''):
        selected_file = dirs[0]
        base_path = selected_file
        #Is it the views/js/css folders ?
        base_path = DailyViewTools().get_main_path()
        if input == False:
            DailyViewTools().prompt('Enter controller type [1] Page [2] Shared: ', '', self.run, dirs)
        else:
            if content == '1' or content == '2':
                self.askControllerName([base_path,main_dailymotion_controller[content]])
            else:
                DailyViewTools().prompt('Enter controller type [1] Page [2] Shared: ', '', self.run, dirs)


    def askControllerName(self,path_infos=['',''], input=False,content=''):
        #Path info =------= [0] Project Base [1] prefix&path
        prefix = path_infos[1]['controller_path']
        if input == False:
            DailyViewTools().prompt('Enter controller path/name (e.g. Kids/KidsUserHome --creates--> controllers/' + prefix + '/Kids/KidsUserHomeController.php)', '', self.askControllerName, path_infos)
        else:
            if re.match(r'^[A-Z][a-z]+([A-Z][a-z]+)*(\/[A-Z][a-z]+([A-Z][a-z]+)*)*$',content):
                print "Passing regex path"
                base_path = path_infos[0]
                new_file = os.path.join(base_path,'controllers',prefix,content + 'Controller.php')
                print "Path: " + new_file
                DailyTools().createBasicTemplate(new_file,path_infos)
                # Now creating css/js/html
                # --------=-
                self.createHtmlJsCss(content,path_infos,new_file)
            else:
                print content + ' <==> Failed Regex Pass'
                DailyViewTools().prompt('Enter controller path/name (e.g. Kids/KidsUserHome)', '', self.askControllerName, path_infos)

    def createHtmlJsCss(self,content,path_infos,initial_controller):
        print path_infos
        lower_content = content.lower()
        for i in ['views','js','css']:
            shared_prefix = ''
            if path_infos[1]['controller_path'] != 'Page':
                shared_prefix = path_infos[1]['controller_path'].lower()
            appendix = 'html' if i == 'views' else i
            base_appendix = 'views' if not i == 'views' else ''
            new_file = os.path.join(path_infos[0], i, base_appendix, shared_prefix, lower_content, lower_content.rpartition('/')[2] + '.' + appendix)

            print "Additional ---> " + new_file
            DailyTools().createBasicTemplate(new_file,path_infos,initial_controller)
