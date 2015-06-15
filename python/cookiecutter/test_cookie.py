import unittest

import cookie

class TestSanitize(unittest.TestCase):

    def test_sanitize_no_removal(self):
        """
        Remove all whitespace and punctuation. Return first twenty characters of
        what's left.
        """

        ok_cases = [
            '',
            'asdf',
            'a',
            'A',
            'zzz',
            '23gds',
            '9',
            '0',
            '12345678901234567890',
            'mmmmmmmmmmmmmmmmmmmm',
            'mmmmmmmmmmmmmmmmmmm',
        ]
        for test_item in ok_cases:
            self.assertEquals(test_item, cookie.sanitize(test_item))

    def test_sanitize_with_removal(self):
        """
        Remove all whitespace and punctuation. Return first twenty characters of
        what's left.
        """

        changes = [
             (' ',                               '',),
             (' asdf',                           'asdf',),
             (' a',                              'a',),
             (' a',                              'a',),
             (' zzz',                            'zzz',),
             (' 23gds',                          '23gds',),
             (' 9',                              '9',),
             (' 0',                              '0',),
             (' 12345678901234567890',           '12345678901234567890',),
             (' mmmmmmmmmmmmmmmmmmmm',           'mmmmmmmmmmmmmmmmmmmm',),
             (' mmmmmmmmmmmmmmmmmmm',            'mmmmmmmmmmmmmmmmmmm',),
             ('  ',                               '',),
             (' a sdf',                           'asdf',),
             (' a ',                              'a',),
             (' a ',                              'a',),
             (' z zz',                            'zzz',),
             (' 2 3gds',                          '23gds',),
             (' 9 ',                              '9',),
             (' 0 ',                              '0',),
             (' 1 2345678901234567890',           '12345678901234567890',),
             (' m mmmmmmmmmmmmmmmmmmm',           'mmmmmmmmmmmmmmmmmmmm',),
             (' m mmmmmmmmmmmmmmmmmm',            'mmmmmmmmmmmmmmmmmmm',),
             ('  .',                               '',),
             (' a.sdf',                           'asdf',),
             (' a.',                              'a',),
             (' a.',                              'a',),
             (' z.zz',                            'zzz',),
             (' 2.3gds',                          '23gds',),
             (' 9.',                              '9',),
             (' 0.',                              '0',),
             (' 1.2345678901234567890',           '12345678901234567890',),
             (' m.mmmmmmmmmmmmmmmmmmm',           'mmmmmmmmmmmmmmmmmmmm',),
             (' m.mmmmmmmmmmmmmmmmmm',            'mmmmmmmmmmmmmmmmmmm',),
             ('rm -rf',                           'rmrf',),
             ('123456789012345678901234567890',   '12345678901234567890',),
        ]
        for input_string, output_string in changes:
            self.assertEquals(cookie.sanitize(input_string), output_string)
