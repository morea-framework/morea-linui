# coding=utf-8
__author__ = 'casanova'

import unittest
import shutil
from MOREA.MoreaFile import MoreaFile, flattened_property_list
from Toolbox.toolbox import *
from MOREA.MoreaProperty import *

testpath = "/tmp/morea-ncursed-test"


def write_string_to_testfile(filename, string):
    fullpath = testpath + "/" + filename
    try:
        f = open(fullpath, 'w')
    except Exception as e:
        raise e
    if type(string) == unicode:
        f.write(string.encode("UTF-8"))
    else:
        f.write(string)
    f.close()
    return fullpath


class MoreaTestCase(unittest.TestCase):
    def setUp(self):
        # Making directory
        shutil.rmtree(testpath, ignore_errors=True)  # paranoid
        os.mkdir(testpath)
        return

    def tearDown(self):
        # Deleting directory
        shutil.rmtree(testpath, ignore_errors=True)  # paranoid
        return


class MoreaParsingTestCase(MoreaTestCase):
    def shortDescription(self):
        return ""


class MoreaTestAcceptingValidFiles(MoreaParsingTestCase):
    def shortDescription(self):
        return super(MoreaTestAcceptingValidFiles, self).shortDescription() + "accepting valid files, "

    def runMoreaTest(self, content):
        try:
            f = MoreaFile(write_string_to_testfile("test.md", content), warnings=False, parse_comments=True)
        except CustomException as e:
            self.fail(
                "  Cannot acquire content due to the following error:\n" +
                yellow(offset_string(str(e), 10)) + "\n\n" + offset_string(red(content), 10))
        self.assertTrue(True)
        return


class MoreaTestAcceptingValidFilesNoComments(MoreaTestAcceptingValidFiles):
    def shortDescription(self):
        return super(MoreaTestAcceptingValidFilesNoComments, self).shortDescription() + "no comments, "

    def runMoreaTest(self, content):
        super(MoreaTestAcceptingValidFilesNoComments, self).runMoreaTest(content)


class MoreaTestAcceptingValidFilesWithNoComments_Test_1(MoreaTestAcceptingValidFilesNoComments):
    def shortDescription(self):
        return super(MoreaTestAcceptingValidFilesWithNoComments_Test_1, self).shortDescription() + "minimal file."

    def runTest(self):
        content = "---\n" \
                  "test: ok\n" \
                  "---\n"
        super(MoreaTestAcceptingValidFilesWithNoComments_Test_1, self).runMoreaTest(content)


class MoreaTestAcceptingValidFilesWithNoComments_Test_2(MoreaTestAcceptingValidFilesNoComments):
    def shortDescription(self):
        return super(MoreaTestAcceptingValidFilesWithNoComments_Test_2, self).shortDescription() + "full-fledged file."

    def runTest(self):
        content = "---\n" \
                  "title: \"doubly quoted\"\n" \
                  "description: some long string\n" \
                  "  that spans multiple\n" \
                  "  lines.\n" \
                  "other: \"some long doubly\n" \
                  "  quoted string\"\n" \
                  "something: true\n" \
                  "list:\n" \
                  "  - item1\n" \
                  "  - item2\n" \
                  "  - crap\n" \
                  "other_list:\n" \
                  "- foo1\n" \
                  "- foo2\n" \
                  "---\n" \
                  "Some content\n"
        super(MoreaTestAcceptingValidFilesWithNoComments_Test_2, self).runMoreaTest(content)


class MoreaTestAcceptingValidFilesWithNoComments_Test_3(MoreaTestAcceptingValidFilesNoComments):
    def shortDescription(self):
        return super(MoreaTestAcceptingValidFilesWithNoComments_Test_3, self).shortDescription() + "unicode support."

    def runTest(self):
        content = u'---\ntitle: \" a ≥ 1 and b quoted\"\n' \
                  u'description:  a ≥ 1 and bing\n' \
                  u'  that  a ≥ 1 and b multiple\n' \
                  u'  lines.\nother: \"some  a ≥ 1 and b doubly\n' \
                  u'  quoted string\"\n' \
                  u'something: true\n' \
                  u'list:\n' \
                  u'  -  a ≥ 1 and b\n' \
                  u'  - item2\n' \
                  u'  -  a ≥ 1 and b\n' \
                  u'other_list:\n' \
                  u'-  a ≥ 1 and b\n' \
                  u'- foo2\n' \
                  u'---\n' \
                  u' a ≥ 1 and b content\n'

        super(MoreaTestAcceptingValidFilesWithNoComments_Test_3, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFiles(MoreaParsingTestCase):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFiles, self).shortDescription() + "rejecting invalid files, "

    def runMoreaTest(self, content):
        try:
            MoreaFile(write_string_to_testfile("test.md", content), warnings=False, parse_comments=True)
        except CustomException as e:
            # print "GOT EXPECTED EXCEPTION: " + str(e)
            self.assertTrue(True)
            return

        self.fail("  Failed to detect error for:\n\n" + offset_string(red(content), 10))


