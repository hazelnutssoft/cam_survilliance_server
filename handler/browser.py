from base import base_handler
from model.device_observed import Device_Observed
from model.device import Device
from model.position import Position
from model.image import Image
from util.marcos import IMAGE_NUMBER_FOR_PAGE

class browser_handler(base_handler):
    @tornado.web.authenticated
    def get(self):

        usr = self.get_current_user()

        device_observed = Device_Observed()
        position = Position()
        image = Image()
        devices = device_observed.observed_devices(usr.id)
        if not devices or len(devices) < 1:
            return self.render('no_devices.html', user_name=usr.name)

        positions = []
        for dev in devices:
            positions.extend(position.get_position_by_device_id(dev.id))
        current_position_id = self.get_argument('position_id', '')
        current_page = self.get_argument('page', '')
        if current_page:
            current_page = int(current_page)
        else:
            current_page = 1
        if current_position_id:
            current_position_id = int(current_position_id)
        else:
            # positions = position.get_position_by_device_id(devices[0].id)
            if positions:
                current_position_id = int(positions[0].id)
            else:
                current_position_id = 0
        total_image_num = image.count_by_position_id(current_position_id)
        total_page_num = total_image_num/IMAGE_NUMBER_FOR_PAGE+1
        start_image_num = (current_page - 1)*IMAGE_NUMBER_FOR_PAGE + 1

        if total_page_num < current_page:
            current_page = total_page_num

        images = image.find_by('order by id desc limit ? offset ?',
                               IMAGE_NUMBER_FOR_PAGE,
                               (current_page - 1)*IMAGE_NUMBER_FOR_PAGE)

        # get the start and end page num
        if current_page > 3:
            start_page_num = current_page-3
        else:
            start_page_num = 1

        end_page_num = start_page_num+6
        if end_page_num>total_page_num:
            end_page_num = total_page_num
            start_page_num = end_page_num-6
            if start_page_num<1:
                start_page_num = 1

        end_image_num  = start_image_num+len(images)-1

        return self.render('browser.html',
                           page_name='browser',
                           positions=positions,
                           current_position_id=current_position_id,
                           current_page=current_page,
                           total_page_num=total_page_num,
                           total_image_num=total_image_num,
                           start_image_num=start_image_num,
                           end_image_num=end_image_num,
                           start_page_num=start_page_num,
                           end_page_num=end_page_num,
                           images=images
                           )