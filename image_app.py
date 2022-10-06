import image_module.images as images

if __name__ == '__main__':
    response = images.jwst_get_all_jpg_images()
    # apod = images.nasa_astronomy_picture_of_the_day()
    print("Done")
