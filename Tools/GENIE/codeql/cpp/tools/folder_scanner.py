import os
import pathlib

from dir_trie import DirTrie
from include_extractor import IncludeExtractor


class FolderScanner:
    # Dir trie used to index the files
    dir_trie = DirTrie()
    # Set of common C/C++ source file extensions
    cpp_source_extensions = ['.c', '.cpp', '.cc', '.cxx', '.c++']
    # Set of common C/C++ header file extensions
    cpp_header_extensions = ['.h', '.hpp', '.hxx', 'hh', 'h++', '.inc']
    # Set of all files in the indexed directory
    all_files = set()
    # Set of all source files in the indexed directory
    source_files = set()
    # Set of all header files in the indexed directory
    header_files = set()
    # Set of visited files.
    visited_files = set()
    # Include file extractor. As it contains a cache of file --> include files it should be reused
    include_extractor = IncludeExtractor()
    # Set of missing include files still left after the processing
    missing_includes = set()
    # Set of include directories to be used to resolve includes
    include_dirs = set()

    def __init__(self, cpp_source_extensions=None, cpp_header_extensions=None):
        """Create an empty FolderScanner"""
        if cpp_source_extensions is not None:
            self.cpp_source_extensions = cpp_source_extensions
        if cpp_header_extensions is not None:
            self.cpp_header_extensions = cpp_header_extensions

    def reset(self):
        """
        Reset the FolderScanner to its initial state keeping the directory trie and include
        extractor
        """
        self.visited_files = set()
        self.include_dirs = set()

    def scan_dir(self, root_dir, follow_symlinks=False):
        """Scan a directory and index its files"""
        self.dir_trie.of_dir(root_dir, follow_symlinks)
        all_files = self.dir_trie.get_paths()
        # Computing some stats
        for path in all_files:
            fullname = os.path.join(*path)
            self.all_files.add(fullname)
            _, file_extension = os.path.splitext(fullname)
            if file_extension.lower() in self.cpp_source_extensions:
                self.source_files.add(fullname)
            elif file_extension.lower() in self.cpp_header_extensions:
                self.header_files.add(fullname)

        print("Indexing folder {}, found {} source files, {} header files, {} total files.".format(
            root_dir, len(self.source_files), len(self.header_files), len(self.all_files)))

    def file_exists(self, fullpath):
        """Test if a file exists"""
        return fullpath in self.all_files

    @staticmethod
    def include_dir_distance(src, include_dir):
        """
        Calculate a distances score for the include dir relative to the src
        The algorithm will prioritize any include directory in a subdirectory of the source file
        """
        try:
            common_path = os.path.commonpath([src, include_dir])
        except ValueError:
            # If the paths are on different drives, commonpath will raise a ValueError
            # We just return a very high distance in this case
            return 100000
        common_dirs = common_path.count(os.path.sep)
        # Include ending directory in the count if any
        if common_path[-1] != os.path.sep:
            common_dirs += 1

        src_dirs = src.count(os.path.sep) - 1  # Will always have a file also
        include_dirs = include_dir.count(os.path.sep)

        return (src_dirs - common_dirs) * 1000 + (include_dirs - common_dirs)

    def resolve_include(self, src, include_file):
        """
        Resolve an include based on file it's included from.
        Return the file to be included and the directory that should be used to include the file,
        or none if there is no solution
        """

        dirs = self.dir_trie.lookup(include_file)
        if dirs == []:
            return None

        include_dirs = []
        for d in dirs:
            fulldir = os.path.join(*d)  # This is the dir to be included.
            fullpath = os.path.join(fulldir, include_file)
            distance = self.include_dir_distance(src, fulldir)
            include_dirs.append((distance, (fulldir, fullpath)))
            # No need to check if already in one of the include dirs as this is done earlier

        return min(include_dirs)[1]

    def exists_on_disk(self, include_file, include_dirs):
        """
        Find the full path of the include file by searching though the given include paths
        The function returns the absolute path to the include file in the first directory that
        contains it
        """
        for d in include_dirs:
            fullpath = os.path.abspath(os.path.join(d, include_file))
            if self.file_exists(fullpath):
                return fullpath

        return None

    @staticmethod
    def is_absolute(path):
        """
        check if the given path is an absolute path in either posix or windows.
        """
        windows_path = pathlib.PureWindowsPath(path)
        posix_path = pathlib.PurePosixPath(path)
        return windows_path.is_absolute() or posix_path.is_absolute()

    def compute_include_dirs_from_include_list(self, includes, src):
        """
        Compute the set of include directories needed to resolve a set of include directives and a
        file containing them (used to determine the path distance).
        The function processes includes transitively, and mimics the compilers' behaviour when
        resolving includes.
        """
        stack = []
        for include in includes:
            # We do not process include files specified through an absolute path
            if not self.is_absolute(include):
                stack.append((include, src))

        # We keep processing includes files from the stack until the stack is empty
        while len(stack) > 0:
            current_include, current_src = stack.pop()

            include_file = self.exists_on_disk(current_include, self.include_dirs)
            # Could we find it?
            if include_file is None:

                # Don't try to resolve relative files by traversing include directories.
                if current_include[0] == '.':
                    continue

                inc = self.resolve_include(current_src, current_include)
                if inc is None:
                    self.missing_includes.add(current_include)
                    continue

                (include_dir, include_file) = inc
                self.include_dirs.add(include_dir)

            if include_file not in self.visited_files:
                # We never visited this file. Add its own includes to the queue
                inner_includes = self.include_extractor.extract_includes(include_file)
                for inner_include in inner_includes:
                    if not self.is_absolute(inner_include):
                        stack.append((inner_include, include_file))
                # Mark the include file as visited
                self.visited_files.add(include_file)

    def get_include_dirs_from_source(self, src):
        """
        Compute the transitive set of include directories needed to compile the given source file.
        """
        include_files = self.include_extractor.extract_includes(src)
        # Reset the state to avoid conflicting with other scanners
        self.reset()
        self.compute_include_dirs_from_include_list(include_files, src)
        return self.include_dirs
