#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:
    project: StatQuest
    name: test_statquest_relations.py
    version: 0.5.1.2
    date: 21.03.2024

Authors:
    Sławomir Marczyński

Copyright (c) 2023 Sławomir Marczyński.
"""

from unittest import TestCase
from unittest.mock import Mock

from statquest_relation import Relation


class TestRelation(TestCase):

    def test_credible_1(self):
        alpha = 0.05
        test_positive = Mock()
        test_positive.prove_relationship = True
        relation = Relation(Mock(), Mock(), test_positive, 0.5, alpha - 0.0001)
        result = relation.credible(alpha)
        self.assertTrue(result)

    def test_credible_2(self):
        alpha = 0.05
        test_positive = Mock()
        test_positive.prove_relationship = True
        relation = Relation(Mock(), Mock(), test_positive, 0.5, alpha + 0.0001)
        result = relation.credible(alpha)
        self.assertFalse(result)

    def test_credible_3(self):
        alpha = 0.05
        test_negative = Mock()
        test_negative.prove_relationship = False
        relation = Relation(Mock(), Mock(), test_negative, 0.5,
                            1.0 - alpha + 0.0001)
        result = relation.credible(alpha)
        self.assertTrue(result)

    def test_credible_4(self):
        alpha = 0.05
        test_negative = Mock()
        test_negative.prove_relationship = False
        relation = Relation(Mock(), Mock(), test_negative, 0.5,
                            1.0 - alpha - 0.0001)
        result = relation.credible(alpha)
        self.assertFalse(result)

    def test_create_relations_1(self):
        expected = {}
        result = Relation.create_relations([], Mock())
        self.assertEqual(expected, result)

    def test_create_relations_2(self):
        expected = {}
        result = Relation.create_relations(Mock(), [])
        self.assertEqual(expected, result)

    def test_create_relations_3(self):
        expected = {}
        result = Relation.create_relations([], [])
        self.assertEqual(expected, result)

    def test_credible_only_1(self):
        relations = {}
        expected = {}
        result = Relation.credible_only(relations, 0.05)  # alpha = 0.05
        self.assertDictEqual(expected, result)

    def test_credible_only_2(self):
        r1 = Mock()
        r2 = Mock()
        r3 = Mock()
        r4 = Mock()
        r1.credible.return_value = True
        r2.credible.return_value = True
        r3.credible.return_value = False
        r4.credible.return_value = True
        relations = {1: [r1], 2: [r1, r2], 3: [r3], 4: [r4, r3]}
        expected = {1: [r1], 2: [r1, r2], 4: [r4]}
        result = Relation.credible_only(relations, 0.05)  # alpha = 0.05
        self.assertDictEqual(expected, result)

    def test_credible_only_3(self):
        r1 = Mock()
        r2 = Mock()
        r3 = Mock()
        r4 = Mock()
        r1.credible.return_value = True
        r2.credible.return_value = True
        r3.credible.return_value = True
        r4.credible.return_value = True
        relations = {1: [r1], 2: [r1, r2], 3: [r3], 4: [r4, r3]}
        expected = relations
        result = Relation.credible_only(relations, 0.05)  # alpha = 0.05
        self.assertDictEqual(expected, result)

    def test_credible_only_4(self):
        r1 = Mock()
        r2 = Mock()
        r3 = Mock()
        r4 = Mock()
        r1.credible.return_value = False
        r2.credible.return_value = False
        r3.credible.return_value = False
        r4.credible.return_value = False
        relations = {1: [r1], 2: [r1, r2], 3: [r3], 4: [r4, r3]}
        expected = {}
        result = Relation.credible_only(relations, 0.05)  # alpha = 0.05
        self.assertDictEqual(expected, result)
