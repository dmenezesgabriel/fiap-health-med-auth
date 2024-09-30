terraform-%:
	@echo "========================"
	@echo "Run terraform $*"
	@echo "========================"
	@if [ "$*" = "apply" ] || [ "$*" = "destroy" ]; then \
		docker compose run --rm terraform $* \
		--auto-approve \
		-var-file=inventories/$(ENV)/terraform.tfvars; \
	else \
		docker compose run --rm terraform $*; \
	fi

app:
	@docker compose up app

run: terraform-init terraform-validate terraform-apply app
	@echo "========================"
	@echo "Run application"
	@echo "========================"

unit-tests:
	@echo "========================"
	@echo "Run unit tests"
	@echo "========================"
	docker compose -f docker-compose-test.yaml run --rm tests \
	/bin/bash -c \
	"python -m pytest tests/unit \
	-s \
	-x \
	-vv \
	--color=yes \
	--cov=/app/src \
	--cov-report=html:/app/reports/coverage \
	--cov-report=xml:/app/reports/coverage/coverage.xml \
	--cov-report=term-missing \
	--alluredir /app/allure-results"

allure:
	@echo "========================"
	@echo "Run Allure dashboard"
	@echo "========================"
	@docker compose -f docker-compose-test.yaml up -d allure

sonar-scan:
	@echo "========================"
	@echo "Run Sonar scan"
	@echo "========================"
	@docker compose -f docker-compose-sonnar.yaml run --rm sonar-scanner

clean:
	@echo "========================"
	@echo "Clean python cache files"
	@echo "========================"
	@sh scripts/clean.sh