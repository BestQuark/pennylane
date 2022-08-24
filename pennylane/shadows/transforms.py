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
"""Classical shadow transforms"""

from itertools import product
from functools import reduce

import pennylane as qml
import pennylane.numpy as np


@qml.batch_transform
def __replace_obs(tape, obs, *args, **kwargs):
    # construct a new tape with everything except the measurement process
    with qml.tape.QuantumTape() as new_tape:
        for op in tape.operations:
            qml.apply(op)

        # queue the new observable
        obs(*args, **kwargs)

    def processing_fn(res):
        return qml.math.squeeze(qml.math.stack(res))

    return [new_tape], processing_fn


def _shadow_expval_diffable(H, k=1):
    """TODO: docs"""

    def decorator(qnode):
        def wrapper(*args, **kwargs):
            # pylint: disable=not-callable
            new_qnode = __replace_obs(qnode, qml.shadow_expval, H, k=k)
            return new_qnode(*args, **kwargs)

        return wrapper

    return decorator


def _shadow_expval_undiffable(H, k=1):
    """TODO: docs"""

    def decorator(qnode):
        def wrapper(*args, **kwargs):
            bits, recipes = qnode(*args, **kwargs)
            shadow = qml.shadows.ClassicalShadow(bits, recipes)
            return shadow.expval(H, k=k)

        return wrapper

    return decorator


def shadow_expval(H, k=1, diffable=False):
    """TODO: docs"""
    return _shadow_expval_diffable(H, k=k) if diffable else _shadow_expval_undiffable(H, k=k)


def _shadow_state_diffable(wires):
    """TODO: docs"""
    wires_list = [wires] if not isinstance(wires[0], list) else wires

    # all pauli observables
    all_observables = []
    for w in wires_list:
        observables = []
        for obs in product(
            *[[qml.Identity, qml.PauliX, qml.PauliY, qml.PauliZ] for _ in range(len(w))]
        ):
            observables.append(reduce(lambda a, b: a @ b, [ob(wire) for ob, wire in zip(obs, w)]))
        all_observables.extend(observables)

    def decorator(qnode):
        new_qnode = __replace_obs(qnode, qml.shadow_expval, all_observables)

        def wrapper(*args, **kwargs):
            # pylint: disable=not-callable
            results = new_qnode(*args, **kwargs)

            # cast to complex
            results = qml.math.cast(results, np.complex64)

            states = []
            start = 0
            for w in wires_list:
                # reconstruct the state given the observables and the expectations of
                # those observables
                state = 0
                for res, obs in zip(
                    results[start : start + 4 ** len(w)],
                    all_observables[start : start + 4 ** len(w)],
                ):
                    state = state + res * qml.math.cast_like(
                        qml.math.convert_like(qml.matrix(obs), res), res
                    )
                state = state / 2 ** len(w)

                states.append(state)
                start += 4 ** len(w)

            return states[0] if not isinstance(wires[0], list) else states

        return wrapper

    return decorator


def _shadow_state_undiffable(wires):
    """TODO: docs"""
    wires_list = [wires] if not isinstance(wires[0], list) else wires

    def decorator(qnode):
        def wrapper(*args, **kwargs):
            bits, recipes = qnode(*args, **kwargs)
            shadow = qml.shadows.ClassicalShadow(bits, recipes)

            states = [qml.math.mean(shadow.global_snapshots(wires=w), 0) for w in wires_list]
            return states[0] if not isinstance(wires[0], list) else states

        return wrapper

    return decorator


def shadow_state(wires, diffable=False):
    """TODO: docs"""
    return _shadow_state_diffable(wires) if diffable else _shadow_state_undiffable(wires)
