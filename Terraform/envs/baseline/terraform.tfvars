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

ci_ssh_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAaL6ZpiCzkbjN2feimCco5TeaGEQs4UEXVC0WWX/1rH silviove@silviove"

vm_definitions = [
  {
    name   = "ansible"
    memory = 2048
    cores  = 2
    disk   = "10G"
    ip     = "192.168.1.5"
  },
  {
    name   = "k8s-cp"
    memory = 2048
    cores  = 2
    disk   = "20G"
    ip     = "192.168.1.6"
  },
  {
    name   = "k8s-worker1"
    memory = 2048
    cores  = 2
    disk   = "20G"
    ip     = "192.168.1.7"
  },
  {
    name   = "k8s-worker2"
    memory = 2048
    cores  = 2
    disk   = "20G"
    ip     = "192.168.1.8"
  },
  {
    name   = "k8s-nfs"
    memory = 2048
    cores  = 2
    disk   = "30G"
    ip     = "192.168.1.9"
  }

]

