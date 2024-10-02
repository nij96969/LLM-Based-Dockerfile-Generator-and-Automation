#!/usr/bin/python3
import subprocess , json
def get_docker_images():
    result = subprocess.run(['docker', 'images', '--format', '{{json .}}'], stdout=subprocess.PIPE)
    images = result.stdout.decode('utf-8').strip().split('\n')
    images = [json.loads(image) for image in images if image]
    return images
