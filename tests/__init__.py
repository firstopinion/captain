# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import

import testdata
from testdata.test import TestCase

from captain.compat import *
from captain import Captain
from captain.reflection import ReflectMethod, ReflectCommand


#environ.QUIET_DEFAULT = ""


class FileScript(object):

#     @property
#     def instance(self):
#         return Script(self)
# 
#     @classmethod
#     def create_instance(cls, *args, **kwargs):
#         script_path = cls(*args, **kwargs)
#         return script_path.instance
# 
    @property
    def captain(self):
        c_orig = Captain.instance

        c = Captain()
        Captain.instance = c

        m = self.path.module

        Captain.instance = c_orig

        return c

    @property
    def parser(self):
        return self.captain.create_parser()

    def __init__(self, body="", **kwargs):
        self.body = self.get_body(body, **kwargs)
        self.path = self.create_script(self.body, **kwargs)
        self.cwd = self.path.basedir

    def get_body(self, body, **kwargs):
        if not body:
            body = ""

        if not isinstance(body, basestring):
            body = "\n".join(body)

        if "header" in kwargs:
            header = kwargs["header"]
            if not isinstance(header, basestring):
                header = "\n".join(header)
        else:
            header = ""
            if "__future__" not in body and "# -*-" not in body:
                header += "\n".join([
                    "# -*- coding: utf-8 -*-",
                    "from __future__ import unicode_literals, division, print_function, absolute_import",
                    "",
                ])

            if "from captain" not in body and "import captain" not in body:
                header += "\n".join([
                    #"#!/usr/bin/env python",
                    #"import sys",
                    #"sys.path.insert(0, '{}')".format(self.cwd),
                    "from captain import Command, handle, arg, args",
                    "import captain",
                    "",
                ])

            if "__version__" not in body:
                header += "\n__version__ = '0.0.1'\n\n"

        if "class" not in body:
            subcommands = kwargs.pop("subcommands", False)
            if subcommands:
                body += "\n".join([
                    "",
                    "class Foo(Command):",
                    "    '''Foo subcommand description'''",
                    "    def handle(self, *args, **kwargs):",
                    "        print('success foo')",
                    "        print('args: ', args)",
                    "        print('kwargs: ', kwargs)",
                ])

            body += "\n".join([
                "",
                "class Default(Command):",
                "    '''default subcommand description'''",
                "    def handle(self, *args, **kwargs):",
                "        print('success default')",
                "        print('args: ', args)",
                "        print('kwargs: ', kwargs)",
            ])

        if header:
            body = header + body

        if "__name__ == " not in body:
            body += "\n".join([
                "",
                "",
                "if __name__ == '__main__':",
                "    handle()",
            ])

        return body

    def command_class(self, command_name="default"):
        cap = self.captain
        return cap.commands[command_name]

    def command(self, command_name="default"):
        return self.command_class(command_name=command_name)()

    def reflect(self, command_name="default"):
        return ReflectCommand(self.captain(command_name))

    def reflect_method(self, command_name="default"):
        return ReflectMethod(self.command(command_name).handle)

    def create_script(self, body, **kwargs):
        return testdata.create_module(
            contents=body,
            #tmpdir=cwd,
        )

#     def __str__(self):
#         return self.path

#     def run(self, arg_str='', **kwargs):
#         cap = self.captain
#         kwargs.setdefault("CAPTAIN_QUIET_DEFAULT", environ.QUIET_DEFAULT)
#         return cap.run(arg_str, quiet=False, **kwargs)

    def run(self, arg_str="", **kwargs):
        s = testdata.Command(
            "{} {}".format(testdata.get_interpreter(), self.path.path),
            cwd=self.cwd,
            **kwargs
        )
        return s.run(arg_str, **kwargs)


class ModuleScript(FileScript):
    def create_script(self, body):

        m = testdata.create_module(
            module_name="{}.__main__".format(testdata.get_module_name()),
            contents=body,
            #tmpdir=cwd,
        )

        return m

