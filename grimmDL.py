

import os
import requests


def download(url: str, dest_folder: str):

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist


    for i in range(1, 101):
        num = f"{i:03}"
        filename = url + str(num) + ".txt"
        save_location = dest_folder + str(num) + ".txt"
        r = requests.get(filename, stream=True)
        if r.ok:
            print("saving to", os.path.abspath(save_location))
            with open(save_location, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))


download("https://www.cs.cmu.edu/~spok/grimmtmp/", dest_folder="stories/")