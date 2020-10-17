# utils.py

from typing import List
import numpy as np
class Indexer(object):
    """
    Bijection between objects and integers starting at 0. Useful for mapping labels, features, etc. into coordinates of a vector space.

    Attributes:
        objs_to_ids
        ids_to_objs
    """
    def __init__(self):
        self.objs_to_ids = {}
        self.ids_to_objs = {}

    def __repr__(self):
        # return str([(name, id) for name,id in zip(self.username_to_session_id, self.session_id_to_username)])
        # return str([key[value] for key, value in self.ids_to_objs.items()])
        return str(self.ids_to_objs)

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.objs_to_ids)

    def get_id(self, object):
        """
        :param object: object to look up
        :return: Returns -1 if the object isn't present, index otherwise
        """
        if (object not in self.objs_to_ids):
            return -1
        else:
            return self.objs_to_ids[object]

    def get_object(self, id):
        """
        :param index: integer index to look up
        :return: Returns the object corresponding to the particular index or None if not found
        """
        if (id not in self.ids_to_objs):
            return None
        else:
            return self.ids_to_objs[id]

    def contains(self, object):
        """
        :param object: object to look up
        :return: Returns True if it is in the Indexer, False otherwise
        """
        return self.get_object(object) != -1

    def add_item(self, id, object):
        if (object not in self.objs_to_ids):
            self.objs_to_ids[object] = id
            self.ids_to_objs[id] = object
        return self.objs_to_ids[object]
            
class Finder(object):
    """
    Bijection between uername and session_id. Useful for mapping labels, features, etc. into coordinates of a vector space.

    Attributes:
        username_to_session_id
        session_id_to_username
    """
    def __init__(self):
        self.username_to_session_id = {}
        self.session_id_to_username = {}

    def __repr__(self):
        # return str([str(self.get_username(i)) for i in range(0, len(self))])
        return str([(name, id) for name,id in zip(self.username_to_session_id, self.session_id_to_username)])

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.username_to_session_id)

    def get_session_id(self, username):
        """
        :param object: object to look up
        :return: Returns -1 if the object isn't present, index otherwise
        """
        if (username not in self.username_to_session_id):
            return -1
        else:
            return self.username_to_session_id[username]

    def get_username(self, session_id):
        """
        :param index: integer index to look up
        :return: Returns the object corresponding to the particular index or None if not found
        """
        if (session_id not in self.session_id_to_username):
            return None
        else:
            return self.session_id_to_username[session_id]

    def contains(self, username):
        """
        :param username: username to look up
        :return: Returns True if it is in the Indexer, False otherwise
        """
        return self.get_session_id(username) != -1

    def add_user(self, username, session_id):
        if (username not in self.username_to_session_id):
            new_session_id = session_id
            self.username_to_session_id[username] = new_session_id
            self.session_id_to_username[new_session_id] = username
        return self.username_to_session_id[username]

if __name__ == '__main__':

# =============== Testing Finder =============================
    # session_list = [i for i in range(9)]
    # user_list = [chr(ord('a')+i) for i in range(9)]
    # age = 21
    # language = "en"
    # finder = Finder()
    # for i in range(len(user_list)):
    #     finder.add_user(user_list[i], session_list[i])
    # print(finder)
    # user_name = finder.get_username(1)
    # print(user_name)
    # print(finder.contains(user_name))
    # print(finder.get_session_id(user_name))

    # =============== Testing Indexer =============================
    sentence = [chr(ord('a')+i) for i in range(26)]
    indexer = Indexer()
    for i in range(len(sentence)):
        indexer.add_item(i, sentence[i])
    print(indexer)
    print(indexer.get_object(1))
    print(indexer.contains('a'))
    print(indexer.contains('??'))
    print(indexer.get_id('z'))

    # Expected: 
    # b
    # True
    # False
    # 25
    # for i in range(10):
    #     print(indexer.get_object(i))

    # import numpy as np
    # h = np.append(np.zeros(50), np.ones(50))
    # y = np.ones(100)
    # tmp=[a==b for a, b in zip(h, y)]
    # print(f"h = {h}, y = {y}")
    # print(sum(tmp))
    # print(len(tmp))
    # x = sum(tmp)/len(tmp)*100.0
    # print(f"x: {x}")