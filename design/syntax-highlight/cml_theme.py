"""
    My pygments syntax-highlighting theme.
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error
from pygments.token import Number, Operator, Generic, Whitespace

class CML(Style):
    """
    Pygments syntax-highlighting theme. Based on the 'colorful' theme.
    """
    default_style = ""
    styles = {
        Comment:                '#8a8a8a',
        Keyword:                '#b12ecc',
        Name:                   '#1a1a1a',
        Name.Function:          '#00aeae',
        Name.Class:             '#00aeae',
        String:                 '#4070a0',
        String.Doc:             '#0f1d94',
   }
