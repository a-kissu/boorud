import requests, json
import os
from requests.api import request

class safebooru:
    def __init__(self, limit=100, tags=''):
        self.save_path = tags
        self.limit = f'limit={limit}'
        self.tags = f'tags={tags}'
        self.posts_list = list()

    def get_posts(self):
        try:
            self.posts_list = self.make_request()
        except:
            return False
        else:
            return self.posts_list
    
    def make_request(self):
        api_url = f'https://safebooru.org/index.php?page=dapi&s=post&q=index&{self.limit}&{self.tags}&json=1'
        try:
           response = requests.get(api_url)
        except:
            print('Error occured while making request.')
            return False
        else:
            if response.content == b'':
                return False
            else:
                bytes_value = response.content
                return json.loads(bytes_value.decode('utf8'))

    def save_images(self):
        image_counter = 0
        os.makedirs(self.save_path, exist_ok=True)
        for image in self.posts_list:
            directory = image['directory']
            image_name = image['image']
            image_url = f'https://safebooru.org/images/{directory}/{image_name}'

            # getting image
            try:
                image_data = requests.get(image_url).content
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print('Error while trying to access the image.')
            else:
                # saving/writing the image
                path_to_save = os.getcwd() + '/' + self.save_path + '/' + image_name
                try:
                    with open(path_to_save, 'wb') as handler:
                        handler.write(image_data)
                except:
                    print('Error while trying to save the image!')
                else:
                    image_counter += 1
                    image_size = round(os.path.getsize(path_to_save)/1.049e+6, 2) # getting image size in bytes, converting to MiB then round off
                    print(f'Saved image : {image_name}, Size : {image_size} MiB ({image_counter}/{len(self.posts_list)})')