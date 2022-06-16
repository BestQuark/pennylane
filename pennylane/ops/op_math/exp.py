# Copyright 2018-2022 Xanadu Quantum Technologies Inc.

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
This submodule defines the symbolic operator that represents e raised to an operator.
"""
from scipy.linalg import expm
from scipy.sparse.linalg import expm as sparse_expm


from pennylane import numpy as np
from pennylane.operation import expand_matrix
from pennylane.wires import Wires

from .symbolicop import SymbolicOp


class Exp(SymbolicOp):
    """class docstring"""

    coeff = 1
    """The numerical coefficient of the operator in the exponential."""

    def __init__(self, coeff=1, base=None, do_queue=True, id=None):
        self.coeff = coeff
        super().__init__(base, do_queue=do_queue, id=id)
        self._name = f"Exp({coeff} {base.name}"
        self._check_batching([coeff] + self.base.parameters)

    @property
    def data(self):
        return [self.coeff] + self.base.data

    @data.setter
    def data(self, new_data):
        self.coeff = new_data[0]
        self.base.data = new_data[1:]

    @property
    def parameters(self):
        return self.data.copy()

    @property
    def num_params(self):
        return self.base.num_params + 1

    @property
    def ndim_params(self):
        return (0,) + self.base.ndim_params

    def matrix(self, wire_order=None):
        mat = expm(self.coeff * self.base.matrix())

        if wire_order is None or self.wires == Wires(wire_order):
            return mat

        return expand_matrix(mat, wires=self.wires, wire_order=wire_order)

    def sparse_matrix(self, wire_order=None):
        if wire_order is not None:
            raise NotImplementedError("Wire order is not implemented for sparse_matrix")

        base_smat = self.coeff * self.base.sparse_matrix()
        return sparse_expm(base_smat)

    def diagonalizing_gates(self):
        return self.base.diagonalizing_gates()

    def eigvals(self):
        return np.exp(self.base.eigvals())

    def generator(self):
        return self.base
