terraform {
  required_providers {
    proxmox = {
      source = "Telmate/proxmox"
      version = "3.0.2-rc07"
    }
  }
}

provider "proxmox" {
  pm_api_url      = var.pm_api_url
  pm_user         = var.pm_user
  pm_password     = var.pm_password
  pm_tls_insecure = true
}

resource "proxmox_vm_qemu" "vm" {
  count = length(var.vm_definitions)

  name        = var.vm_definitions[count.index].name
  target_node = var.pm_target_node
  clone       = var.vm_template
  os_type     = "cloud-init"

  memory  = var.vm_definitions[count.index].memory

  scsihw = "virtio-scsi-pci"
  boot   = "order=scsi0"

  disk {
    slot     = "scsi0"
    size     = var.vm_definitions[count.index].disk
    type     = "disk"
    storage  = var.pm_storage
    iothread = true
  }

  cpu {
    sockets = 1
    cores   = var.vm_definitions[count.index].cores
  }

  network {
    id     = 0
    model  = "virtio"
    bridge = var.pm_bridge
    tag    = tostring(var.pm_vlan)
  }

  ipconfig0 = "ip=${var.vm_definitions[count.index].ip}/24,gw=${var.pm_gateway}"

  ciuser  = var.ci_user
  sshkeys = var.ci_ssh_key

  agent = 1
}
