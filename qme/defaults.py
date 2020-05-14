"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from qme.utils.file import get_userhome
import multiprocessing
import os
import sys


def getenv(variable_key, default=None, required=False, silent=True):
    """ attempt to get an environment variable. If the variable
        is not found, None is returned.

        Arguments:

         - variable_key (str) : the variable name
         - required (bool) : exit with error if not found
         - silent (bool) : Do not print debugging information
    """
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." % variable_key)
        sys.exit(1)

    if not silent and variable is not None:
        bot.verbose("%s found as %s" % (variable_key, variable))

    return variable


QME_NPROC = multiprocessing.cpu_count()
QME_WORKERS = int(getenv("QME_WORKERS", QME_NPROC * 2 + 1))
QME_SHELL = getenv("QME_SHELL", "ipython")

# Default database is filesystem
QME_DATABASE = getenv("QME_DATABASE", "filesystem")

# Determine database backend to use, and where to store config
USERHOME = get_userhome()
QME_HOME = os.path.join(USERHOME, ".qme")

# Database folder for filesystem or sqlite database
QME_DATABASE = os.path.join(QME_HOME, "database")
QME_DATABASE_STRING = os.environ.get("QME_DATABASE")