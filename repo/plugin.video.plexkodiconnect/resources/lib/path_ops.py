#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File and Path operations

Kodi xbmc*.*() functions usually take utf-8 encoded commands, thus try_encode
works.
Unfortunatly, working with filenames and paths seems to require an encoding in
the OS' getfilesystemencoding - it will NOT always work with unicode paths.
However, sys.getfilesystemencoding might return None.
Feed unicode to all the functions below and you're fine.

WARNING: os.path won't really work with smb paths (possibly others). For
xbmcvfs functions to work with smb paths, they need to be both in passwords.xml
as well as sources.xml
"""
import shutil
import os
from os import path  # allows to use path_ops.path.join, for example
import re

import xbmcvfs

# Kodi seems to encode in utf-8 in ALL cases (unlike e.g. the OS filesystem)
KODI_ENCODING = 'utf-8'
REGEX_FILE_NUMBERING = re.compile(r'''_(\d\d)\.\w+$''')


def append_os_sep(path):
    """
    Appends either a '\\' or '/' - IRRELEVANT of the host OS!! (os.path.join is
    dependant on the host OS)
    """
    separator = '/' if '/' in path else '\\'
    return path if path.endswith(separator) else path + separator


def translate_path(path):
    """
    Returns the XBMC translated path [unicode]
    e.g. Converts 'special://masterprofile/script_data'
    -> '/home/user/XBMC/UserData/script_data' on Linux.
    """
    return xbmcvfs.translatePath(path)


def exists(path):
    """
    Returns True if the path [unicode] exists. Folders NEED a trailing slash or
    backslash!!
    """
    return xbmcvfs.exists(path) == 1


def rmtree(path, *args, **kwargs):
    """Recursively delete a directory tree.

    If ignore_errors is set, errors are ignored; otherwise, if onerror
    is set, it is called to handle the error with arguments (func,
    path, exc_info) where func is os.listdir, os.remove, or os.rmdir;
    path is the argument to that function that caused it to fail; and
    exc_info is a tuple returned by sys.exc_info().  If ignore_errors
    is false and onerror is None, an exception is raised.

    """
    return shutil.rmtree(path, *args, **kwargs)


def copyfile(src, dst):
    """Copy data from src to dst"""
    return shutil.copyfile(src, dst)


def makedirs(path, *args, **kwargs):
    """makedirs(path [, mode=0777])

    Super-mkdir; create a leaf directory and all intermediate ones. Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist.  This is recursive.
    """
    return os.makedirs(path, *args, **kwargs)


def remove(path):
    """
    Remove (delete) the file path. If path is a directory, OSError is raised;
    see rmdir() below to remove a directory. This is identical to the unlink()
    function documented below. On Windows, attempting to remove a file that is
    in use causes an exception to be raised; on Unix, the directory entry is
    removed but the storage allocated to the file is not made available until
    the original file is no longer in use.
    """
    return os.remove(path)


def walk(top, topdown=True, onerror=None, followlinks=False):
    """
    Directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 3-tuple

        dirpath, dirnames, filenames

    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    Note that the names in the lists are just names, with no path components.
    To get a full path (which begins with top) to a file or directory in
    dirpath, do os.path.join(dirpath, name).

    If optional arg 'topdown' is true or not specified, the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are generated top down).  If topdown is false, the triple
    for a directory is generated after the triples for all of its
    subdirectories (directories are generated bottom up).

    When topdown is true, the caller can modify the dirnames list in-place
    (e.g., via del or slice assignment), and walk will only recurse into the
    subdirectories whose names remain in dirnames; this can be used to prune the
    search, or to impose a specific order of visiting.  Modifying dirnames when
    topdown is false is ineffective, since the directories in dirnames have
    already been generated by the time dirnames itself is generated. No matter
    the value of topdown, the list of subdirectories is retrieved before the
    tuples for the directory and its subdirectories are generated.

    By default errors from the os.listdir() call are ignored.  If
    optional arg 'onerror' is specified, it should be a function; it
    will be called with one argument, an os.error instance.  It can
    report the error to continue with the walk, or raise the exception
    to abort the walk.  Note that the filename is available as the
    filename attribute of the exception object.

    By default, os.walk does not follow symbolic links to subdirectories on
    systems that support them.  In order to get this functionality, set the
    optional argument 'followlinks' to true.

    Caution:  if you pass a relative pathname for top, don't change the
    current working directory between resumptions of walk.  walk never
    changes the current directory, and assumes that the client doesn't
    either.

    Example:

    import os
    from os.path import join, getsize
    for root, dirs, files in os.walk('python/Lib/email'):
        print root, "consumes",
        print sum([getsize(join(root, name)) for name in files]),
        print "bytes in", len(files), "non-directory files"
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

    """
    # Get all the results from os.walk and store them in a list
    walker = list(os.walk(top,
                          topdown,
                          onerror,
                          followlinks))
    for top, dirs, nondirs in walker:
        yield (top,
               [x for x in dirs],
               [x for x in nondirs])


def copytree(src, dst, *args, **kwargs):
    """
    Recursively copy an entire directory tree rooted at src to a directory named
    dst and return the destination directory. dirs_exist_ok dictates whether to
    raise an exception in case dst or any missing parent directory already
    exists.

    Permissions and times of directories are copied with copystat(), individual
    files are copied using copy2().

    If symlinks is true, symbolic links in the source tree are represented as
    symbolic links in the new tree and the metadata of the original links will
    be copied as far as the platform allows; if false or omitted, the contents
    and metadata of the linked files are copied to the new tree.

    When symlinks is false, if the file pointed by the symlink doesn’t exist, an
    exception will be added in the list of errors raised in an Error exception
    at the end of the copy process. You can set the optional
    ignore_dangling_symlinks flag to true if you want to silence this exception.
    Notice that this option has no effect on platforms that don’t support
    os.symlink().

    If ignore is given, it must be a callable that will receive as its arguments
    the directory being visited by copytree(), and a list of its contents, as
    returned by os.listdir(). Since copytree() is called recursively, the ignore
    callable will be called once for each directory that is copied. The callable
    must return a sequence of directory and file names relative to the current
    directory (i.e. a subset of the items in its second argument); these names
    will then be ignored in the copy process. ignore_patterns() can be used to
    create such a callable that ignores names based on glob-style patterns.

    If exception(s) occur, an Error is raised with a list of reasons.

    If copy_function is given, it must be a callable that will be used to copy
    each file. It will be called with the source path and the destination path
    as arguments. By default, copy2() is used, but any function that supports
    the same signature (like copy()) can be used.

    Raises an auditing event shutil.copytree with arguments src, dst.
    """
    return shutil.copytree(src, dst, *args, **kwargs)


def basename(path):
    """
    Returns the filename for path [unicode] or an empty string if not possible.
    Safer than using os.path.basename, as we could be expecting \\ for / or
    vice versa
    """
    try:
        return path.rsplit('/', 1)[1]
    except IndexError:
        try:
            return path.rsplit('\\', 1)[1]
        except IndexError:
            return ''


def create_unique_path(directory, filename, extension):
    """
    Checks whether 'directory/filename.extension' exists. If so, will start
    numbering the filename until the file does not exist yet (up to 99)
    """
    res = path.join(directory, '.'.join((filename, extension)))
    while exists(res):
        occurance = REGEX_FILE_NUMBERING.search(res)
        if not occurance:
            filename = '{}_00'.format(filename[:min(len(filename),
                                                    251 - len(extension))])
            res = path.join(directory, '.'.join((filename, extension)))
        else:
            number = int(occurance.group(1)) + 1
            if number > 99:
                raise RuntimeError('Could not create unique file: {} {} {}'.format(
                                   directory, filename, extension))
            basename = re.sub(REGEX_FILE_NUMBERING, '', res)
            res = '{}_{:02d}.{}'.format(basename, number, extension)
    return res
