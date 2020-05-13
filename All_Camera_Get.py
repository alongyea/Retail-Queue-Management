from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder

import requests
import shutil
import json
import pprint
import time
import sys


pp = pprint.PrettyPrinter(indent=4)

def webex_message(roomId, message_text, message_url):
    # message_url is the URL for the picture.
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(message_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open('local_image.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp

    m = MultipartEncoder({'roomId': roomId,
                          'text': message_text,
                          'files': ('local_image.jpg', open('local_image.jpg', 'rb'), 'image/jpeg')})
    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                    headers={'Authorization': 'Bearer <xxxx>',
                     'Content-Type': m.content_type})
    print('Send Message to Team Rooms')
    local_file.close()
    return (r)

file = open('queue_MGMT.json', 'r')
CCTV_config = file.read()
cctv_data=json.loads(CCTV_config)
file.close()

payload = {""}


for w in cctv_data['cameras']:
    w.update({'queue_flag': False})
    w.update({'photo_flag': False})
    w.update({'first_timestamp': 0})

while True:
    try:
        for w in cctv_data['cameras']:
            headers = {"X-Cisco-Meraki-API-Key": cctv_data['config']['X-Cisco-Meraki-API-Key']}
            url = "https://api.meraki.com/api/v0/devices/" + w['camera_serial'] + "/camera/analytics/live"
            ss_url = "https://api.meraki.com/api/v0/networks/" + w['network_id'] + "/cameras/" + w['camera_serial'] + "/snapshot"
            response = requests.request("GET", url, headers=headers)
            mv_data=json.loads(response.text)
            people = mv_data["zones"][w['zone']]["person"]
            print(people, w['camera_serial'])
            mv_timestamp = mv_data["ts"]
            timestamp = time.time()
            if people > 0:
                if w['queue_flag'] == False:
                    w['queue_flag'] = True
                    w['first_timestamp'] = timestamp
                else:
                    if (timestamp - w['first_timestamp']) > 5:
                        if w['queue_photo'] == False:
                            print ("Number of People = ", people, "at", mv_timestamp)
                            now = datetime.now()
                            date_time = now.strftime("%A %d %B %Y at %H:%M:%S")
                            message_text = 'There is a big queue at Checkout ' + w['camera_name'] + ' on ' + date_time + ' With over ' + str(people) + ' Customers Waiting'
                            print(message_text)
                            response = requests.post(ss_url, headers=headers)
                            ss_data=json.loads(response.text)
                            print(ss_data['url'])
                            pp.pprint(response)
                            w['queue_photo'] = True
    #                       add delay to make sure photo has been taken
                            time.sleep(1)
                            roomId = w['roomId']
                            message_url = ss_data['url']
                            r = webex_message(roomId, message_text, message_url)
                            pp.pprint(r)
                            print (r)
            else:
                if (timestamp - w['first_timestamp']) > 20:
                    w['queue_flag'] = False
                    w['queue_photo'] = False

        time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
