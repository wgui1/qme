"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


def init_db(database, config_dir=None):
    """Initialize the database, meaning a base client and appropriate functions
       to save, or generate a unique ID based on the backend being used. Each
       client has it's own init to check for a connection (or filesystem 
       path existence) and then functions to interact with entities.
    """
    # Question: are postgres /mysql different here?
    if database == "filesystem":
        from .filesystem import FileSystemDatabase as Database
    elif database.startswith("sqlite"):
        from .sqlite import SqliteDatabase as Database
    else:
        from .relational import RelationalDatabase as Database
    return Database(config_dir=config_dir)