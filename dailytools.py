# coding=utf8
import sublime
import sublime_plugin
import re
import os

templates_path = os.path.join(sublime.packages_path(), 'SideBarDaily', 'templates')
main_dailymotion_folder = 'dailymotion'


class DailySwitchToCommand(sublime_plugin.TextCommand):

    def get_main_path(self):
        open_folders = sublime.active_window().folders()
        for i in open_folders:
            print(i)
            if i.rpartition('/')[2] == main_dailymotion_folder:
                return i
                break
        return False

    def run(self, edit, destination_type):
        print("Switching to: " + destination_type)
        window = sublime.active_window()
        if not window:
            return
        view = window.active_view()
        if view is None:
            return
        print("YEAH")
        current_file_path = view.file_name();
        #Switching to same ?
        if current_file_path.rpartition('.')[-1] == destination_type:
            print("Useless to switch to same.")
            return
        results = re.search(r'\/%s\/(views|js|css|controllers)\/(([a-zA-Z0-9]+)\/(([a-zA-Z0-9]+\/)*))' % main_dailymotion_folder, current_file_path)
        if not results:
            print("Wrong Emplacement to switch !")
            return
        print("---GROUP MATCH--")
        print('[0]  ' + results.group(0))
        print('[1]  ' + results.group(1))
        print('[2]  ' + results.group(2))
        print('[3]  ' + results.group(3))
        print('[4]  ' + results.group(4))
        template_switch_type = results.group(1)
        ending_controller_name = current_file_path.split('/')[-1].split('Controller')[0]
        ending_file_name = results.group(2).split('/')[:-1][-1]
        template_switch_type = results.group(1)
        print("From type: " + template_switch_type)
        main_path = self.get_main_path()
        css_url = js_url = controllers_url = html_url = current_file_path

        if template_switch_type == 'views':
            controller_path_prefix = 'Shared' if results.group(3) == 'shared' else 'Page'
            css_class_name =  controller_path_prefix.lower() + "_" + "_".join(results.group(2).split('/')[:-1])
            #path_modified = results.group(2) if controller_path_prefix = 'Shared' else results.group(2).split('/')

            print("Ending file name: " + ending_file_name)
            #CSS
            css_url = os.path.join(main_path,'css', template_switch_type, results.group(2), ending_file_name  + '.css')
            #JS
            js_url = os.path.join(main_path,'js', template_switch_type, results.group(2), ending_file_name  + '.js')
            #CONTROLLER
            if results.group(4):
                controllers_url = os.path.join(main_path,'controllers',controller_path_prefix,results.group(2).capitalize(),results.group(3).capitalize() + 'Controller.php')
                upper_path = os.path.join(main_path,'controllers',controller_path_prefix,results.group(2).capitalize())
            else:
                controllers_url = os.path.join(main_path,'controllers',controller_path_prefix, ending_file_name.capitalize() + 'Controller.php')
                upper_path = os.path.join(main_path,'controllers',controller_path_prefix,ending_file_name.capitalize())
            print("Upper_path: " + upper_path)
            # for dirname, dirnames, filenames in os.walk(upper_path):
            #     print(filenames)
            # print("---END LISTING DIR---")
            print("-")

        # TODO: HANDLE SHARED + CONTROLLER
        if template_switch_type == 'js':
            print("Ending file name: " + ending_file_name)
            #CSS
            css_url = os.path.join(main_path,'css', results.group(2), ending_file_name  + '.css')
            #HTML
            html_url = os.path.join(main_path, results.group(2), ending_file_name  + '.html')

        if template_switch_type == 'css':
            print("Ending file name: " + ending_file_name)
            #CSS
            js_url = os.path.join(main_path,'js', results.group(2), ending_file_name  + '.js')
            #HTML
            html_url = os.path.join(main_path, results.group(2), ending_file_name  + '.html')



            #print("CssClassName: " + css_class_name)
            #print("CssUrlName: " + css_url)
            #print("HTMLUrlName" + html_url)
            #print("JsUrlName: " + js_url)
            #print("ControllerName" + controllers_url)




        if destination_type == 'js':
            if os.path.exists(js_url):
                sublime.active_window().open_file(js_url)
        if destination_type == 'html':
            if os.path.exists(js_url):
                sublime.active_window().open_file(html_url)
        if destination_type == 'controllers':
            if os.path.exists(controllers_url):
                sublime.active_window().open_file(controllers_url)
        if destination_type == 'css':
            if os.path.exists(js_url):
                sublime.active_window().open_file(css_url)


class ExamplesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        #TESTING SUITE
        path_infos_page = [u'/Users/Elyx0/Sites/www/daily/test/dailymotion', {'prefix': 'Pg', 'controller_path': 'Page'}]
        path_infos_shared = [u'/Users/Elyx0/Sites/www/daily/test/dailymotion', {'prefix': 'Sd', 'controller_path': 'Shared'}]
        #print("=============================")
        #print("CONTROLLERS")
        #print("=============================")
        #DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/controllers/Shared/Queeery/NotController.php',path_infos_shared)
        #DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/controllers/Page/Johhhhn/McKainController.php',path_infos_page)
        #DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/controllers/Page/SpeeecialController.php',path_infos_page)
        # print("=============================")
        # print("VIEWS")
        # print("=============================")
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/views/shared/admin/speccos/randomizer/randomizer.html',path_infos_shared)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/views/shared/pika/pika.html',path_infos_shared)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/views/shared/twodirs/onemore/onemore.html',path_infos_shared)
        # print("-=-=-=-=-=-=-=-= PAGE UNDER ==-=-==-=-=-=-=-=")
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/views/admin/sugar/sugar.html',path_infos_page)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/views/whynot/whynot.html',path_infos_page)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/views/three/two/one/one.html',path_infos_page)
        # print("=============================")
        # print("JS")
        # print("=============================")
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/js/views/shared/one/one.js',path_infos_shared)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/js/views/shared/two/one/randomizer.js',path_infos_shared)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/js/views/shared/three/two/one/one.js',path_infos_shared)
        # print("-=-=-=-=-=-=-=-= PAGE UNDER ==-=-==-=-=-=-=-=")
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/js/views/simple/simple.css',path_infos_page)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/js/views/two/one/one.js',path_infos_page)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/js/views/three/two/one/one.js',path_infos_page)
        # print("=============================")
        # print("CSS")
        # print("=============================")
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/css/views/shared/one/one.css',path_infos_shared)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/css/views/shared/two/one/randomizer.css',path_infos_shared)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/css/views/shared/three/two/one/one.css',path_infos_shared)
        # print("-=-=-=-=-=-=-=-= PAGE UNDER ==-=-==-=-=-=-=-=")
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/css/views/simple/simple.css',path_infos_page)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/css/views/two/one/one.css',path_infos_page)
        # DailyTools().createBasicTemplate('/Users/Elyx0/Sites/www/daily/test/dailymotion/css/views/three/two/one/one.css',path_infos_page)
        print("")


