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
	docker build -t $(LOCAL_IMAGE) .
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


unit-tests:
	uv run pytest tests/unit-tests

precommit:
	uv run pre-commit run --all-files

dev-server:
	cd src/mock_copilotkit_server && ENV="dev" uv run python -m server
