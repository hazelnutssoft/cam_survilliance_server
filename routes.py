__auther__= "guo xiao"

from handler import *

handlers = [
    (r'/', home_handler),
    (r'/browser',browser_handler),
    (r'/setting',setting_handler),
    (r"/setting/(\w+)",setting_handler),
    (r'/api/upload_image', image_handler),
    (r'/api/ctrl', ctrl_handler),
    (r'/login', login_handler),
    (r'/logout', logout_handler)
]