class DailyTools:

    def test(self):
        print("Called")

    def createBasicTemplate(self, path, path_infos, controller_initial_path=False,return_values_only_for=False):
        if controller_initial_path is not False:
            print("InitialControllerPath: " + controller_initial_path)
        if os.path.exists(path) and return_values_only_for is False:
            print("[ERROR] Already Exists !!!")
            return
        name = os.path.dirname(path).rpartition('/')[2]
        controller_path = path_infos[1]['controller_path']  #Shared or Page
        controller_path_prefix = path_infos[1]['prefix']  #sd or pg
        template_type = self.getTypeFromPath(path)
        view_file = os.path.join(templates_path, template_type)
        print("--------------Starting Templating-----------")
        print("View File Used: " + view_file)
        print("Using path: " + path)
        # WIll need to parse path to origin to put good classes -> admin/test -> Pg_Admin_test
        results = re.search(r'\/%s\/(views|js|css|controllers)\/(([a-zA-Z0-9]+)\/(([a-zA-Z0-9]+\/)*))' % main_dailymotion_folder, path)
        if not results:
            print("NO RESULT BRO :(")
            return
        print("---GROUP MATCH--")
        print('[0]  ' + results.group(0))
        print('[1]  ' + results.group(1))
        print('[2]  ' + results.group(2))
        print('[3]  ' + results.group(3))
        print('[4]  ' + results.group(4))

        template_switch_type = results.group(1)
        ending_controller_name = path.split('/')[-1].split('Controller')[0]
        print("Template-Type: " + template_switch_type)

        #Creating custom vars for controllers templates
        #controllers are always /controllers/Page or /controllers/Shared
        if template_switch_type == 'controllers':
            if results.group(4):
                #It's a complicated controller Page/About/MyController.php
                controller_name = "_".join(results.group(2).split('/')[:-1]) + '_' + ending_controller_name
                #view is about/MyController/MyController.html
                view_path = os.path.join("/".join(results.group(4).split('/')[:-1]).lower(), ending_controller_name.lower(), ending_controller_name.lower() + '.html')
                if controller_path == 'Shared':
                    view_path = os.path.join(controller_path.lower(), view_path)
            else:
                #It's a Page/TotoController type
                #view is toto/toto.html
                controller_name_backup = path.split('/')[-1].split('Controller')[0]
                controller_name = controller_path + '_' + controller_name_backup
                view_path = os.path.join(controller_name_backup.lower(), controller_name_backup.lower() + '.html')
            print("ControllerName: " + controller_name)
            print("ViewPath:" + view_path)
            #UglyHack :(
            print("RETURN_ONLY == :" + return_values_only_for if return_values_only_for is not False else '-UNSET-')
            if return_values_only_for == 'controllers':
                print("SPECIAL RETURN BABY !!!!!!!!!!!!!!!!")
                return controller_name

        #Creating custom vars for views
        if template_switch_type == 'views':
            if controller_path == 'Shared':
                full_name = "_".join(results.group(2).split('/')[1:])[:-1]
                css_class_name = controller_path_prefix.lower() + "_" + full_name
            else:
                full_name = "_".join(results.group(2).split('/')[:-1])
                css_class_name = controller_path_prefix.lower() + "_" + full_name
            #path_modified = results.group(2) if controller_path_prefix = 'Shared' else results.group(2).split('/')
            ending_file_name = results.group(2).split('/')[:-1][-1]
            print("Ending file name: " + ending_file_name)
            css_url = os.path.join('/css', template_switch_type, results.group(2), ending_file_name + '.css')
            js_url = os.path.join('/js', template_switch_type, results.group(2), ending_file_name + '.js')
            print("CssClassName: " + css_class_name)
            print("FullName: " + full_name)
            print("CssUrlName: " + css_url)
            print("JsUrlName: " + js_url)

        print("ControllerPath: " + controller_path)
        #Creating custom vars for CSS
        if template_switch_type == 'css':
            if controller_path == 'Shared':
                css_class_name = controller_path_prefix.lower() + "_" + "_".join(results.group(4).split('/')[1:])[:-1]

            if controller_path == 'Page':
                css_class_name = controller_path_prefix.lower() + "_" + "_".join(results.group(4).split('/'))[:-1]
            print("CssClassName: " + css_class_name)
        #Creating custom vars for JS
        if template_switch_type == 'js':
            # if controller_path == 'Shared':
            #     js_var_name =  controller_path_prefix.capitalize() + "_" + "_".join(map(lambda i: i.capitalize(), results.group(4).split('/')[1:]))[:-1]
            #     ending_initial_path = controller_initial_path.split('/')[-1].split('Controller')[0]
            #     js_var_name = js_var_name.replace(ending_initial_path.capitalize(),ending_initial_path)
            # if controller_path == 'Page':
            #     js_var_name = controller_path_prefix.capitalize() + "_" + "_".join(map(lambda i: i.capitalize(), results.group(4).split('/')))[:-1]
            #     ending_initial_path = controller_initial_path.split('/')[-1].split('Controller')[0]
            #     print("CurrentJSVAR: " + js_var_name)
            #     print("ending_from_controller: " + ending_initial_path)
            #     js_var_name = js_var_name.replace(ending_initial_path.capitalize(),ending_initial_path)
            if return_values_only_for is False:
                print("Trying...")
                evaluated_only = self.createBasicTemplate(controller_initial_path, path_infos, controller_initial_path,'controllers')
                js_var_name = evaluated_only.replace(controller_path,controller_path_prefix)
                print("JsVarName :" + js_var_name)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        new_file = open(path, 'w')
        for line in open(view_file, 'r'):
            line = line.replace('[[name]]', name)
            line = line.replace('[[name|capitalize]]', name.capitalize())
            line = line.replace('[[name|lowercase]]', name.lower())
            line = line.replace('[[controller_prefix_short]]', path_infos[1]['prefix'])
            #
            if template_switch_type == 'controllers':
                line = line.replace('[[controller_name]]', controller_name)
                line = line.replace('[[view_path]]', view_path)
                line = line.replace('[[extend_from]]', "Page" if controller_path == "Page" else "Base")
            #
            if template_switch_type == 'views':
                #DIFFERENT CASE FOR SHARED VIEWS ?
                line = line.replace('[[css_class_name]]', css_class_name)
                line = line.replace('[[css_url]]', css_url)
                line = line.replace('[[js_url]]', js_url)
                line = line.replace('[[full_name]]', full_name)

            if template_switch_type == 'css':
                line = line.replace('[[css_class_name]]', css_class_name)

            if template_switch_type == 'js':
                line = line.replace('[[js_var_name]]', js_var_name)

            new_file.write(line)
        new_file.close()
        sublime.active_window().open_file(path)
        print("=========")

    def getTypeFromPath(self, path):
        match = re.search(r'\/%s\/(\w+)/' % main_dailymotion_folder, path)
        template_type_name = match.group(1)
        return template_type_name + '.' + path.rpartition('.')[2]
