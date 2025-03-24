![“Ih NCAT](![/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_1_0.png](https://pyinstaller.org/en/stable/_static/pyinstaller-draft1a-100_trans.png))

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
CCNA Cheat Sheet 
 
This CCNA command ‘cheat sheet’ covers both ICND parts 1 & 2 and covers the current 
CCNA exam (640-802). 
 
Whilst not an exhaustive IOS command list it covers the majority of commands found in the 
exam. Older ‘cheat sheets’ may contain additional commands, such as IPX which is no longer 
in the exam.  
 
Cisco Modes 
 
Description 
Keyboard short cut 
User mode 
 
Switch> 
Enter Privilege mode 
 
Switch>enable 
Privileged mode 
 
Switch# 
Enter configuration mode 
 
Switch#configure terminal 
 
Global Config mode 
 
Switch(config)# 
Enter Interface mode   
 
Switch(config)#interface fa0/1 
Interface mode 
 
Switch(config-if) 
Return to global 
configuration 
 
Switch(config-if)exit 
Exit Global Config mode 
 
Switch(config)#exit 
Return to use mode 
 
Switch#disable 
Logout 
 
Switch>exit 
 
 
Keyboard Shortcuts 
 
Description 
Keyboard shortcut 
Recall Previous command 
 
Up arrow or <Ctrl> p 
Recall Next command 
 
Down arrow or <Ctrl> n 
Beginning of command 
 
<Ctrl> a 
 
End of command 
 
<Ctrl> e 
Delete input   
 
<Ctrl> d 
Exit Configuration Mode 
 
<Ctrl> z 
Complete command 
 
TAB 


| Description                    | Keyboard short cut             |
|--------------------------------|--------------------------------|
| User mode                      | Switch>                        |
| Enter Privilege mode           | Switch>enable                  |
| Privileged mode                | Switch#                        |
| Enter configuration mode       | Switch#configure terminal      |
| Global Config mode             | Switch(config)#                |
| Enter Interface mode           | Switch(config)#interface fa0/1 |
| Interface mode                 | Switch(config-if)              |
| Return to global
configuration | Switch(config-if)exit          |
| Exit Global Config mode        | Switch(config)#exit            |
| Return to use mode             | Switch#disable                 |
| Logout                         | Switch>exit                    |




| Description             | Keyboard shortcut      |
|-------------------------|------------------------|
| Recall Previous command | Up arrow or <Ctrl> p   |
| Recall Next command     | Down arrow or <Ctrl> n |
| Beginning of command    | <Ctrl> a               |
| End of command          | <Ctrl> e               |
| Delete input            | <Ctrl> d               |
| Exit Configuration Mode | <Ctrl> z               |
| Complete command        | TAB                    |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_2_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
 
 
Device Configuration 
 
Description 
Commands 
Configure device system 
name 
 
Switch(config)#hostname sw1 
 
Sets the encrypted enable 
password 
 
Switch(config)#enable secret cisco 
Sets the unencrypted enable 
password 
 
Switch(config)#enable password cisco 
Enable password encryption 
on all clear text password 
within the configuration file 
 
Switch(config)#service password-encryption 
Configure a Message Of The 
Banner, with an ending 
character of $ 
  
Switch(config)#banner motd $ 
Assign IP address to vlan 
Switch(config)#int vlan 1 
Switch(config-if)#ip addr 172.22.1.11 
255.255.255.0 
 
Assign Default gateway, note 
the mode 
 
Switch(config)#ip default-gateway 10.1.1.1 
Select one interface 
 
 
Switch(config)#int fa0/1 
 
Select a range of interfaces 
(version dependant) 
 
Switch(config)#int range fa0/1 – 12 
 
Set the interface description 
 
Switch(config-if)#description 
Add vlan using config mode 
switch(config)#vlan 11 
switch(config-vlan)#name test 
 
Configure Interface fa0/1 @ 
speed 100 Mbps and full 
duplex 
 
Switch(config-if)#speed 100 
Switch(config-if)#duplex full 
Assign interface to vlan 
 
switch(config-if)#switchport access vlan 11 
Enable Port Security.  
Switch(config-if)#switchport mode access 
Switch(config-if)#switchport port-security 
Switch(config-if)#switchport port-security 
mac-address sticky 
 
Disable Interface 
Switch(config-if)shutdown 
 
Enable Interface  
 
Switch(config-if)no shutdown 
 


| Description                                                                         | Commands                                                                                                                                          |
|-------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Configure device system
name                                                        | Switch(config)#hostname sw1                                                                                                                       |
| Sets the encrypted enable
password                                                  | Switch(config)#enable secret cisco                                                                                                                |
| Sets the unencrypted enable
password                                                | Switch(config)#enable password cisco                                                                                                              |
| Enable password encryption
on all clear text password
within the configuration file | Switch(config)#service password-encryption                                                                                                        |
| Configure a Message Of The
Banner, with an ending
character of $                    | Switch(config)#banner motd $                                                                                                                      |
| Assign IP address to vlan                                                           | Switch(config)#int vlan 1
Switch(config-if)#ip addr 172.22.1.11
255.255.255.0                                                                     |
| Assign Default gateway, note
the mode                                               | Switch(config)#ip default-gateway 10.1.1.1                                                                                                        |
| Select one interface                                                                | Switch(config)#int fa0/1                                                                                                                          |
| Select a range of interfaces
(version dependant)                                    | Switch(config)#int range fa0/1 – 12                                                                                                               |
| Set the interface description                                                       | Switch(config-if)#description                                                                                                                     |
| Add vlan using config mode                                                          | switch(config)#vlan 11
switch(config-vlan)#name test                                                                                              |
| Configure Interface fa0/1 @
speed 100 Mbps and full
duplex                          | Switch(config-if)#speed 100
Switch(config-if)#duplex full                                                                                         |
| Assign interface to vlan                                                            | switch(config-if)#switchport access vlan 11                                                                                                       |
| Enable Port Security.                                                               | Switch(config-if)#switchport mode access
Switch(config-if)#switchport port-security
Switch(config-if)#switchport port-security
mac-address sticky |
| Disable Interface                                                                   | Switch(config-if)shutdown                                                                                                                         |
| Enable Interface                                                                    | Switch(config-if)no shutdown                                                                                                                      |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_3_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
Configures 5 Telnet sessions 
each with a password of 
‘cisco’ 
 
Switch(config)#line vty 0 4 
Switch(config-line)#login 
Switch(config-line)#password cisco 
Enable and define console 
password of ‘cisco’ 
Switch(config)#line con 0 
Switch(config-line)#login 
Switch(config-line)#password cisco 
 
Synchronise console 
messages (keep what you 
have typing on the screen) 
  
Switch(config-line)#logging synchronous 
Set the timezone and 
automatically adjust 
 
  
Switch(config)#clock timezone gmt 0 
Switch(config)#clock summer-time gmt 
recurring 
Sets the switch priority for 
the vlan. This combined with 
the switch mac address 
creates the switch BID 
 
Switch(config)#spanning-tree vlan 1 priority 
4096 
Enables portfast 
 
 
Switch(config)#int fa0/1 
Switch(config-if)#spanning-tree portfast 
Enables RSTP. Other 
options are, PVST and MST 
 
Switch(config)#spanning-tree mode rapid-pvst 
Creates a vlan. Note this 
now done  in config mode 
not vlan database. Also note 
the ‘int vlan’ command does 
NOT  create vlans 
 
 
Switch(config)#vlan 2 
Switch(config-vlan)#name sales 
Assign an interface to vlan 2 
 
Switch(config-if)#switchport access vlan 2 
Unconditionally forces an 
interface into trunking. Other 
options are access and 
dynamic 
 
Switch(config-if)#switchport mode trunk 
Manually assign a switch to 
a VTP domain. A switch will 
automatically become part of 
a VTP domain if it’s currently 
in the ‘null’ domain and 
receives a VTP frame 
 
Switch(config)#vtp domain lab 
Changes the VTP mode from 
the default ‘server’ mode to 
client mode. In client mode 
no changes can be made 
 
Switch(config)#vtp mode client 
Enable the http server to 
SDM can be used 
 
Router(config)#ip http server 


| Configures 5 Telnet sessions
each with a password of
‘cisco’                                                                                                      | Switch(config)#line vty 0 4
Switch(config-line)#login
Switch(config-line)#password cisco |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Enable and define console
password of ‘cisco’                                                                                                                     | Switch(config)#line con 0
Switch(config-line)#login
Switch(config-line)#password cisco   |
| Synchronise console
messages (keep what you
have typing on the screen)                                                                                            | Switch(config-line)#logging synchronous                                                  |
| Set the timezone and
automatically adjust                                                                                                                         | Switch(config)#clock timezone gmt 0
Switch(config)#clock summer-time gmt
recurring       |
| Sets the switch priority for
the vlan. This combined with
the switch mac address
creates the switch BID                                                           | Switch(config)#spanning-tree vlan 1 priority
4096                                        |
| Enables portfast                                                                                                                                                  | Switch(config)#int fa0/1
Switch(config-if)#spanning-tree portfast                        |
| Enables RSTP. Other
options are, PVST and MST                                                                                                                     | Switch(config)#spanning-tree mode rapid-pvst                                             |
| Creates a vlan. Note this
now done in config mode
not vlan database. Also note
the ‘int vlan’ command does
NOT create vlans                                       | Switch(config)#vlan 2
Switch(config-vlan)#name sales                                     |
| Assign an interface to vlan 2                                                                                                                                     | Switch(config-if)#switchport access vlan 2                                               |
| Unconditionally forces an
interface into trunking. Other
options are access and
dynamic                                                                           | Switch(config-if)#switchport mode trunk                                                  |
| Manually assign a switch to
a VTP domain. A switch will
automatically become part of
a VTP domain if it’s currently
in the ‘null’ domain and
receives a VTP frame | Switch(config)#vtp domain lab                                                            |
| Changes the VTP mode from
the default ‘server’ mode to
client mode. In client mode
no changes can be made                                                         | Switch(config)#vtp mode client                                                           |
| Enable the http server to
SDM can be used                                                                                                                         | Router(config)#ip http server                                                            |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_4_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
Defines a username and 
password. The list can be 
used for many things from 
PPP authentication to user 
access 
 
Router(config)#username sue password cisco 
Defines a local host file. Like 
/etc/hosts in unix 
 
Router(config)#ip host mypc 10.1.1.3 
Disables DNS lookup. Useful 
when a command as been 
miss typed 
 
Router(config)#no ip domain-lookup 
Sets the logical (not 
physical) bandwidth of 
interface. This is used by 
routing protocols, SNMP 
queuing etc 
 
Router(config)#int s0 
Router(config-if)#bandwidth 
Sets the physical clock 
 
Router(config-if)#clock rate 64000 
Set the serial interface WAN 
encapsulation. Other options 
are PPP or frame-relay 
 
Router(config-if)#encapsulation hdlc 
Authentication on PPP is 
optional. This command 
enable chap on the interface. 
Other option PAP  
 
Router(config-if)#ppp authentication chap 
Defines the type of LMI 
being used. If left un-
configured the correct LMI 
type should be automatically 
detected 
 
Router(config-if)#frame-relay lmi-type cisco 
Defines a static route. 
Renumber static routes have 
an admin distance of 1. 
Therefore will over ride any 
dynamic routing. 
 
Router(config)#ip route 50.0.0.0 255.0.0.0 
10.1.2.1 
Enables RIP version 1 on all 
LOCAL interfaces which 
have a 10.x.x.x address 
 
Enables RIP version 2 
Router(config)#router rip 
Router(config-router)#network 10.0.0.0 
 
 
Router(config-router)#version 2 
Enable the router to provide 
a DHCP service. 
Router(config)#ip dhcp pool MYPOOL 
Router(dhcp-config)#network 10.1.1.0 
255.255.255.0 
Router(dhcp-config)#default-router 10.1.1.1 
Router(dhcp-config)#exit 
Router(config)#ip dhcp excluded-address 
10.1.1.1 10.1.1.99 
Changes the config register 
which controls what the 
Router(config)#config-register 0x2102 


| Defines a username and
password. The list can be
used for many things from
PPP authentication to user
access              | Router(config)#username sue password cisco                                                                                                                                                                            |
|---------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Defines a local host file. Like
/etc/hosts in unix                                                                        | Router(config)#ip host mypc 10.1.1.3                                                                                                                                                                                  |
| Disables DNS lookup. Useful
when a command as been
miss typed                                                             | Router(config)#no ip domain-lookup                                                                                                                                                                                    |
| Sets the logical (not
physical) bandwidth of
interface. This is used by
routing protocols, SNMP
queuing etc               | Router(config)#int s0
Router(config-if)#bandwidth                                                                                                                                                                     |
| Sets the physical clock                                                                                                   | Router(config-if)#clock rate 64000                                                                                                                                                                                    |
| Set the serial interface WAN
encapsulation. Other options
are PPP or frame-relay                                          | Router(config-if)#encapsulation hdlc                                                                                                                                                                                  |
| Authentication on PPP is
optional. This command
enable chap on the interface.
Other option PAP                            | Router(config-if)#ppp authentication chap                                                                                                                                                                             |
| Defines the type of LMI
being used. If left un-
configured the correct LMI
type should be automatically
detected          | Router(config-if)#frame-relay lmi-type cisco                                                                                                                                                                          |
| Defines a static route.
Renumber static routes have
an admin distance of 1.
Therefore will over ride any
dynamic routing. | Router(config)#ip route 50.0.0.0 255.0.0.0
10.1.2.1                                                                                                                                                                   |
| Enables RIP version 1 on all
LOCAL interfaces which
have a 10.x.x.x address
Enables RIP version 2                         | Router(config)#router rip
Router(config-router)#network 10.0.0.0
Router(config-router)#version 2                                                                                                                      |
| Enable the router to provide
a DHCP service.                                                                              | Router(config)#ip dhcp pool MYPOOL
Router(dhcp-config)#network 10.1.1.0
255.255.255.0
Router(dhcp-config)#default-router 10.1.1.1
Router(dhcp-config)#exit
Router(config)#ip dhcp excluded-address
10.1.1.1 10.1.1.99 |
| Changes the config register
which controls what the                                                                       | Router(config)#config-register 0x2102                                                                                                                                                                                 |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_5_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
router does when the router 
boots 
 
Creates a logical sub 
interface below the physical 
interface 
 
Enables 802.1q trunking on 
the interface 
 
Define the ip address 
 
Router(config)#int fa0/0.1 
 
 
 
Router(config-subif)#encapsulation dot1Q 1 
 
 
Router(config-subif)#ip address 10.1.1.1 
255.255.255.0 
Enable OSPF on any local 
interface which start with the 
ip address 10.1.x.x. Note the 
inverted mask 
 
Router(config-)#router ospf 1 
Router(config-router)#network 10.1.0.0 
0.0.255.255 area 0 
EIGRP can be configured in 
a similar way to RIP or the 
mask option could be used 
  
Router(config)#router eigrp 1 
Router(config-router)#network 172.16.0.0 
Or 
Router(config-router)#network 172.16.2.0 
0.0.0.255 
Defines a standard ACL. 
Standard ACL use number 
1-99 
 
Router(config)#access-list 1 permit 
172.16.1.1 
 
Defines an Extended ACL. 
The first address is the 
source IP address 
Router(config)#access-list 101 deny  tcp host 
172.16.1.1 host 172.16.2.1 eq telnet 
Router(config)#access-list 101 permit ip any 
any 
 
Use the group command to 
attach an ACL to an 
interface. 
is used under an interface if 
the ACL is to filter traffic  
 
Router(config)#interface fa0/0 
Router(config-if)#ip access-group 1 out 
 
An example using named 
ACL in stead of numbers 
Router(config)#ip access-list extended 
my_list 
Router(config-ext-nacl)# deny tcp host 
172.16.1.1 host 172.16.2.1 eq ftp 
Router(config-ext-nacl)# permit ip any any 
 
Attaching a named ACL to 
an interface 
Router(config)#int fa0/0 
Router(config-if)#ip access-group my_list in 
 
Configuring a static NAT to 
allow a server to be access 
via the Internet, using the IP 
address on interface s0/0/1 
 
Router(config)#ip nat inside source static 
10.1.1.2 interface s0/0/1 
Defining interface which NAT 
takes place between 
 
Router(config)#int fa0/0.1 
Router(config-if)#ip nat inside 
 
Enables RIPng  
Router(config)#ipv6 unicast-routing 
ROuter(config)#ipv6 router rip ccna 


| router does when the router
boots                                                                                           |                                                                                                                                                                    |
|-----------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Creates a logical sub
interface below the physical
interface
Enables 802.1q trunking on
the interface
Define the ip address | Router(config)#int fa0/0.1
Router(config-subif)#encapsulation dot1Q 1
Router(config-subif)#ip address 10.1.1.1
255.255.255.0                                       |
| Enable OSPF on any local
interface which start with the
ip address 10.1.x.x. Note the
inverted mask                         | Router(config-)#router ospf 1
Router(config-router)#network 10.1.0.0
0.0.255.255 area 0                                                                            |
| EIGRP can be configured in
a similar way to RIP or the
mask option could be used                                            | Router(config)#router eigrp 1
Router(config-router)#network 172.16.0.0
Or
Router(config-router)#network 172.16.2.0
0.0.0.255                                       |
| Defines a standard ACL.
Standard ACL use number
1-99                                                                        | Router(config)#access-list 1 permit
172.16.1.1                                                                                                                     |
| Defines an Extended ACL.
The first address is the
source IP address                                                         | Router(config)#access-list 101 deny tcp host
172.16.1.1 host 172.16.2.1 eq telnet
Router(config)#access-list 101 permit ip any
any                                 |
| Use the group command to
attach an ACL to an
interface.
is used under an interface if
the ACL is to filter traffic          | Router(config)#interface fa0/0
Router(config-if)#ip access-group 1 out                                                                                             |
| An example using named
ACL in stead of numbers                                                                              | Router(config)#ip access-list extended
my_list
Router(config-ext-nacl)# deny tcp host
172.16.1.1 host 172.16.2.1 eq ftp
Router(config-ext-nacl)# permit ip any any |
| Attaching a named ACL to
an interface                                                                                       | Router(config)#int fa0/0
Router(config-if)#ip access-group my_list in                                                                                              |
| Configuring a static NAT to
allow a server to be access
via the Internet, using the IP
address on interface s0/0/1          | Router(config)#ip nat inside source static
10.1.1.2 interface s0/0/1                                                                                               |
| Defining interface which NAT
takes place between                                                                            | Router(config)#int fa0/0.1
Router(config-if)#ip nat inside                                                                                                         |
| Enables RIPng                                                                                                               | Router(config)#ipv6 unicast-routing
ROuter(config)#ipv6 router rip ccna                                                                                            |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_6_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
Router(config)#int s0/0/0 
Router(config-if)#ipv6 rip ccna enable 
 
 
 
Privilege Commands 
 
Description 
Commands 
Manually starts the setup 
dialog which is automatically 
invoked when the device 
starts with no config 
  
Switch#setup 
Displays the config held in 
DRAM. Which is lost if not 
copy run start command is 
not used 
 
Switch#show running-config 
Displays the NVRAM (None 
volatile) config.  
 
Switch#show startup-config 
Saves the config. Without 
this command all 
changes/configuration will be 
lost. 
 
Switch#copy running-config startup-config 
Saves the running config to a 
TFTP server 
 
Switch#copy running-config tftp 
Copies IOS files to a TFTP 
server  
 
Switch#copy flash tftp 
Copies files from a TFTP 
server the device flash  
 
Switch#copy tftp flash 
 
Erase the config held in 
NVRAM. If this is followed 
with the reload command all 
configuration is lost 
 
Switch#erase startup-config 
Reboots the device 
 
Switch#reload 
Abort sequence  
 
<Shift> <Ctrl> 6 
Suspend Telnet Session 
 
<Shift> <Ctrl> 6(then let all keys go, then)x 
Show the current  sessions.  
The one with a * is your 
active session 
 
Switch#show sessions 
Forcible closes a telnet 
session 
 
Switch#disconnect 
Set the device local clock. 
Note  this is not done in 
config mode 
Switch#clock set 10:00:00 april 2 2008 


|  | Router(config)#int s0/0/0
Router(config-if)#ipv6 rip ccna enable |
|--|------------------------------------------------------------------|




| Description                                                                                           | Commands                                      |
|-------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| Manually starts the setup
dialog which is automatically
invoked when the device
starts with no config | Switch#setup                                  |
| Displays the config held in
DRAM. Which is lost if not
copy run start command is
not used             | Switch#show running-config                    |
| Displays the NVRAM (None
volatile) config.                                                            | Switch#show startup-config                    |
| Saves the config. Without
this command all
changes/configuration will be
lost.                        | Switch#copy running-config startup-config     |
| Saves the running config to a
TFTP server                                                             | Switch#copy running-config tftp               |
| Copies IOS files to a TFTP
server                                                                     | Switch#copy flash tftp                        |
| Copies files from a TFTP
server the device flash                                                      | Switch#copy tftp flash                        |
| Erase the config held in
NVRAM. If this is followed
with the reload command all
configuration is lost | Switch#erase startup-config                   |
| Reboots the device                                                                                    | Switch#reload                                 |
| Abort sequence                                                                                        | <Shift> <Ctrl> 6                              |
| Suspend Telnet Session                                                                                | <Shift> <Ctrl> 6(then let all keys go, then)x |
| Show the current sessions.
The one with a * is your
active session                                    | Switch#show sessions                          |
| Forcible closes a telnet
session                                                                      | Switch#disconnect                             |
| Set the device local clock.
Note this is not done in
config mode                                      | Switch#clock set 10:00:00 april 2 2008        |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_7_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
Display the IOS version 
along with other useful info 
e.g sys uptime, config 
register etc 
 
Switch#show version 
Displays the file contents of 
the flash 
 
Switch#show flash 
Displays the clock 
 
Switch#show clock 
Displays the users currently 
logged on 
 
Switch#show users 
By default displays the last 
10 commands  
 
Switch#show history 
Displays the ARP cache  
 
Switch#show arp 
Displays the spanning tree 
status on vlan 1 
 
Switch#show spanning-tree vlan 1 
Lists all the configured vlans 
 
Switch#show vlan 
Displays VTP info such as 
VTP mode, VTP domain, 
VTP counter.  
 
Switch#sh vtp status 
Ping selected address 
 
Switch#ping 10.1.1.1 
Extended ping. Must be in 
privilege mode 
 
Switch#ping 
Display the interface status 
 
Switch#show int fa0/1 
Displays the vlan status and 
the IP address VLAN 1 
(often the management vlan) 
 
Switch#show interfaces vlan 1 
Displays a list of CDP 
neighbours 
  
Switch#show cdp neighbors 
Extended information on the 
above 
 
Switch#show cdp neighbors details 
Display CDP packets as they 
arrive 
 
Switch#debug cdp packets 
Display ping packets as they 
arrive 
 
Switch#debug icmp packets 
Display switch MAC 
Addresses table. These 
entries are learnt from the 
source mac address in the 
Ethernet frames  
 
Switch#show mac address-table 


| Display the IOS version
along with other useful info
e.g sys uptime, config
register etc                        | Switch#show version               |
|-----------------------------------------------------------------------------------------------------------------|-----------------------------------|
| Displays the file contents of
the flash                                                                         | Switch#show flash                 |
| Displays the clock                                                                                              | Switch#show clock                 |
| Displays the users currently
logged on                                                                          | Switch#show users                 |
| By default displays the last
10 commands                                                                        | Switch#show history               |
| Displays the ARP cache                                                                                          | Switch#show arp                   |
| Displays the spanning tree
status on vlan 1                                                                     | Switch#show spanning-tree vlan 1  |
| Lists all the configured vlans                                                                                  | Switch#show vlan                  |
| Displays VTP info such as
VTP mode, VTP domain,
VTP counter.                                                    | Switch#sh vtp status              |
| Ping selected address                                                                                           | Switch#ping 10.1.1.1              |
| Extended ping. Must be in
privilege mode                                                                        | Switch#ping                       |
| Display the interface status                                                                                    | Switch#show int fa0/1             |
| Displays the vlan status and
the IP address VLAN 1
(often the management vlan)                                  | Switch#show interfaces vlan 1     |
| Displays a list of CDP
neighbours                                                                               | Switch#show cdp neighbors         |
| Extended information on the
above                                                                               | Switch#show cdp neighbors details |
| Display CDP packets as they
arrive                                                                              | Switch#debug cdp packets          |
| Display ping packets as they
arrive                                                                             | Switch#debug icmp packets         |
| Display switch MAC
Addresses table. These
entries are learnt from the
source mac address in the
Ethernet frames | Switch#show mac address-table     |




---

![“Ih NCAT](/home/aloeffler/Documents/PDF-Markdown_Output/Networking - Cisco CCNA (Kopie 2)_image_8_0.png)

 
Experts in Networking  
 
 
0870 350 4000            training@ncat.co.uk            www.ncat.co.uk  
Displays the interface 
operational status and IP 
addresses for all router 
interfaces 
 
Router#show ip interface brief 
Displays all the configured 
routing protocols  
 
Router#show ip protocols 
Displays the IP routeing 
table 
 
Router#show ip route 
Displays the NAT 
translations 
 
Router#show ip nat translations 
Displays the physical cable 
DTE/DCE, x.21, V.35, 
RS232 configuration 
 
Router#show controllers s 0 
Displays the end-to-end 
status. Recall that ‘show 
interface’ does not 
 
Router#show frame-relay pvc 
Displays the type of LMI and 
the number LMI frames 
 
Router#show frame-relay lmi 
Displays the frame relay 
inverse ARP table  
 
Router#show frame-relay map 
To be come neighbours both 
the local and remote 
interface must be correctly 
configured.   
 
Router#show ip ospf neighbor 
If adjacent routers don’t 
become neighbours. Then 
use the command to check 
the local router interface is 
configured correctly 
 
Router#show ip ospf interface 
Same information as the 
above OSPF commands but 
with EIGRP. Remember that 
AS numbers  MUST  match 
 
Router#show ip eigrp neighbor 
Same information as the 
above OSPF commands but 
with EIGRP 
 
Router#show ip eigrp interface 
IPv6 ping. Recall that :: 
means all zero in between 
 
Router#ping 2000:1000:500:3::1 
 
 


| Displays the interface
operational status and IP
addresses for all router
interfaces                                          | Router#show ip interface brief  |
|-------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| Displays all the configured
routing protocols                                                                                 | Router#show ip protocols        |
| Displays the IP routeing
table                                                                                                | Router#show ip route            |
| Displays the NAT
translations                                                                                                 | Router#show ip nat translations |
| Displays the physical cable
DTE/DCE, x.21, V.35,
RS232 configuration                                                          | Router#show controllers s 0     |
| Displays the end-to-end
status. Recall that ‘show
interface’ does not                                                         | Router#show frame-relay pvc     |
| Displays the type of LMI and
the number LMI frames                                                                            | Router#show frame-relay lmi     |
| Displays the frame relay
inverse ARP table                                                                                    | Router#show frame-relay map     |
| To be come neighbours both
the local and remote
interface must be correctly
configured.                                       | Router#show ip ospf neighbor    |
| If adjacent routers don’t
become neighbours. Then
use the command to check
the local router interface is
configured correctly | Router#show ip ospf interface   |
| Same information as the
above OSPF commands but
with EIGRP. Remember that
AS numbers MUST match                               | Router#show ip eigrp neighbor   |
| Same information as the
above OSPF commands but
with EIGRP                                                                    | Router#show ip eigrp interface  |
| IPv6 ping. Recall that ::
means all zero in between                                                                           | Router#ping 2000:1000:500:3::1  |




---

