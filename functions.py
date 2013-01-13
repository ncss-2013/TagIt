import tornado

#####getting the username of the logged in user (sub function)###
##def get_current_username():
##    if response.get_secure_cookie('tag_it') is not None:
##        return response.get_secure_cookie('tag_it').decode("utf-8")
##    else:
##        return None
##
#####boolean value of whether the user is logged in or not (sub function) ###
##def is_logged_in():
##    if response.get_cookie('tag_it') is None:
##        return False
##    else:
##        return True

###Main function, creates context dictionary with compulsory values only ###
def make_context(response):
    context = {}
    #making user context
    if response.get_cookie('tag_it'):
        context['is_logged_in'] = True
        try:
            context['username'] = response.get_secure_cookie('tag_it').decode("utf-8")
        except:
            response.clear_cookie('tag_it')
            response.redirect('/')
    else:
        context['is_logged_in'] = False
    return context
