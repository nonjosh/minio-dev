# %%
import pandas as pd
# %%
storage_options = {
    "anon": False,
    "key": "minio",
    "secret": "minio123",
    "client_kwargs": {
        "endpoint_url": "http://192.168.0.101:9000",
    },
}
# %%
# Require s3fs
df = pd.read_csv(
    "s3://test/people2.csv",
    storage_options=storage_options,
)
df
# %%
