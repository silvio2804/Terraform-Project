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

  clone      = var.vm_template
  full_clone = true

  os_type = "cloud-init"

  memory = var.vm_definitions[count.index].memory

  cpu {
    sockets = 1
    cores   = var.vm_definitions[count.index].cores
  }

  disks {
    scsi {
      scsi0 {
        disk {
          storage = var.pm_storage
          size    = 100
        }
      }
    }
  }

  #ok
  network {
    id     = 0
    model  = "virtio"
    bridge = var.pm_bridge
    tag    = tostring(var.pm_vlan)
  }

  # Cloud-init networking
  #ipconfig0 = "ip=${var.vm_definitions[count.index].ip}/24,gw=${var.pm_gateway}"

  ipconfig0  = var.vm_definitions[coun.index].ip
  
  #cloudinit_cdrom_storage = "local"
  scsihw = "virtio-scsi-single"
  
  # Cloud-init user
  ciuser  = var.ci_user
  sshkeys = var.ci_ssh_key

  agent = 1

}





/*

resource "proxmox_vm_qemu" "vm" {
  name        = "myvm"
  target_node = "local"
 # onboot      = true
  vmid        = "801"

# Enter the name of your cloned cloud-init template we initially created
  clone = "alma-template"

  # Activate QEMU agent for this VM
  agent = 1


  os_type = "cloud-init"
  cores   = 1
  sockets = 1
  memory  = 1024
  numa    = false
  kvm = true
  protection = false
  vm_state = "running"
  define_connection_info = true


  #cloudinit_cdrom_storage = "local"
  scsihw = "virtio-scsi-single"

  disks {
    scsi {
      scsi0 {
        disk {
          storage = "local-lvm" #mine is local, yours to be local-lvm
          size    = 100
        }
      }
    }
  }

  network {
    id     = 0
    bridge   = "vmbr0"
    firewall = true      # You can turn firewall off, I will leave mine on
    model    = "virtio"
    #linkdown = false
    #tag       = 10
  }


  # Cloud Init Settings
  boot       = "order=scsi0;net0"
  ipconfig0  = "ip=192.168.1.80/24,gw=192.168.1.1" #add your ip addr and gw
  
  ciuser  = var.ci_user
  sshkeys = var.ci_ssh_key

}

*/









