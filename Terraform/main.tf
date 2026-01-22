terraform {
  required_providers {
    proxmox = {
      source  = "Telmate/proxmox"
      version = "3.0.2-rc07"
    }
  }
}

provider "proxmox" {
  pm_api_url      = var.pm_api_url
  pm_user         = var.pm_user
  pm_password     = var.pm_user
  pm_tls_insecure = var.pm_tls_insecure
}


resource "proxmox_vm_qemu" "vm" {
  count = length(var.vm_definitions)

  name        = var.vm_definitions[count.index].name
  target_node = var.pm_target_node
  os_type     = "cloud-init"

  memory = var.vm_definitions[count.index].memory
  cores  = var.vm_definitions[count.index].cores
  scsihw = "virtio-scsi-pci"

  # Disco da zero
  disk {
    slot    = 0
    size    = var.vm_definitions[count.index].disk
    type    = "scsi"
    storage = var.pm_storage
    iothread = true
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
  sshkeys  = var.ci_ssh_key
  ipconfig0 = "ip=${var.vm_definitions[count.index].ip}/24,gw=${var.pm_gateway}"

  agent = 1
}








