# In-Store Inventory Management Object Detection

## 1. Install

You can use `Docker` to install all the needed packages and libraries easily. Two Dockerfiles are provided for both CPU and GPU support.

- **CPU:**

```bash
$ docker build -t ins_inv_mng_obj_detect_jc --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile .
```

- **GPU:**

```bash
$ docker build -t ins_inv_mng_obj_detect_gpu_jc --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f docker/Dockerfile .
```

### Run Docker

- **CPU:**

```bash
$ docker run --rm --net host -it -v "$(pwd)":/home/app/src --workdir /home/app/src ins_inv_mng_obj_detect_jc bash
```

- **GPU:**

```bash
$ docker run --rm --net host --gpus all -it -v "$(pwd)":/home/app/src --workdir /home/app/src ins_inv_mng_obj_detect_gpu_jc bash
```

