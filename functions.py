import tornado

###getting the username of the logged in user (sub function)###
def get_current_username(resp):
    if resp.get_secure_cookie('tag_it') is not None:
        return resp.get_secure_cookie('tag_it').decode("utf-8")
    else:
        return None

###boolean value of whether the user is logged in or not (sub function) ###
def is_logged_in(resp):
    if resp.get_cookie('tag_it') is None:
        return False
    else:
        return True

###Main function, creates context dictionary with compulsory values only ###
def make_context(response):
    context = {}
    context['is_logged_in']= is_logged_in(response)
    if context['is_logged_in'] == True:
        context['username']= get_current_username(response)
    return context
