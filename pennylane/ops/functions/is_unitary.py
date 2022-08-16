# Copyright 2018-2021 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
This module contains the qml.is_unitary function.
"""

import numpy as np

import pennylane as qml
from pennylane.operation import Operator


def is_unitary(op: Operator):
    """Check if the operation is unitary."""
    return np.allclose(
        qml.prod(op.matrix(), qml.adjoint(op)).matrix(), np.identity(op.wires**2)
    ) and np.allclose(qml.prod(qml.adjoint(op), op.matrix()).matrix(), np.identity(op.wires**2))
