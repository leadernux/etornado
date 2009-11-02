#!/usr/bin/env python
#
# Copyright 2009 Eight Systems
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core
import sys

extensions = []

distutils.core.setup(
    name="etornado",
    version="0.1",
    packages = ["etornado","etornado.utils"],
    ext_modules = extensions,
    author="Eight Systems",
    author_email="python-etornado@googlegroups.com",
    url="http://etornado.eightsystems.com.br/",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="ETornado FaceBook Tornado enhancements",
)
