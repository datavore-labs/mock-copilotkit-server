

unit-tests:
	uv run pytest tests/unit-tests

precommit:
	uv run pre-commit run --all-files

dev-server:
	cd src/mock_copilotkit_server && ENV="dev" uv run python -m server

docker-build:
	docker build -t mock-copilotkit-server .
