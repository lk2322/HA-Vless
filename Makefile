.PHONY: install deploy update setup-dev check lint update-clients show-urls

# Install required roles and collections
install:
	ansible-galaxy install -r requirements.yml

# Deploy the full setup
deploy:
	ansible-playbook -i inventory.yml site.yml

# Update only the Xray configuration
update-clients:
	ansible-playbook -i inventory.yml update-xray-config.yml

# Show connection URLs for all clients
show-urls:
	ansible-playbook -i inventory.yml show-client-urls.yml

# Setup development environment
setup-dev:
	cp -n inventory.example.yml inventory.yml || true
	cp -n group_vars/all.example.yml group_vars/all.yml || true
	@echo "Development environment setup complete. Edit inventory.yml and group_vars/all.yml with your settings."

# Check playbook syntax
check:
	ansible-playbook -i inventory.yml site.yml --syntax-check

# Check ansible-lint (if installed)
lint:
	@if command -v ansible-lint > /dev/null; then \
		ansible-lint .; \
	else \
		echo "ansible-lint is not installed. Install with: pip install ansible-lint"; \
	fi

# Help 
help:
	@echo "Available commands:"
	@echo "  make install         - Install required Ansible roles and collections"
	@echo "  make setup-dev       - Setup development environment by copying example files"
	@echo "  make deploy          - Deploy the full setup"
	@echo "  make update-clients  - Update only Xray client configurations"
	@echo "  make show-urls       - Generate and display client connection URLs"
	@echo "  make check           - Check playbook syntax"
	@echo "  make lint            - Run ansible-lint if installed"