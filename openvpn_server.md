# OpenVPN Server - With Port Forward

[Source](https://github.com/angristan/openvpn-install)

## Install OpenVPN Server

Download one-click install script

```bash
curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
```

Install

```bash
export AUTO_INSTALL=y
./openvpn-install.sh
```

**From HOST** download ovpn file (2.2.2.2 is your vps ip address):

```bash
scp root@2.2.2.2:/root/client.ovpn ./
```

**Switch to VPS**

## Port Forward

Example for `5000/tcp`

Replace `12.12.12.12` with the public ip address of VPS.

Replace `10.8.0.2` with the private IP of the VPN client. The first client that connects is assigned that IP address. For static IPs, modify the ovpn client file and add:

```bash
ifconfig-push 10.8.0.3 255.255.255.0
```

Install iptables-persistent

```bash
apt install iptables-persistent -y
```

Iptables.

```bash
iptables -t nat -A PREROUTING -p tcp -d 5.22.216.24 --dport 5000 -j DNAT --to-destination 10.8.0.2:5000
iptables -A FORWARD -p tcp -d 10.8.0.2 --dport 5000 -j ACCEPT
netfilter-persistent save
```