class MoreaTestRejectingInvalidFilesWithNoComments(MoreaTestRejectingInvalidFiles):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments, self).shortDescription() + "no comments, "


class MoreaTestRejectingInvalidFilesWithNoComments_Test_1(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_1, self).shortDescription() + "empty file."

    def runTest(self):
        content = ""
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_1, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithNoComments_Test_2(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_2, self).shortDescription() + "one new line."

    def runTest(self):
        content = "\n"
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_2, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithNoComments_Test_3(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_3, self).shortDescription() + "some strings."

    def runTest(self):
        content = "hello\n" \
                  "bye\n"
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_3, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithNoComments_Test_4(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_4, self).shortDescription() + "wrong delimiter."

    def runTest(self):
        content = "--\n" \
                  "TITLE: \"doubly quoted\"\n" \
                  "---\n" \
                  "Some random content\n"
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_4, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithNoComments_Test_5(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_5, self).shortDescription() + "empty content."

    def runTest(self):
        content = "---\n" \
                  "---\n"
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_5, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithNoComments_Test_6(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_6,
                     self).shortDescription() + "YAML as a sentence."

    def runTest(self):
        content = "---\n" \
                  "some sentence\n" \
                  "---\n" \
                  "some content\n"
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_6, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithNoComments_Test_7(MoreaTestRejectingInvalidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithNoComments_Test_7, self).shortDescription() + "broken line."

    def runTest(self):
        content = "---\n" \
                  "foo: line that\n" \
                  "is not indented" \
                  "---\n"
        super(MoreaTestRejectingInvalidFilesWithNoComments_Test_7, self).runMoreaTest(content)


class MoreaTestParsingValidFiles(MoreaParsingTestCase):
    def shortDescription(self):
        return super(MoreaTestParsingValidFiles, self).shortDescription() + "parsing valid files, "

    def runMoreaTest(self, content, parsetree):
        try:
            # print "CONTENT = ",content
            f = MoreaFile(write_string_to_testfile("test.md", content), warnings=False, parse_comments=True)
            # print "\nFLATTENED===>", flattened_property_list(f.property_list), "\n"
            # print "\nTEST===>", contents[index][1], "\n"
            self.assertEqual(cmp(parsetree, flattened_property_list(f.property_list)), 0,
                             "  Incorrect parse tree for:\n\n" + offset_string(
                                 red(content), 10) + offset_string(
                                 red("PARSED:\n" + str(flattened_property_list(f.property_list))) + "\n\n" +
                                 red("EXPECTED:\n" + str(parsetree)), 10) + "\n")

            return
        except CustomException as e:
            self.fail(
                "  Cannot acquire content due to the following error:\n" + yellow(
                    offset_string(str(e), 10)) + "\n\n" + offset_string(red(content), 10))


