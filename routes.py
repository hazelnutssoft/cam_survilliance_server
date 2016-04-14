__auther__= "guo xiao"

from handler import *

handlers = [
    (r'/', home_handler),
    (r'/browser',browser_handler),
    (r'/setting',setting_handler),
    (r"/setting/(\w+)",setting_handler),
    (r'/api/upload_image', image_handler),
    (r'/api/position', position_handler),
    (r'/api/device', device_handler),
    (r'/api/observer', observer_handler),
    (r'/register', register_handler),
    (r'/login', login_handler),
    (r'/logout', logout_handler)
]

