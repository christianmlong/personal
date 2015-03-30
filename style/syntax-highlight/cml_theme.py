"""
    My pygments syntax-highlighting theme.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error
from pygments.token import Number, Operator, Generic

class CML(Style):
    """
    Pygments syntax-highlighting theme.
    """
    default_style = "friendly"
    styles = {
        Comment:                'italic #888',
        Keyword:                'bold #005',
        Name:                   '#f00',
        Name.Function:          '#0f0',
        Name.Class:             'bold #0f0',
        String:                 'bg:#eee #111'
    }


