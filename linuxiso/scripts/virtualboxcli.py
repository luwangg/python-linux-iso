#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse
import logging
import json
import textwrap

# Local import
# DIR_PWD = os.path.dirname(os.path.realpath('__file__'))
# sys.path.append(os.path.join(DIR_PWD, ".."))
from linuxiso.virtualbox import Virtualbox  # noqa
from linuxiso.ressources.tools import load_conf  # noqa


def argument_parser():
    #parser_c = argparse.ArgumentParser("create", add_help=False)

    # parser = argparse.ArgumentParser(
    #     prog='downloadcli',
    #     description='Program manage download of iso/image',
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    #     epilog=textwrap.dedent('''\
    #         Example of standard usage:
    #
    #             ./downloadcli --list
    #             ./downloadcli --status debian-9.6.0-strech-amd64-netinst.iso
    #             ./downloadcli --download debian-9.6.0-strech-amd64-netinst.iso
    #         '''))
    #
    # parser_c.add_argument(
    #     "-i", "--iso",
    #     help="iso/image to mount",
    #     metavar="ISO_NAME")
    # parser_c.add_argument(
    #     "-e", "--recipe",
    #     help="recipe",
    #     metavar="RECIPE")

    # parser = argparse.ArgumentParser(
    #     description='Program manage virtualbox VM',
    #     parents=[parser_c])


    parser = argparse.ArgumentParser(
        prog='virtualboxcli',
        description='Program manage virtualbox',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            Example of standard usage:

                ./virtualboxcli --list
                ./virtualboxcli --create myhostname
            '''))

    # parser = argparse.ArgumentParser(
    #     description='Program manage virtualbox VM')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l", "--list",
        help="list curent VMs status",
        action="store_true")
    group.add_argument(
        "--list-ostypes",
        help="list os type supported by Virtualbox",
        action="store_true")
    group.add_argument(
        "-c", "--create",
        help="create new VM (and mount an iso/image)",
        metavar="VM_NAME")
    group.add_argument(
        "-x", "--run",
        help="run virtualbox VM",
        metavar="VM_NAME")
    group.add_argument(
        "-r", "--remove",
        help="delete VM",
        metavar="VM_NAME_OR_UID")

    parser.add_argument(
        "-f", "--config-file",
        help="load personnal configuration file (defaut: settings.yaml)",
        metavar="CONF_FILE")

    group_vq = parser.add_mutually_exclusive_group()
    group_vq.add_argument(
        "-v", "-vv", "--verbose",
        help="enable verbosity: -v = INFO, -vv = DEBUG ",
        action="count",
        default=0)
    group_vq.add_argument(
        "-q", "--quiet",
        help="quiet mode",
        action="store_true")

    return parser


def main(args):
    """Parsing comnand line options/arguments"""
    if args:

        # Manage "verbose" and "quiet" options
        if args.verbose == 0:
            logging.basicConfig(level=logging.WARNING)
        elif args.verbose == 1:
            logging.basicConfig(level=logging.INFO)
        elif args.verbose >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif args.quiet:
            logging.basicConfig(level=logging.NOTSET)

        # Manage "config-file" options
        conf = load_conf(args.config_file)  # Manage None conf
        virtualbox = Virtualbox(conf=conf)

        # Manage "list", "create", "run" and "delete" options
        if args.list:             # List custom iso/image status
            result = virtualbox.list_vms()
            print(json.dumps(result, indent=4))
        elif args.list_ostypes:
            result = virtualbox.list_ostypes()
            # print(json.dumps(result, indent=4))
            print(json.dumps(sorted(list(result.keys())), indent=4))
        elif args.create:         # Create one VM
            virtualbox.create(args.create)
        elif args.run:            # Run one existing VM
            virtualbox.run(args.run)
        elif args.remove:         # Remoce one existing VM
            virtualbox.remove(args.remove)


if __name__ == "__main__":
    """Entry point for command ligne usage (with options/arguments)"""

    parser = argument_parser()
    args = parser.parse_args()
    main(args)


    #  Exemple of comand ligne call:
    #   python virtualbox.py -l
    #   python virtualbox.py -c testdeploy -e Debian-amd64-standard -i /home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server.iso
    #   python virtualbox.py -r testdeploy

    #   python virtualbox.py -c proliant -e Debian-amd64-raid -i /home/jnaud/var/isocustom/Custom-FullAuto-Debian-9-strech-amd64-netinst-server-proliant.iso

    # python virtualbox.py -c ubuntutest -e Debian-amd64-standard -i /home/jnaud/var/isocustom/Custom-FullAuto-Ubuntu-16.04.4-LTS-Xenial_Xerus-amd64-desktop.iso
    # python virtualbox.py -c ubuntutest -e Debian-amd64-standard -i /home/jnaud/var/isocustom/Custom-FullAuto-Ubuntu-17-Artful_Aardvark-amd64-desktop.iso
