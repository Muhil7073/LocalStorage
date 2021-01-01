import os
import sys
import json
import fcntl
import threading
import functools


'''
Function used to syncronize the function to make them thread-safe
'''
def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap

class LocalStorage:
    '''
    Creates a folder .localstore in the specified / default location
    '''
    def __init__(self, filepath = ""):
        self.__directory_name = ".localstore"
        if filepath != "":
            if filepath[-1] != "/":
                filepath += "/"
        self.__filelocation = filepath + self.__directory_name
        if not os.path.exists(self.__filelocation):
            os.mkdir(self.__filelocation)
        self.__filelocation += "/"

    '''
    Every key is created as a separate file, and the value is stored in the file
    Validations:
    * If value is not a JSON
    * If key length is more than 32
    * If the key aready exists or not
    * If the datastore exceeds 1GB
    * If the value exceeds 16KB
    '''
    @synchronized
    def create(self, key, value, ttl = 0):
        if type(value) != dict:
            raise Exception("Value is not a JSON object")

        if len(key) > 32:
            raise Exception("The keys must be in 32 characters length.")

        filename = self.__filelocation + key + ".json"
        if os.path.exists(filename):
            raise Exception("Key already exists")

        len_val = len(json.dumps(value))

        if (len_val + self.__get_size()) > 1024:
            raise Exception("Datastore exceeds memory limit of 1GB")

        if len_val >= 16000:
            raise Exception("File size exceeds 16KB")

        with open(filename, 'w') as fileKey:
            fcntl.flock(fileKey, fcntl.LOCK_EX)
            json.dump(value, fileKey)
            fcntl.flock(fileKey, fcntl.LOCK_UN)
            print("Key: {} with Value {} created successfully".format(key, value))
            return True

    '''
    Retrieves the json value & returns it
    Raises exception when the key doesn't exists
    '''
    @synchronized
    def get(self, key):
        filename = self.__filelocation + key + ".json"
        if not os.path.exists(filename):
            raise Exception("Key: {} doesn't exist".format(key))
        with open(filename, 'r') as fileKey:
            fcntl.flock(fileKey, fcntl.LOCK_EX)
            data = json.load(fileKey)
            fcntl.flock(fileKey, fcntl.LOCK_UN)
            return data

    '''
    Deletes the file, Returns
    true, if the file is deleted
    false, if the file doesn't exist
    '''
    @synchronized
    def delete(self, key):
        filename = self.__filelocation + key + ".json"
        if os.path.exists(filename):
            os.remove(filename)
            print("{} deleted".format(key))
            return True
        return False

    '''
    This is a helper function
    Returns an integer representation of size in MB - Size of .localstore
    '''
    def __get_size(self):
        total_size = 0
        for dirpath, _, filenames in os.walk(self.__filelocation[:-1]):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size//1024**2
