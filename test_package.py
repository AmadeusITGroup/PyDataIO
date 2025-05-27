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

import pytest
from package import square


@pytest.mark.parametrize(
    "x,res",
    [(1, 1), (2, 4), (-1, 1), (0, 0)],
)
def test_square(x: int, res: int) -> None:
    assert square(x) == res
