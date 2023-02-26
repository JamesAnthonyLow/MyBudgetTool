#!/bin/bash
SOURCE_DIR="$(dirname "$0")"/..
IMAGE_NAME=budget_tool_image

run_command(){
    docker build "$SOURCE_DIR" -t "$IMAGE_NAME"
    docker run --rm -v "$SOURCE_DIR":/workspace "$IMAGE_NAME" bash -c "$@"
}

run_it_command(){
    docker build "$SOURCE_DIR" -t "$IMAGE_NAME"
    docker run --rm -it -v "$SOURCE_DIR":/workspace "$IMAGE_NAME" "$@"
}