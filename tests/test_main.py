import unittest
from unittest.mock import patch
from parameterized import parameterized
from main import *


class TestAddToMainApp(unittest.TestCase):

    def test_check_document_existance(self):
        result = check_document_existance('11-2')
        self.assertTrue(result)
        result = check_document_existance('2642662feg')
        self.assertFalse(result)

    def test_get_doc_owner_name(self):
        with unittest.mock.patch('builtins.input', return_value='11-2'):
            result = get_doc_owner_name()
            self.assertEqual(result, 'Геннадий Покемонов')
        with unittest.mock.patch('builtins.input', return_value='10006'):
            result = get_doc_owner_name()
            self.assertEqual(result, 'Аристарх Павлов')

    def test_get_all_doc_owners_names(self):
        result = get_all_doc_owners_names()
        reference = {'Василий Гупкин', 'Аристарх Павлов', 'Геннадий Покемонов'}
        self.assertEqual(result, reference)

    def test_remove_doc_from_shelf(self):
        def counter(count=0):
            for directory_number, directory_docs_list in directories.items():
                count += len(directory_docs_list)
            return count

        count_before = counter()
        remove_doc_from_shelf('2207 876234')
        count_after = counter()
        self.assertEqual(count_before, count_after + 1)

    def test_add_new_shelf(self):
        with unittest.mock.patch('builtins.input', return_value='4'):
            shelf_number, added = add_new_shelf()
            self.assertEqual(shelf_number, '4')
            self.assertTrue(added)
        with unittest.mock.patch('builtins.input', return_value='2'):
            shelf_number, added = add_new_shelf()
            self.assertEqual(shelf_number, '2')
            self.assertFalse(added)

    @parameterized.expand([('12345678', '3'), ('87654321', '5')])
    def test_append_doc_to_shelf(self, doc_number, shelf_number):
        append_doc_to_shelf(doc_number, shelf_number)
        test = doc_number in directories[shelf_number]
        self.assertTrue(test)

    @parameterized.expand([('10006', '2'), ('11-2', '1')])
    def test_get_doc_shelf(self, doc, result):
        with patch('builtins.input', return_value=doc):
            test = get_doc_shelf()
            self.assertEqual(test, result)

    @parameterized.expand([('10006', '3'), ('11-2', '2')])
    def test_move_doc_to_shelf(self, doc, shelf):
        with patch('builtins.input', side_effect=[doc, shelf]):
            move_doc_to_shelf()
            self.assertTrue(doc in directories[shelf])


class TestDeleteFromMainApp(unittest.TestCase):

    @parameterized.expand(['10006', '11-2'])
    def test_delete_doc(self, doc):
        with patch('builtins.input', return_value=doc):
            delete_doc()
            test = True
            for current_document in documents:
                doc_number = current_document['number']
                if doc_number == doc:
                    test = False
            self.assertTrue(test)

    @parameterized.expand([('4234 66', 'pass', 'Лёня Голубков', '3'), ('4537 67', 'licence', 'Немцов Борис', '5')])
    def test_add_new_doc(self, doc, typ, name, shelf):
        with patch('builtins.input', side_effect=[doc, typ, name, shelf]):
            add_new_doc()
            test = {"type": typ, "number": doc, "name": name} in documents and doc in directories[shelf]
            self.assertTrue(test)
