from os.path import splitext, exists


def unique_me(path: str) -> str:
    """
    Given a path, creates a unique file name if the file already exists.
    <strong>e.g.</strong> file(1).txt
    :param path: The path that requires a unique name.
    :return: A unique path that does not already exist
    """
    filename, ext = splitext(path)
    count = 0
    while exists(path):
        count += 1
        path = filename + '(' + str(count) + ')' + ext
    return path
