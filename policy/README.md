# Create user accounts

```sh
mc admin user add myminio/ myuser2 mypassword
mc admin user add myminio/ mymyuser_dev mypassword
mc admin policy add myminio myuser_dev policy/myuser_dev.json
mc admin policy set myminio myuser_dev user=myuser_dev
mc admin user add myminio/ myuser_readonly mypassword
mc admin policy add myminio myuser_readonly policy/myuser_readonly.json
mc admin policy set myminio myuser_readonly user=myuser_readonly
mc admin group add myminio mygroup_readonly myuser_readonly
mc admin group add myminio mygroup_readonly myuser_dev
mc admin policy set myminio myuser_readonly group=mygroup_readonly
```
