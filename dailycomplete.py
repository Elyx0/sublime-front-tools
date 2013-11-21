# import sublime, sublime_plugin
# import threading


# try:
#     from BufferScroll import BufferScrollAPI
# except:
#     BufferScrollAPI = False


# class Object():
#     pass

# class DailyComplete(sublime_plugin.EventListener):

#     def on_query_completions(self, view, prefix, locations):
#         print "COMPLETING?"
#         print locations
#         print view
#         print prefix
#         return [('dictionary', 'dictionary'), ('dominos', 'dominos'), ('dropbox', 'dropbox'), ('delta', 'delta'), ('direct tv', 'direct tv'), ('dillards', 'dillards'), ('drudge report', 'drudge report'), ('driving directions', 'driving directions'), ('dish network', 'dish network'), ('directions', 'directions')]


# class DailyCompleteThread(threading.Thread):
#     def nothing():
#         print ""
