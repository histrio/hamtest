build:
	docker build -t histrio/hamtest:latest .
run:
	docker run -it --rm histrio/hamtest:latest
run-dev:
	docker run -it --rm -v ${PWD}/main.py:/app/main.py -v ${PWD}/output:/output histrio/hamtest:latest