class MoreaTestParsingValidFilesWithNoComments(MoreaTestParsingValidFiles):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithNoComments, self).shortDescription() + "no comments, "

    def runMoreaTest(self, content, parsetree):
        super(MoreaTestParsingValidFilesWithNoComments, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithNoComments_Test_1(MoreaTestParsingValidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithNoComments_Test_1, self).shortDescription() + "full file."

    def runTest(self):
        content = "---\n" \
                  "test: ok\n" \
                  "long string: wir\n" \
                  "      - tanzen\n" \
                  "list of things:\n" \
                  "  - hello1\n" \
                  "  - hello2\n" \
                  "list of one thing:\n" \
                  "  - hello1\n" \
                  "---\n"
        parsetree = {"test": [[False, (False, "ok")]],
                     "list of things": [[False, [(False, "hello1"), (False, "hello2")]]],
                     "list of one thing": [[False, [(False, "hello1")]]],
                     "long string": [[False, (False, "wir - tanzen")]],
                     }

        super(MoreaTestParsingValidFilesWithNoComments_Test_1, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithNoComments_Test_2(MoreaTestParsingValidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithNoComments_Test_2, self).shortDescription() + "multi-line string."

    def runTest(self):
        content = "---\n" \
                  "long string: wir\n" \
                  "\n\n\n" \
                  "      - tanzen\n" \
                  "---\n"
        parsetree = {"long string": [[False, (False, "wir\n\n\n- tanzen")]]
                     }

        super(MoreaTestParsingValidFilesWithNoComments_Test_2, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithNoComments_Test_3(MoreaTestParsingValidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithNoComments_Test_3, self).shortDescription() + "unicode."

    def runTest(self):
        content = "---\n" \
                  "long string: a ≥ 1\n" \
                  "---\n"
        parsetree = {"long string": [[False, (False, u"a \u2265 1")]]
                     }

        super(MoreaTestParsingValidFilesWithNoComments_Test_3, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithNoComments_Test_4(MoreaTestParsingValidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithNoComments_Test_4, self).shortDescription() + "multi-line with #'s."

    def runTest(self):
        content = "---\n" \
                  "long string: \"something        \n" \
                  " # this hash is fine\n" \
                  "end of string\"\n" \
                  "---\n"
        parsetree = {"long string": [[False, (False, "something # this hash is fine end of string")]]
                     }

        super(MoreaTestParsingValidFilesWithNoComments_Test_4, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithNoComments_Test_5(MoreaTestParsingValidFilesWithNoComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithNoComments_Test_5,
                     self).shortDescription() + "multi-line with #'s #2."

    def runTest(self):
        content = "---\n" \
                  "long string: \"something        \n" \
                  " # this hash is fine\n" \
                  "# and so is this one      # and this one\n" \
                  "end of string\"\n" \
                  "---\n"
        parsetree = {"long string": [
            [False, (False, "something # this hash is fine # and so is this one      # and this one end of string")]]
        }

        super(MoreaTestParsingValidFilesWithNoComments_Test_5, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments(MoreaTestParsingValidFiles):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments, self).shortDescription() + "comments, "

    def runMoreaTest(self, content, parsetree):
        super(MoreaTestParsingValidFilesWithComments, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_1(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_1, self).shortDescription() + "all commented out."

    def runTest(self):
        content = "---\n" \
                  "#test: ok\n" \
                  "---\n\n"
        parsetree = {"test": [[True, (True, "ok")]]
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_1, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_2(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_2,
                     self).shortDescription() + "multiline, all commented out."

    def runTest(self):
        content = "---\n" \
                  "#long string: ok\n" \
                  "# something else\n" \
                  "#      another thing\n" \
                  "---\n\n"
        parsetree = {"long string": [[True, (True, "ok something else another thing")]]
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_2, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_3(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_3,
                     self).shortDescription() + "multiline, all commented out #2."

    def runTest(self):
        content = "---\n" \
                  "#long string:\n" \
                  "# some string\n" \
                  "# something else\n" \
                  "#      another thing\n" \
                  "---\n\n"
        parsetree = {"long string": [[True, (True, "some string something else another thing")]]
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_3, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_4(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_4,
                     self).shortDescription() + "commented-out list items."

    def runTest(self):
        content = "---\n" \
                  "title: something    \n" \
                  "list_of_stuff:   \n" \
                  "  - item1\n" \
                  "  #- item2 # some comment\n" \
                  " # # # # # # # # # #- item3\n" \
                  "#  - item4###\n" \
                  "  - item5\n" \
                  "---\n\n"
        parsetree = {'list_of_stuff': [
            [False, [(False, 'item1'), (True, 'item2'), (True, 'item3'), (True, 'item4###'), (False, 'item5')]]],
            'title': [[False, (False, 'something')]]
        }
        super(MoreaTestParsingValidFilesWithComments_Test_4, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_5(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_5,
                     self).shortDescription() + "empty list items."

    def runTest(self):
        content = "---\n" \
                  "list_of_stuff:   \n" \
                  "  - ####item1\n" \
                  "  - item2\n" \
                  "#  - item5\n" \
                  "---\n\n"
        parsetree = {'list_of_stuff': [[False, [(False, 'item2'), (True, 'item5')]]],
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_5, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_6(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_6,
                     self).shortDescription() + "multiline unquoted value."

    def runTest(self):
        content = "---\n" \
                  "#something_long: here is the\n" \
                  "# beginning\n" \
                  "# and some more\n" \
                  "---\n\n"
        parsetree = {'something_long': [[True, (True, "here is the beginning and some more")]],
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_6, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_7(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_7,
                     self).shortDescription() + "multiline quoted value."

    def runTest(self):
        content = "---\n" \
                  "#something_long: \"here is the\n" \
                  "# beginning\n" \
                  "# and some more\"\n" \
                  "---\n\n"
        parsetree = {'something_long': [[True, (True, "here is the beginning and some more")]],
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_7, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_8(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_8,
                     self).shortDescription() + "insanity."

    def runTest(self):
        content = "---\n" \
                  "#something_long: \"here is the ###\n" \
                  "# beginning ###\n" \
                  "#  # # and some # # more\"   ###### EOL # # # EOL2\n" \
                  "#extra:\n" \
                  "##### - item2 # EOL # EOL ##### EOL\n" \
                  "               ## - item3 ###\n" \
                  "# # # # # # - item4\n" \
                  "#   item4item4\n" \
                  "---\n\n"
        parsetree = {'something_long': [[True, (True, "here is the ### beginning ### # # and some # # more")]],
                     'extra': [[True, [(True, "item2"), (True, 'item3'), (True, 'item4 item4item4')]]],
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_8, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_9(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_9,
                     self).shortDescription() + "numerical values."

    def runTest(self):
        content = "---\n" \
                  "#number: 12\n" \
                  "othernumber: 42\n" \
                  "---\n\n"
        parsetree = {'number': [[True, (True, 12)]],
                     'othernumber': [[False, (False, 42)]],
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_9, self).runMoreaTest(content, parsetree)


class MoreaTestParsingValidFilesWithComments_Test_10(MoreaTestParsingValidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestParsingValidFilesWithComments_Test_10,
                     self).shortDescription() + "boolean values."

    def runTest(self):
        content = "---\n" \
                  "#stuff: false\n" \
                  "stuff2: True\n" \
                  "---\n\n"
        parsetree = {'stuff': [[True, (True, False)]],
                     'stuff2': [[False, (False, True)]],
                     }
        super(MoreaTestParsingValidFilesWithComments_Test_10, self).runMoreaTest(content, parsetree)


class MoreaTestRejectingInvalidFilesWithComments(MoreaTestRejectingInvalidFiles):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithComments, self).shortDescription() + "comments, "


class MoreaTestRejectingInvalidFilesWithComments_Test_1(MoreaTestRejectingInvalidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithComments_Test_1,
                     self).shortDescription() + "fishy commenting."

    def runTest(self):
        content = "---\n" \
                  "#test:\n" \
                  "  - itemA\n" \
                  "#  - itemB\n" \
                  "  - itemC\n" \
                  "---\n\n"
        super(MoreaTestRejectingInvalidFilesWithComments_Test_1, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithComments_Test_2(MoreaTestRejectingInvalidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithComments_Test_2,
                     self).shortDescription() + "dangling full-line comments."

    def runTest(self):
        content = "---\n" \
                  "title: \"I love \n" \
                  "   # SHOULD NOT BE LOST\n" \
                  "   C # something \"  # EOL\n" \
                  "# Hello World!!!\n" \
                  "---\n\n"

        super(MoreaTestRejectingInvalidFilesWithComments_Test_2, self).runMoreaTest(content)


class MoreaTestRejectingInvalidFilesWithComments_Test_3(MoreaTestRejectingInvalidFilesWithComments):
    def shortDescription(self):
        return super(MoreaTestRejectingInvalidFilesWithComments_Test_3,
                     self).shortDescription() + "dangling full-line comments #2."

    def runTest(self):
        content = "---\n" \
                  "title: \"I love \n" \
                  "# Hello World!!!\n" \
                  "some_property: hello\n" \
                  "# Full-line comments\n" \
                  "some_other_property: full" \
                  "---\n\n"

        super(MoreaTestRejectingInvalidFilesWithComments_Test_3, self).runMoreaTest(content)