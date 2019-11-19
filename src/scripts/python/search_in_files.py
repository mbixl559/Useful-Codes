#! /usr/bin/python3

"""search_in_files.py Seaches the contents of files in a directory for matches to a regex"""

__author__ = "Mark Bixler"

__version__ = "1.0.1"
__maintainer__ = "Mark Bixler"

from argparse import ArgumentParser
import sys
import re
import os

class Args:
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('commandName', type=str)
        self.parser.add_argument('pattern', type=str)
        self.parser.add_argument('-r', '--recursive', action='store_true', help="Recursively search this directory")
        self.parser.add_argument('-f', '--showFile', action='store_true', help="Show filename along with matched text")
        self.parser.add_argument('-g', '--group', type=int, help="The index of the regex group to return", default=0)
        self.parsedArgs = self.parser.parse_args(sys.argv)

    def getPattern(self):
        return self.parsedArgs.pattern
    def isRecursive(self):
        return self.parsedArgs.recursive
    def getMatchGroup(self):
        return self.parsedArgs.group
    def getShowFiles(self):
        return self.parsedArgs.showFile

class Search:
    def __init__(self, pattern, recurse=False, showFiles=False):
        self.regex = re.compile(pattern)
        self.isRecursive = recurse
        self.showFiles = showFiles

    def doSearch(self, matchGroup):
        currPath = ".";
        matches = self.searchDir(currPath, matchGroup)
        return matches

    def searchDir(self, dir, matchGroup):
        matches = []
        dirnames = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
        filenames = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        if(self.isRecursive):
            for dirname in dirnames:
                if(dirname != "." and dirname != ".."):
                    matches.extend(self.searchDir(os.path.join(dir, dirname), matchGroup))
        for fileName in filenames:
            exludes = [".png", ".jpg"]
            for ex in exludes:
                if ex in fileName:
                    continue
            with open(os.path.join(dir, fileName)) as file:
                try:
                    for line in file:
                        result = self.regex.search(line)
                        if result is not None:
                            if self.showFiles:
                                matches.append(result.group(matchGroup) + " - {}".format(os.path.join(dir, fileName)))
                            else:
                                matches.append(result.group(matchGroup))
                except:
                    continue
        return matches



if __name__ == "__main__":
    args = Args()
    search = Search(args.getPattern(), args.isRecursive(), args.getShowFiles())
    matches = search.doSearch(args.getMatchGroup())
    for match in matches:
        print(match)
