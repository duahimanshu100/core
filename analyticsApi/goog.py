import requests
import json
import base64


def get_image_vision_google(access_key='AIzaSyCvfPLuqRbsbUTrUBLaHQVt_Lr5GTHa9JU', image_url):
    vision_url = 'https://vision.googleapis.com/v1/images'
    vision_url = vision_url + ':annotate?key=%s' % access_key
    vision_headers = {'Content-Type': 'application/json'}
    content = requests.get(image_url).content
    b64 = base64.b64encode(content)
    string_b64 = b64.decode('utf-8')
    data = (
        {"requests": [{"image": {"content": string_b64}, "features": [
            {"type": "IMAGE_PROPERTIES", "maxResults": 50}, {"type": "LABEL_DETECTION", "maxResults": 50}, {"type": "FACE_DETECTION", "maxResults": 50}]}]}
    )
    data = json.dumps(data)
    vision_results = requests.post(
        url=vision_url, headers=vision_headers, data=data).json()
    return vision_results


def get_image_vision_amazon():
    pass
