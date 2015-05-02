import os

if 'EC2' in os.environ:
    from .ec2 import *
if 'HEROKU' in os.environ:
    from .heroku import *
if 'DOKKU' in os.environ:
    from .dokku import *
if 'FLYNN' in os.environ:
    from .flynn import *
else:
    try:
        from .local import *
    except ImportError:
        from .base import *
