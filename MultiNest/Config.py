# -*- coding: UTF-8 -*-
"""
Global configuration for MultiNest.
"""

import os
import json

from logging import \
    debug, log

VERBOSE = 5


class Config(dict):
    """
    Global configuration for MultiNest.

    MultiNest.Config defines global instance of Config class: conf.
    Config stores variables as instace members e.g.:
        conf.config_file
    The variables are also accessible via dictionary interface e.g.:
        conf['conf_file']
    """

    def __init__(self, *args, **kwargs):
        """
        Upon initialisation some default values are applied to the variables.
        However to finish the initialization :py:meth:`Config.load` method
        should be called.
        """
        # Config is a dict. Make all the keys accessible as attributes while
        # retaining the dict API
        super(Config, self).__init__(*args, **kwargs)
        self.__dict__ = self

        # Define default values
        self.config_file = None  #: Config file name
        self.log_level = 'INFO'  #: Logging level
        self.log_output = None  #: Log output file name
        self.gw_url = "http://localhost:5000"

    def load(self, conf_name=None):
        """
        Load MultiNest configuration from JSON file and finalize the
        initialisation.

        :param conf_name: name of MultiNest config file. When *None* is
            provided hardcoded defaults are used.
        """

        if conf_name is not None:
            # Load configuration from option file
            debug("@Config - Loading global configuration: %s" % conf_name)
            self.config_file = conf_name
            with open(self.config_file) as _conf_file:
                _conf = json.load(_conf_file)
            log(VERBOSE, json.dumps(_conf))
            self.update(_conf)

        debug('@Config - Finalise configuration initialisation')
        # Normalize paths to full versions
        for _key, _value in self.items():
            if '_path_' in _key and isinstance(_value, (str, unicode)):
                log(VERBOSE, '@Config - Correct path to full one: %s -> %s.' %
                    (_key, _value))
                self[_key] = os.path.realpath(_value)

        # Generate subdir names
        log(VERBOSE, self)


conf = Config()
