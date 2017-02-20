import requests
import json
import base64
import boto3


def get_vision_google(image_url, access_key='AIzaSyCvfPLuqRbsbUTrUBLaHQVt_Lr5GTHa9JU'):
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


def get_vision_amazon(image_url):
    client = boto3.client('rekognition')
    content = requests.get(image_url).content
    response = {}
    response['detect_faces'] = client.detect_faces(
        Attributes=['ALL'],
        Image={
            'Bytes': content
        }
    )
    response['detect_labels'] = client.detect_labels(
        MaxLabels=100,
        Image={
            'Bytes': content
        }
    )
    return response


def get_vision_results(image_url):
    if not image_url:
        return None, None
    google_vision_results = get_vision_google(image_url)
    amazon_vision_results = get_vision_amazon(image_url)

    return google_vision_results, amazon_vision_results
    # google_vision_results['responses'][0]['imagePropertiesAnnotation']
    # google_vision_results['responses'][0]['labelAnnotations']
    # google_vision_results['responses'][0]['faceAnnotations']
