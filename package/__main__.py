# This file is part of PROJECT.
#
# PROJECT is free software: you can redistribute it and/or
# modify it under the terms of the Apache 2.0 License as published by
# the Apache Software Foundation.
#
# PROJECT is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the License
# for more details.
#
# You should have received a copy of the Apache 2.0 License
# along with PROJECT.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

from .module import square
from ._version import __version__


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="Squarer of ints")
    parser.add_argument("x", type=int)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s, version {__version__}",
    )
    args = parser.parse_args()
    print(f"Square of {args.x} is {square(args.x)}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
