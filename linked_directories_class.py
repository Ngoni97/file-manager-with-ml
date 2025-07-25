# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:53:09 2024

@author: Ngoni
"""

# singly linked list class for referencing directories

class LinkedDirectory(object):
    """ Creating an instance for a selected directory """
    
    class _Directory(object):
        """ Non-Public method for the directory instance """
        __slots__ = "_currentDir", "_nextDir"
        
        def __init__(self, element, nxt):
            self._currentDir = element
            self._nextDir = nxt

    class Empty(Exception):
        """ Empty list error """
        pass
    
    def __init__(self):
        """ Create an empty stack """
        self._head_Dir = None   # reference to the head/current directory
        self._dirLen = 0 # initialize the directory length

    def addDir(self, elem):
        """ Add element elem to the top of the stack """
        self._head_Dir = self._Directory(elem, self._head_Dir)
         # initially self._head_Dir = None, so it will not be linked
        # to anything
        self._dirLen += 1 # update the length  

    def callDir(self):
        """ Calls the recent previous directory and deletes it after passing it out """
        if self._dirLen == 1:
            raise Empty('Stack is empty')
        else:
            curDir = self._head_Dir._currentDir
            self._head_Dir = self._head_Dir._nextDir  # bypass the former top directory by
                                                                 # referencing the previous directory
            self._dirLen -= 1
            print('length =', self._dirLen)
        return self._head_Dir._currentDir

    def current_Dir(self):
        print('self._head_Dir._currentDir', self._head_Dir._currentDir)
        print('stack length =', self._dirLen)
        return self._head_Dir._currentDir

# LIFO
# by popping the last element/directory you delete it from the list


# testing
if __name__ == "__main__":
    print('this has been run directly without being imported\n\n') 
    Dir = LinkedDirectory()
    Dir.addDir('Ngoni')
    Dir.addDir('Tafadzwa')
    Dir.addDir('deleted')
    Dir.callDir()
    print(Dir.current_Dir())

    input('\n\nPress enter to quit')
