pm_api_url      = "https://192.168.1.135:8006/api2/json"
pm_user         = "terraform@pve"
pm_password     = "password"
pm_target_node  = "local"
pm_storage      = "local-lvm"
pm_bridge       = "vmbr0"
pm_vlan         = 100
pm_gateway      = "192.168.1.1"

vm_template = "origin"

ci_user    = "silvio"
ci_ssh_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAaL6ZpiCzkbjN2feimCco5TeaGEQs4UEXVC0WWX/1rH silviove@silviove"

vm_definitions = [
  {
    name   = "test-vm-1"
    cores  = 2
    memory = 2048
    disk   = "20G"
    ip     = "192.168.100.50"
  }
]

