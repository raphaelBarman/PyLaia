from __future__ import absolute_import

from typing import Optional, Callable, Union

import torch
from torch.nn.utils.rnn import PackedSequence

from laia.data import PaddedTensor
from laia.engine.feeders.feeder import Feeder


class TensorFeeder(Feeder):
    r"""Feed a PyTorch Tensor to the model.

    Args:
      device: Device Where the data should be allocated.
      requires_grad: Whether or not the `Tensor` requires grads. (default: False)
      parent_feeder: Parent feeder that should feed this. (default: None)
    """

    def __init__(
        self,
        device,  # type: Union[str, torch.device]
        requires_grad=False,  # type: bool
        parent_feeder=None,  # type: Optional[Callable]
    ):
        # type: (...) -> None
        super(TensorFeeder, self).__init__(parent_feeder)
        self._device = device
        self._requires_grad = requires_grad

    def _feed(self, x):
        if isinstance(x, torch.Tensor):
            return x.requires_grad(self._requires_grad).to(self._device)
        elif isinstance(x, PaddedTensor):
            xs = x.sizes.to(self._device)
            x = x.data.requires_grad_(self._requires_grad).to(self._device)
            return PaddedTensor(x, xs)
        elif isinstance(x, PackedSequence):
            xs = x.batch_sizes.to(self._device)
            x = x.data.requires_grad_(self._requires_grad).to(self._device)
            return PackedSequence(x, xs)
        else:
            raise ValueError("Type {!r} is not supported".format(type(x)))


# For backward compatibility
VariableFeeder = TensorFeeder
