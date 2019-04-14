import pickle
import os, errno

def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def save(self, savename, dirname=None, exc=None):
    """Saves all attributes to a Pickle file.

    Parameters
    ----------
    savename - string
        The name of the pickle file (not including the file extension) to
        write to.

    dirname - string, optional, default None
        The path/name of the directory in which the Pickle file will be
        saved. If None, the file will be saved to the current working
        directory.

    exc - array-like of strings, optional, default None
        A vector of SAM attributes to exclude from the saved file.
    """
    self._create_dict(exc)

    if (dirname is not None):
        create_folder(dirname + "/")
        f = open(dirname + "/" + savename + ".p", 'wb')
    else:
        f = open(savename + ".p", 'wb')

    pickle.dump(self.pickle_dict, f)
    f.close()


def load(self, n):
    """Loads attributes from a Pickle file.

    Loads all attributes from the specified Pickle file into the SAM
    object.

    Parameters
    ----------
    n - string
        The path of the Pickle file.
    """
    f = open(n, 'rb')
    pick_dict = pickle.load(f)
    for i in range(len(pick_dict)):
        self.__dict__[list(pick_dict.keys())[i]] = pick_dict[list(pick_dict.keys())[i]]
    f.close()


def _create_dict(self, exc):
    self.pickle_dict = self.__dict__.copy()
    if (exc):
        for i in range(len(exc)):
            try:
                del self.pickle_dict[exc[i]]
            except:
                0;  # do nothing