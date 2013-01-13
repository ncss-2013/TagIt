import tornado

###getting the username of the logged in user ###
def get_current_username(resp):
    return resp.get_secure_cookie('tag_it').decode("utf-8")

###boolean value of whether the user is logged in or not
def is_logged_in(resp):
    if resp.get_cookie('tag_it')!= None:
        return True
    else:
        return False

context["username"] = get_current_username(response)
