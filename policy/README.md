# Create user accounts

```sh
# Add a new users
mc admin user add myminio/ myuser2 mypassword

# Add readonly account, Create readonly policy, Set policy to user
mc admin user add myminio/ myuser_readonly mypassword
mc admin policy add myminio myuser_readonly policy/myuser_readonly.json
mc admin policy set myminio myuser_readonly user=myuser_readonly

# Add dev account, Create dev policy, set policy to user
mc admin user add myminio/ myuser_dev mypassword
mc admin policy add myminio myuser_dev policy/myuser_dev.json
mc admin policy set myminio myuser_dev user=myuser_dev

# Create group policy, Assign user to group
mc admin group add myminio mygroup_readonly myuser_readonly
mc admin group add myminio mygroup_readonly myuser_dev
mc admin policy set myminio myuser_readonly group=mygroup_readonly
```
