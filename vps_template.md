# VPS Template

**Ubuntu 22 / 24**

## Common

Update

```bash
apt update -y
apt full-upgrade -y
```

Install iptables-persistent

```bash
apt install iptables-persistent -y
```

DNS

```bash
sed -i '/nameserver/d' /etc/resolv.conf
echo "nameserver 1.1.1.1" | tee -a /etc/resolv.conf
echo "nameserver 8.8.8.8" | tee -a /etc/resolv.conf
```

Preserve bash history

```bash
echo 'shopt -s histappend' >> ~/.bashrc
echo 'PROMPT_COMMAND="history -a; $PROMPT_COMMAND"' >> ~/.bashrc
source ~/.bashrc
exit
```