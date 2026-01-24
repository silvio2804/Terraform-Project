ansible -i /playbooks/hosts all -m ping
ansible-playbook -i /playbooks/hosts install-kube.yml
ansible-playbook -i /playbooks/hosts master-setup.yml
ansible-playbook -i /playbooks/hosts worker-setup.yml
ansible-playbook -i /playbooks/hosts main.yml