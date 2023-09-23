from django import dispatch

user_logged_in = dispatch.Signal()
user_logged_out = dispatch.Signal()
user_login_failed = dispatch.Signal()
regenerate_token = dispatch.Signal()
