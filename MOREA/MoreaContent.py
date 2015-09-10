from Toolbox.toolbox import CustomException
from MoreaFile import MoreaFile
from MoreaGrammar import MoreaGrammar

import os
import re

__author__ = 'casanova'


class MoreaContent(object):
    """ A class for the whole MOREA Web site content """

    def __init__(self):
        self.files = []

    def acquire_all_content(self, root, parse_comments):
        if not os.path.isdir(root):
            raise CustomException("Can't find master/src/morea in the working directory... aborting!")

        err = False
        err_msg = ""
        self.files = []
        for path, subs, files in os.walk(root):
            for f in files:
                if re.match(".*.md$", f) is not None:
                    try:
                        self.files.append(MoreaFile(path + "/" + f, warnings=True, parse_comments=parse_comments))
                    except CustomException as e:
                        err_msg += str(e)
                        err = True
        if err:
            raise CustomException(err_msg)

        print "  Acquired content from " + str(len(self.files)) + " MOREA .md files"
        return

    def check(self):
        try:
            self.type_check()
            self.reference_check()
        except CustomException as e:
            raise e
        return

    def type_check(self):

        print "  Type-checking..."

        err_msg = ""
        for f in self.files:
            # print "****************************", f.path
            try:
                f.typecheck()
            except CustomException as e:
                err_msg += f.path + ":\n" + unicode(e)

        if err_msg != "":
            raise CustomException(err_msg)

        return

    def reference_check(self):

        try:
            print "  Checking for duplicate ids..."
            self.check_for_duplicate_ids()

            print "  Checking for dangling references..."
            self.check_for_invalid_references()

        except CustomException as e:
            raise e

        return

    def save(self):
        print "SAVE: NOT IMPLEMENTED YET"
        return

    def check_for_duplicate_ids(self):
        err_msg = ""

        # Build list of ALL ids
        ids = [[f.path, f.get_value_of_scalar_required_property("morea_id")] for f in self.files]

        # Find duplicates (very inefficient, but makes error reporting nice)
        for [path, id] in ids:
            if len([[p, i] for [p, i] in ids if id == i]) > 1:
                err_msg += "  Error: Duplicated morea_id " + id + " (one occurrence in file " + path + ")\n"

        if err_msg != "":
            raise CustomException(err_msg)

        return

    def check_for_invalid_references(self):

        err_msg = ""

        for f in self.files:
            reference_list = f.get_reference_list()
            for [label, idstring] in reference_list:
                if idstring is not None:
                    referenced_list = None
                    try:
                        referenced_file = self.get_file(idstring)
                    except CustomException as e:
                        err_msg += "  Error: " + f.path + " references unknown morea_id " + idstring + "\n"
                    continue

                    morea_type = referenced_file.get_value_of_scalar_required_property("morea_type")
                    if not MoreaGrammar.is_valid_reference(label, morea_type):
                        print "label=", label, "idstring= ", idstring
                        err_msg += "  Error: File " + f.path + " mistakenly references id " + idstring + \
                                   ", which is of type " + \
                                   referenced_file.get_value_of_scalar_required_property("morea_type") + \
                                   ", as part of " + label + "\n"

        if err_msg != "":
            raise CustomException(err_msg)

        return

    def get_file(self, id_string):
        for f in self.files:
            if f.get_value_of_scalar_required_property("morea_id") == id_string:
                return f
        raise CustomException("")

    def save(self):
        # TODO
        print "SAVE: not implemented"
        return