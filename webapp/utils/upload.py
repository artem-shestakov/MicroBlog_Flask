allowed_type = set(['image/png', 'image/jpeg'])


def allowed_image(image):
    """
    Check image content type

    :param image: Upload image
    """
    return image.content_type in allowed_type