from folder_scanner import FolderScanner


def get_missing_system_includes(includes):
    """
    Get a list of missing system includes from a list of includes.

    :param includes: A list of includes
    :return: A list of missing system includes
    """
    folder_scanner = FolderScanner()
    root_dir = "/usr/include"
    folder_scanner.scan_dir(root_dir, False)
    folder_scanner.compute_include_dirs_from_include_list(includes, root_dir)
    return folder_scanner.include_dirs
