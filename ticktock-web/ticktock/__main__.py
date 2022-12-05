#!/usr/bin/env python3
# Entrypoint for the application

import logging
from ticktock.cmd import argparser
from ticktock.logging import setup_logger

if __name__ == "__main__":
    args = argparser.parse_args()

    # Set up the logger:
    loglevel = logging.DEBUG if args.debug else logging.INFO
    setup_logger(level=loglevel)

    args.func(args)
