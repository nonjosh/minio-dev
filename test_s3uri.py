# %%
import pandas as pd
# %%
storage_options = {
    "anon": False,
    "key": "minio",
    "secret": "minio123",
    "client_kwargs": {
        "endpoint_url": "http://localhost:9000",
    },
}
# %%
# Require s3fs
df = pd.read_csv(
    "s3://test/people.csv",
    storage_options=storage_options,
)
df
# %%
