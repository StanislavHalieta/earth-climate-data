from flask.json.provider import DefaultJSONProvider  
import numpy as np                                   


class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        def default_encoder(o):
            if isinstance(o, (np.int64, np.int32)):
                return int(o)
            if isinstance(o, (np.float64, np.float32)):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
            return super().default_encoder(o)
        
        kwargs['default'] = default_encoder
        return super().dumps(obj, **kwargs)
