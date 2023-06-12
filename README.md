# Network_Automation_batchCreateUser
Create multiple users on multiple nodes with different settings

![image](https://github.com/EyadNasr/Network_Automation_batchCreateUser/assets/62260537/4fe3f028-f59b-454c-9de0-3a766f2c9024)


All routers are initally configured with the following:
- Interface Ethernet1/0/0 has an IP address from the subnet 192.168.200.0/24 (**.1** through **.4**) which is directly connected to the cloud network (local windows network adapter) which has the IP 192.168.200.254
- All routers are configured with ssh username: **test123** and a password: **Huawei@123**
- No other configuration is done on the routers

The script first checks whether the username and password of the user is valid then it creates the users on the required nodes (with multithreads) 
