terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "3.0.2-rc07"
    }
  }
}

provider "proxmox" {
  pm_api_url      = "https://192.168.1.135:8006/api2/json"
  pm_user         = "terraform@pve"
  pm_password     = "password"
  pm_tls_insecure = true
}


resource "proxmox_vm_qemu" "vm" {
  count = length(var.vm_definitions)

  name        = var.vm_definitions[count.index].name
  target_node = var.pm_target_node
  os_type     = "cloud-init"

  memory = var.vm_definitions[count.index].memory

  cpu { 
    cores =var.vm_definitions[count.index].cores 
  }

  scsihw = "virtio-scsi-single"

  # Disco da zero
  disk {
    size    = var.vm_definitions[count.index].disk
    #type    = "scsi"
    storage = var.pm_storage
    iothread = true
    disk_file  = "local-lvm:vm-100-disk-0"
    passthrough = true
    slot    = "scsi0"
  }

  # Rete
  network {
    id     = 0
    model  = "virtio"
    bridge = var.pm_bridge
    tag    = tostring(var.pm_vlan)
  }

  # Cloud-init
  ciuser   = var.ci_user
  cipassword = var.ci_password
  sshkeys  = var.ci_ssh_key
  ipconfig0 = "ip=${var.vm_definitions[count.index].ip}/24,gw=${var.pm_gateway}"

  agent = 1
}








