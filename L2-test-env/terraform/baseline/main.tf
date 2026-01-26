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
  target_node = var.vm_definitions[count.index].target_node
  os_type     = "cloud-init"
  clone       = "almalinux-cloud"
  full_clone  = true

  memory = var.vm_definitions[count.index].memory

  cpu { 
    cores =var.vm_definitions[count.index].cores 
  }

  scsihw = "virtio-scsi-single"

  disks {
      # Disco principale qcow2
      scsi {
        scsi0 {
          disk {
            size    = "10G"
            storage = "local-lvm"
          }
        }
      }
      # Drive Cloud-Init
      ide {
        ide2 {
          cloudinit {
            storage = "local-lvm"
          }
        }
      }
    }

    # Rete
    network {
      id     = 0
      model  = "virtio"
      bridge = var.pm_bridge
      #tag    = tostring(var.pm_vlan)
    }

  serial {
      id   = 0
      type = "socket"
    }

    # Cloud-init
    ciuser   = var.ci_user
    cipassword = var.ci_password
    sshkeys  = var.ci_ssh_key
    ipconfig0 = "ip=${var.vm_definitions[count.index].ip}/24,gw=${var.pm_gateway}"

    agent = 1

    lifecycle {
      ignore_changes = [
        disks,
        boot,
      ]
    }

}


/*
resource "null_resource" "ansible_bootstrap" {
  depends_on = [proxmox_vm_qemu.vm]

  connection {
    type        = "ssh"
    user        = var.ci_user
    private_key = file("~/.ssh/id_ed25519")
    host        = [for vm in var.vm_definitions : vm.ip if vm.name == "ansible"][0]
    
    # TRUCCO 1: Evita /tmp che potrebbe avere permessi noexec o essere lockato
    script_path = "/home/${var.ci_user}/terraform_script.sh"
    
    # TRUCCO 2: Aumenta il timeout di connessione
    timeout     = "5m"
  }

  provisioner "remote-exec" {
    inline = [
      # TRUCCO 3: Aspetta che Cloud-Init abbia finito davvero
      "while [ ! -f /var/lib/cloud/instance/boot-finished ]; do echo 'Waiting for cloud-init...'; sleep 2; done",
      
      # Opzionale: pulizia se una run precedente è fallita
      "rm -rf ~/Ansible-repo",
      
      "git clone https://github.com/silvio2804/Ansible-repo.git ~/Ansible-repo"
    ]
  }
}




  # Trasferimento chiave privata 
  provisioner "file" {
    source      = "./id_ed25519" #chiave di ansible
    destination = "/home/${var.ci_user}/"
  }

  provisioner "file" {
    source      = "./id_ed25519"
    destination = "/home/${var.ci_user}/.ssh/id_ed25519"

  # Forza l'uso di SCP invece di SFTP
  connection {
    type     = "ssh"
    user     = var.ci_user
    host     = "192.168.1.5" # o l'IP del nodo
    use_sftp = false
    }
}*/











