pm_api_url      = "https://192.168.1.135:8006/api2/json"
pm_user         = "terraform@pve"
pm_password     = "password"
pm_target_node  = "local"
pm_storage      = "local-lvm"
pm_bridge       = "vmbr0"
pm_vlan         = 100
pm_gateway      = "192.168.1.1"


ci_user    = "silvio"
ci_password = "silvio"

ci_ssh_key = <<EOF
ssh-ed25519 ... silviove@silviove
ssh-ed25519 ... silvio@ansible
EOF

vm_definitions = [
  {
    name   = "ansible"
    target_node = "local"
    memory = 2048
    cores  = 2
    disk   = "10G"
    ip     = "192.168.1.5"
  },
  {
    name   = "master"
    target_node = "local"
    memory = 4096
    cores  = 3
    disk   = "20G"
    ip     = "192.168.1.6"
  },
  {
    name   = "worker1"
    target_node = "server2"
    memory = 3072
    cores  = 2
    disk   = "20G"
    ip     = "192.168.1.7"
  },
  {
    name   = "worker2"
    target_node = "server2"
    memory = 3072
    cores  = 2
    disk   = "20G"
    ip     = "192.168.1.8"
  },
  {
    name   = "nfs"
    target_node = "server2"
    memory = 2048
    cores  = 2
    disk   = "30G"
    ip     = "192.168.1.9"
  }

]

