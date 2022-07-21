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
Tests for classical shadows
"""
import pytest
import pennylane as qml
import pennylane.numpy as np
from pennylane.shadows import ClassicalShadow

np.random.seed(777)

wires = range(3)
shots = 10000
dev = qml.device("default.qubit", wires=wires, shots=shots)


@qml.qnode(dev)
def qnode(n_wires):
    for i in range(n_wires):
        qml.Hadamard(i)
    return qml.classical_shadow(wires=range(n_wires))


shadows = [ClassicalShadow(*qnode(n_wires)) for n_wires in range(2, 3)]


class TestUnitTestClassicalShadows:
    """Unit Tests for ClassicalShadow class"""

    @pytest.mark.parametrize("shadow", shadows)
    def test_unittest_snapshots(self, shadow):
        """Test the output shape of snapshots method"""
        T, n = shadow.bitstrings.shape
        assert (T, n) == shadow.recipes.shape
        assert shadow.local_snapshots().shape == (T, n, 2, 2)
        assert shadow.global_snapshots().shape == (T, 2**n, 2**n)


class TestIntegrationShadows:
    """Integration tests for classical shadows class"""

    @pytest.mark.parametrize("shadow", shadows)
    def test_pauli_string_expval(self, shadow):
        """Testing the output of expectation values match those of exact evaluation"""

        o1 = qml.PauliX(0)
        res1 = shadow._expval_observable(o1, k=2)

        o2 = qml.PauliX(0) @ qml.PauliX(1)
        res2 = shadow._expval_observable(o1, k=2)

        res_exact = 1.0
        assert qml.math.allclose(res1, res_exact, atol=1e-1)
        assert qml.math.allclose(res2, res_exact, atol=1e-1)

    Hs = [
        qml.PauliX(0),
        qml.PauliX(0) @ qml.PauliX(1),
        1.0 * qml.PauliX(0),
        0.5 * qml.PauliX(1) + 0.5 * qml.PauliX(1),
        qml.Hamiltonian([1.0], [qml.PauliX(0) @ qml.PauliX(1)]),
    ]

    @pytest.mark.parametrize("H", Hs)
    @pytest.mark.parametrize("shadow", shadows)
    def test_expval_input_types(self, shadow, H):
        """Test ClassicalShadow.expval can handle different inputs"""
        assert qml.math.allclose(shadow.expval(H, k=2), 1.0, atol=1e-1)

    def test_reconstruct_bell_state(
        self,
    ):
        """Test that a bell state can be faithfully reconstructed"""
        wires = range(2)

        dev = qml.device("default.qubit", wires=wires, shots=10000)

        @qml.qnode(dev)
        def qnode(n_wires):
            qml.Hadamard(0)
            qml.CNOT(wires=[0, 1])
            return qml.classical_shadow(wires=range(n_wires))

        # should prepare the bell state
        bitstrings, recipes = qnode(2)
        shadow = ClassicalShadow(bitstrings, recipes)
        global_snapshots = shadow.global_snapshots()

        state = np.sum(global_snapshots, axis=0) / shadow.snapshots
        bell_state = np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]])
        assert qml.math.allclose(state, bell_state, atol=1e-1)

        # reduced state should yield maximally mixed state
        bitstrings, recipes = qnode(1)
        shadow = ClassicalShadow(bitstrings, recipes)
        global_snapshots = shadow.global_snapshots()

        state = np.sum(global_snapshots, axis=0) / shadow.snapshots
        assert qml.math.allclose(state, 0.5 * np.eye(2), atol=1e-1)
