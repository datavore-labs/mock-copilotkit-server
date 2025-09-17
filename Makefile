# Project configuration
PROJECT_ID := audience-builder-tintash
SERVICE_NAME := copilotkit-server
REGION := us-central1
IMAGE_TAG := latest

# Docker image names
LOCAL_IMAGE := $(SERVICE_NAME):$(IMAGE_TAG)
GCR_IMAGE := gcr.io/$(PROJECT_ID)/$(SERVICE_NAME):$(IMAGE_TAG)

# Set default project
.PHONY: setup
setup:
	@echo "Setting up project configuration..."
	gcloud config set project $(PROJECT_ID)
	gcloud auth configure-docker
	@echo "Setup complete!"

# Build Docker image locally
.PHONY: build
build:
	@echo "Building Docker image locally..."
	docker buildx build --platform linux/amd64 --cache-from $(GCR_IMAGE) --load -t $(LOCAL_IMAGE) .
	docker tag $(LOCAL_IMAGE) $(GCR_IMAGE)
	@echo "Build complete: $(GCR_IMAGE)"

# Push image to GCR
.PHONY: push
push:
	@echo "Pushing image to GCR..."
	docker push $(GCR_IMAGE)
	@echo "Push complete: $(GCR_IMAGE)"

# Deploy using Cloud Build
.PHONY: deploy
deploy:
	@echo "Deploying using Cloud Build..."
	gcloud builds submit --config cloudbuild.yaml --project=$(PROJECT_ID)
	@echo "Deployment complete!"


# Clean up local Docker images
.PHONY: clean
clean:
	@echo "Cleaning up local Docker images..."
	-docker rmi $(LOCAL_IMAGE) $(GCR_IMAGE)
	@echo "Cleanup complete!"

# Local development commands
.PHONY: run
run: clean build
	docker run -d \
		--name $(SERVICE_NAME)-local \
		-p 8080:8080 \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		$(LOCAL_IMAGE)
	@echo "Container running at http://localhost:8080"


live-tests:
	uv run behave tests/live-tests/features/

live-tests-verbose:
	uv run behave tests/live-tests/features/ -v

live-tests-docker: clean build
	@echo "Removing existing test container if it exists..."
	-docker stop $(SERVICE_NAME)-test 2>/dev/null || true
	-docker rm $(SERVICE_NAME)-test 2>/dev/null || true
	docker run -d --name $(SERVICE_NAME)-test -p 8000:8000 $(LOCAL_IMAGE)
	@echo "Waiting for container to start..."
	@sleep 5
	COPILOTKIT_SERVER_URL=http://localhost:8000 uv run behave tests/live-tests/features/
	docker stop $(SERVICE_NAME)-test
	docker rm $(SERVICE_NAME)-test


unit-tests:
	uv run pytest tests/unit-tests

precommit:
	uv run pre-commit run --all-files

dev-server:
	cd src/mock_copilotkit_server && ENV="dev" uv run python -m server
