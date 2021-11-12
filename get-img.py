import os
from posixpath import basename
import time
import re
import urllib.parse
import requests
import hashlib
from bs4 import BeautifulSoup

website_url = 'http://localhost/wordpress/'
# second - use this to not wreck havoc on the website.
time_between_download_requests = 1
output_directory = 'C:/Users/azima/Downloads/Kompas/Mas dennis/get-img-python'

ignore_sizes_regex = r'-\d+x\d+.[a-z]+'


def traverse_url_recursive(url, sleepTime=1):

    # ignore the images that were resized by wordpress during upload
    if(re.search(ignore_sizes_regex, str(url)) != None):
        return

    r = None
    try:
        r = requests.head(url)
    except:
        print('The URL could not be reached')
        return

    if(str(r.headers['Content-Type']).__contains__('html')):

        try:
            r = requests.get(url)
        except:
            print('The URL could not be reached')
            return

        html_parsed = None
        try:
            html_parsed = BeautifulSoup(r.text, 'html.parser')
        except:
            print('Invalid HTML')
            return

        for links in html_parsed.find_all('a'):
            if(links.get_text() != 'Name'
                    and links.get_text() != 'Last modified'
                    and links.get_text() != 'Size'
                    and links.get_text() != 'Description'
                    and links.get_text() != 'Parent Directory'):

                # time.sleep(sleepTime)

                try:
                    traverse_url_recursive(
                        urllib.parse.urljoin(url, links['href']))
                except:
                    print('The link does not contain href.')

    else:

        time.sleep(sleepTime)

        file_path = os.path.join(output_directory, url.split('wp-content/')[1])
        filename, file_extension = os.path.splitext(file_path)
        filename = os.path.basename(filename)

        hash_file = hashlib.sha256(('!Nr' + filename).encode()).hexdigest()
        upper_filename = hash_file.upper()
        

        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except:
                print('The directory could not be created.')

        try:

            try:
                r = requests.get(url)
            except:
                print('The URL could not be reached')
                return

            if file_extension in [".png", ".jpg"]:
                open(upper_filename, 'wb').write(r.content)
                print('File downloaded: ', upper_filename)
            else:
                print('Skip')

        except:

            print('There was an error opening the file.')


traverse_url_recursive(urllib.parse.urljoin(
    website_url, 'wp-content/uploads/'), time_between_download_requests)
