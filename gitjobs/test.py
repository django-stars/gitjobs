# -*- coding: utf-8 -*-
import unittest
import uuid
import datetime

from core import *

class TestJobsApi(unittest.TestCase):
    def setUp(self):
        self._id = "89126536-b6fd-11e0-8fa9-e88a8dce15b4"

    def _notexist(self):
        return Position(str(uuid.uuid4()))

    def testRepr(self):
        position = Position(self._id)
        self.assertEqual(str(position), '<Position 89126536-b6fd-11e0-8fa9-e88a8dce15b4>')
    
    def testPositionRequest(self):
        position = Position(self._id)
        self.assertEqual(position.id, self._id)
        self.assertEqual(position.company, u"Übermind")

    def testMarkdown(self):
        position = Position(self._id, markdown=True)
        #TODO: pure test, need more clever checking
        self.assertIn("**", position.description)

    def testNotExistPosition(self):
        # Note, using assertRaises in manager mode is only
        # python 2.7 compatible
        with self.assertRaises(ApiRequestError):
            data = self._notexist().id

    def testCreatedDate(self):
        position = Position(self._id)
        self.assertEqual("Mon Jul 25 20:35:36 UTC 2011",
            position.created_at)
        self.assertIsInstance(position.created, datetime.datetime)

class TestSearchPosition(unittest.TestCase):
    def setUp(self):
        self.keyword = "python"

    def testDescriptionSearch(self):
        p = Positions(description=self.keyword)
        self.assertIsInstance(p.items, list)

    def testLocationSearch(self):
        p = Positions(description=self.keyword,
            location="New York")
        #TODO, create more real test
        import pdb
        pdb.set_trace()
        self.assertEqual(p.count, 8)

if __name__ == '__main__':
    unittest.main()
