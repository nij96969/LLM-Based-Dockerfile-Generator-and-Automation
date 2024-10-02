#!/usr/bin/python3

import docker

def update_image(container_id):
	client = docker.from_env()
	container = client.containers.get(container_id)
	img = container.attrs['Config']['Image'].split(':')
	changes = container.diff()

	if changes:
		new_tag = input("Enter Version Tag :")
		container.commit(repository = img[0], tag = new_tag)
		container.commit(repository = img[0] ,tag='latest')	
		print("Image updated successfully.")
		print(img[0],":",img[1])
		client.images.prune(filters={'dangling': True})
	else :
		print("No changes detected. Skipping image update.")

def get_container_id_by_name(container_name):
    client = docker.from_env()
    containers = client.containers.list()

    for container in containers:
        if container.name == container_name:
            return container.id

    return None

def main():
    container_name = input("Enter the name of the container you want to update: ")
    container_id = get_container_id_by_name(container_name)

    if container_id:
        update_image(container_id)
    else:
        print("Container not found.")

main()
