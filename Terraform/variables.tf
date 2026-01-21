variable "pm_api_url" {
  type = string
}

variable "pm_user" {
  type = string
}

variable "pm_tls_insecure" {
  description = "Whether to allow insecure TLS connections"
  type        = bool
  default     = false  # opzionale, se vuoi un valore di default
}

variable "pm_password" {
  type      = string
  sensitive = true
}

variable "pm_target_node" {
  type = string
}

variable "pm_storage" {
  type = string
}

variable "pm_bridge" {
  type = string
}

variable "pm_vlan" {
  type = number
}

variable "pm_gateway" {
  type = string
}

variable "vm_template" {
  type = string
  description = "Golden image cloud-init template"
}

variable "ci_user" {
  type = string
}

variable "ci_ssh_key" {
  type = string
}

variable "vm_definitions" {
  type = list(object({
    name   = string
    cores  = number
    memory = number
    disk   = string
    ip     = string
  }))
}
