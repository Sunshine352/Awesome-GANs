import tensorflow as tf
import numpy as np
import scipy.misc


def down_sampling(img):
    shape = img.get_shape()  # [batch, height, width, channels]

    h2 = int(shape[1] // 2)
    w2 = int(shape[2] // 2)

    return tf.image.resize_images(img, [h2, w2], tf.image.ResizeMethod.BILINEAR)


def up_sampling(img):
    shape = img.get_shape()  # [batch, height, width, channels]

    h2 = int(shape[1] * 2)
    w2 = int(shape[2] * 2)

    return tf.image.resize_images(img, [h2, w2], tf.image.ResizeMethod.BILINEAR)


def inverse_transform(images, inv_type='255'):
    if inv_type == '255':    # [ 0  1]
        images *= 255
    elif inv_type == '127':  # [-1, 1]
        images = (images + 1) * (255 / 2.)

    # clipped by [0, 255]
    images[images > 255] = 255
    images[images < 0] = 0

    return images.astype(np.uint8)


def merge(images, size):
    h, w = images.shape[1], images.shape[2]

    img = np.zeros((h * size[0], w * size[1], 3))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j * h:j * h + h, i * w:i * w + w, :] = image

    return img


def save_image(images, size, path):
    return scipy.misc.imsave(path, merge(images, size))


def save_images(images, size, image_path, inv_type='255'):
    return save_image(inverse_transform(images, inv_type), size, image_path)


def img_save(img, path, inv_type='255'):
    return scipy.misc.imsave(path, img)
    # return cv2.imwrite(path, inverse_transform(img, inv_type))
