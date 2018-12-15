import time

import os
import pyuploadcare as uc


UC_PUBLIC_KEY = os.getenv('UC_PUBLIC_KEY')
UC_PRIVATE_KEY = os.getenv('UC_PRIVATE_KEY')


def init_uc(pub_key, secret):
    uc.conf.pub_key = pub_key
    uc.conf.secret = secret

def upload_image(fp):
    return uc.api_resources.File.upload(fp, store=True)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('Upload an image to UploadCare')
    parser.add_argument('file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    init_uc(UC_PUBLIC_KEY, UC_PRIVATE_KEY)
    print('uploading image')
    file_ = upload_image(args.file)
    # # wait for image to get to CDN
    # delay = 2
    # while not file_.is_ready():
    #     print('image not ready')
    #     time.sleep(delay)
    #     delay *= 2
    #     # file_.info()  # refresh image info
    # print('image available')
    print('image url:', file_.cdn_url)
