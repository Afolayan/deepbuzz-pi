from utils.utils import *
from image_upload import *
import requests


def create_upload_object(filename):
    return ImageUpload(
        #ImageFile=get_actual_image(filename),
        FileName=filename
    )


def upload(upload_object):
    ## url = "{0}{1}".format(server_url, data_upload_url)
    url = get_server_url_upload()
    print("url ==> {0}".format(url))

    headers = {'Content-Type': 'application/json'}
    #request = requests.post(url, data=upload_object, headers=headers)
    path_img = os.getcwd()+"/image.png"
    with open(path_img, "rb") as image_file:
        name_img= os.path.basename(path_img)
        files = {'ImageFile': (name_img,image_file,'multipart/form-data',{'Expires': '0'})}
        datum = {'FileName': 'image.png', 'DateCreated': 1575845321265}
        with requests.Session() as s:
            r = s.post(url,files=files, data=datum)

            print("request ==> {0}".format(r))
            print("content ==> {0}".format(r.content))
            print("json ==> {0}".format(r.json))
            print("headers ==> {0}".format(r.headers))
            print("raw is: {0} ".format(r.raw))
            print("raw is: {0} ".format(r.text))
            
            print(r.status_code)
    return r.status_code


def continuous_capture():
    filename = "image.png"
    print('Captured %s' % filename)
    upload_object = create_upload_object(filename)
    print('Captured %s' % upload_object)
    print('object: %s' % upload_object.toString())
    upload_status = upload(upload_object)
    print("upload status code: {0}".format(upload_status))



def start():
    # capture and upload image here
    continuous_capture()
    print("HTTP request sent")


start()