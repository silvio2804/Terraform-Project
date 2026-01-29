ansible -i hosts all -m ping
ansible-playbook -i hosts install-kube.yml -K
ansible-playbook -i hosts master-setup.yml
ansible-playbook -i hosts join-worker.yml
ansible-playbook -i hosts main.yml