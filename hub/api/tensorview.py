from hub.features import featurify, FeatureConnector, FlatTensor
from hub.store.storage_tensor import StorageTensor

class TensorView:
    def __init__(
        self,
        token=None,
        num_samples: int = None,
        mode: str = None,
        dtype=None,
        path=None,
        slice_=None,
        _tensors=None,
        offset=0
    ):
        assert dtype is not None
        assert num_samples is not None
        assert mode is not None
        assert path is not None
        assert _tensors is not None

        self.token = token
        self.mode = mode
        self.num_samples = num_samples
        self.dtype: FeatureConnector = dtype
        # self._flat_tensors: Tuple[FlatTensor] = tuple(self.dtype._flatten())
        self._tensors = _tensors
        self.path=path
        self.offset = offset
        self.slice_=slice_
        if self.slice_ is not None and len(self.slice_)!=0:
            ls=list(self.slice_)
            # we assign to ls instead of adding offset to prevent doubling offset                
            if isinstance(ls[0],int):
                ls[0]=self.offset
            elif isinstance(ls[0],slice):
                ls[0]=slice(self.offset,offset+num_samples)
            self.slice_=tuple(ls)
        else:
            self.slice_=slice(self.offset,offset+num_samples)

    
    def numpy(self):
        if self.slice_ is None:
            return self._tensors[self.path][:]
        return self._tensors[self.path][self.slice_]