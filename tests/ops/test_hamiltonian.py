# Copyright 2018-2020 Xanadu Quantum Technologies Inc.

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
Tests for the Hamiltonian class.
"""
import numpy as np
import pytest

import pennylane as qml
from pennylane import numpy as pnp

COEFFS_PARAM_INTERFACE = [
    ([-0.05, 0.17], 1.7, "autograd"),
    (np.array([-0.05, 0.17]), np.array(1.7), "autograd"),
    (pnp.array([-0.05, 0.17], requires_grad=True), pnp.array(1.7, requires_grad=True), "autograd"),
]

try:
    from jax import numpy as jnp

    COEFFS_PARAM_INTERFACE.append((jnp.array([-0.05, 0.17]), jnp.array(1.7), "jax"))
except ImportError:
    pass

try:
    import tf

    COEFFS_PARAM_INTERFACE.append(
        (tf.Variable([-0.05, 0.17], dtype=tf.double), tf.Variable(1.7, dtype=tf.double), "tf")
    )
except ImportError:
    pass

try:
    import torch

    COEFFS_PARAM_INTERFACE.append((torch.tensor([-0.05, 0.17]), torch.tensor([1.7]), "torch"))
except ImportError:
    pass


def circuit1(param):
    qml.RX(param, wires=0)
    qml.RY(param, wires=0)
    return qml.expval(qml.PauliX(0))


def circuit2(param):
    qml.RX(param, wires=0)
    qml.RY(param, wires=0)
    return qml.expval(qml.PauliZ(0))


dev = qml.device("default.qubit", wires=2)


class TestHamiltonianCoefficients:
    @pytest.mark.parametrize("coeffs", [el[0] for el in COEFFS_PARAM_INTERFACE])
    def test_creation_different_coeff_types(self, coeffs):
        H = qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)])
        assert qml.math.allclose(coeffs, H.coeffs)

    @pytest.mark.parametrize("coeffs", [el[0] for el in COEFFS_PARAM_INTERFACE])
    def test_grouping_different_coeff_types(self, coeffs):
        H = qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(1)])
        H.group()
        assert len(H.grouped_ops) == 1
        assert np.allclose(H.grouped_coeffs[0], coeffs)
        assert len(H.grouped_ops[0]) == 2
        assert H.grouped_ops[0][0].name == "PauliX"
        assert H.grouped_ops[0][1].name == "PauliZ"

    @pytest.mark.parametrize("coeffs", [el[0] for el in COEFFS_PARAM_INTERFACE])
    def test_simplify_different_coeff_types(self, coeffs):
        H1 = qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(1)])
        H2 = qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.Identity(0) @ qml.PauliZ(1)])
        H2.simplify()

        assert H1.compare(H2)


class TestVQEEvaluation:
    @pytest.mark.parametrize("coeffs, param, interface", COEFFS_PARAM_INTERFACE)
    def test_vqe_forward_different_coeff_types(self, coeffs, param, interface):
        dev = qml.device("default.qubit", wires=2)
        H = qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)])
        H.group()

        @qml.qnode(dev, interface=interface)
        def circuit():
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(H)

        @qml.qnode(dev, interface=interface)
        def circuit1():
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(qml.PauliX(0))

        @qml.qnode(dev, interface=interface)
        def circuit2():
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(qml.PauliZ(0))

        res = circuit()
        res_expected = coeffs[0] * circuit1() + coeffs[1] * circuit2()
        assert np.isclose(res, res_expected)


class TestVQEdifferentiation:
    @pytest.mark.parametrize("simplify", [True, False])
    def test_vqe_differentiation_paramshift(self, simplify):
        coeffs = np.array([-0.05, 0.17])
        param = np.array(1.7)

        # differentiating a circuit with measurement expval(H)
        @qml.qnode(dev, diff_method="parameter-shift")
        def circuit(coeffs, param):
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(
                qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)], simplify=simplify)
            )

        grad_fn = qml.grad(circuit)
        grad = grad_fn(coeffs, param)

        # differentiating a cost that combines circuits with
        # measurements expval(Pauli)
        half1 = qml.QNode(circuit1, dev, diff_method="parameter-shift")
        half2 = qml.QNode(circuit2, dev, diff_method="parameter-shift")

        def combine(coeffs, param):
            return coeffs[0] * half1(param) + coeffs[1] * half2(param)

        grad_fn_expected = qml.grad(combine)
        grad_expected = grad_fn_expected(coeffs, param)

        assert np.allclose(grad[0], grad_expected[0])
        assert np.allclose(grad[1], grad_expected[1])

    def test_vqe_differentiation_autograd(self):
        coeffs = pnp.array([-0.05, 0.17], requires_grad=True)
        param = pnp.array(1.7, requires_grad=True)

        # differentiating a circuit with measurement expval(H)
        @qml.qnode(dev, interface="autograd")
        def circuit(coeffs, param):
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)]))

        grad_fn = qml.grad(circuit)
        grad = grad_fn(coeffs, param)

        # differentiating a cost that combines circuits with
        # measurements expval(Pauli)
        half1 = qml.QNode(circuit1, dev, interface="autograd")
        half2 = qml.QNode(circuit2, dev, interface="autograd")

        def combine(coeffs, param):
            return coeffs[0] * half1(param) + coeffs[1] * half2(param)

        grad_fn_expected = qml.grad(combine)
        grad_expected = grad_fn_expected(coeffs, param)

        assert np.allclose(grad[0], grad_expected[0])
        assert np.allclose(grad[1], grad_expected[1])

    def test_vqe_differentiation_jax(self):

        jax = pytest.importorskip("jax")
        jnp = pytest.importorskip("jax.numpy")
        coeffs = jnp.array([-0.05, 0.17])
        param = jnp.array(1.7)

        # differentiating a circuit with measurement expval(H)
        @qml.qnode(dev, interface="jax")
        def circuit(coeffs, param):
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)]))

        grad_fn = jax.grad(circuit)
        grad = grad_fn(coeffs, param)

        # differentiating a cost that combines circuits with
        # measurements expval(Pauli)
        half1 = qml.QNode(circuit1, dev, interface="jax")
        half2 = qml.QNode(circuit2, dev, interface="jax")

        def combine(coeffs, param):
            return coeffs[0] * half1(param) + coeffs[1] * half2(param)

        grad_fn_expected = jax.grad(combine)
        grad_expected = grad_fn_expected(coeffs, param)

        assert np.allclose(grad[0], grad_expected[0])
        assert np.allclose(grad[1], grad_expected[1])

    def test_vqe_differentiation_torch(self):

        torch = pytest.importorskip("torch")
        coeffs = torch.tensor([-0.05, 0.17], requires_grad=True)
        param = torch.tensor(1.7, requires_grad=True)

        # differentiating a circuit with measurement expval(H)
        @qml.qnode(dev, interface="torch")
        def circuit(coeffs, param):
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)]))

        res = circuit(coeffs, param)
        res.backward()
        grad = (coeffs.grad, param.grad)

        # differentiating a cost that combines circuits with
        # measurements expval(Pauli)

        # we need to create new tensors here
        coeffs2 = torch.tensor([-0.05, 0.17], requires_grad=True)
        param2 = torch.tensor(1.7, requires_grad=True)

        half1 = qml.QNode(circuit1, dev, interface="torch")
        half2 = qml.QNode(circuit2, dev, interface="torch")

        def combine(coeffs, param):
            return coeffs[0] * half1(param) + coeffs[1] * half2(param)

        res_expected = combine(coeffs2, param2)
        res_expected.backward()
        grad_expected = (coeffs2.grad, param2.grad)

        assert np.allclose(grad[0], grad_expected[0])
        assert np.allclose(grad[1], grad_expected[1])

    def test_vqe_differentiation_tf(self):
        tf = pytest.importorskip("tf")
        coeffs = tf.Variable([-0.05, 0.17], dtype=tf.double)
        param = tf.Variable(1.7, dtype=tf.double)

        # differentiating a circuit with measurement expval(H)
        @qml.qnode(dev, interface="tf")
        def circuit(coeffs, param):
            qml.RX(param, wires=0)
            qml.RY(param, wires=0)
            return qml.expval(qml.Hamiltonian(coeffs, [qml.PauliX(0), qml.PauliZ(0)]))

        with tf.GradientTape() as tape:
            res = circuit(coeffs, param)
        grad = tape.gradient(res, [coeffs, param])

        # differentiating a cost that combines circuits with
        # measurements expval(Pauli)

        # we need to create new tensors here
        coeffs2 = tf.Variable([-0.05, 0.17], dtype=tf.double)
        param2 = tf.Variable(1.7, dtype=tf.double)
        half1 = qml.QNode(circuit1, dev, interface="tf")
        half2 = qml.QNode(circuit2, dev, interface="tf")

        def combine(coeffs, param):
            return coeffs[0] * half1(param) + coeffs[1] * half2(param)

        with tf.GradientTape() as tape2:
            res_expected = combine(coeffs2, param2)
        grad_expected = tape2.gradient(res_expected, [coeffs2, param2])

        assert np.allclose(grad[0], grad_expected[0])
        assert np.allclose(grad[1], grad_expected[1])
