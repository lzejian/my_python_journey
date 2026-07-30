FROM public.ecr.aws/lambda/python:3.12

# 告诉 Numba 使用 AWS Lambda 的可写临时目录
ENV NUMBA_CACHE_DIR=/tmp

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
CMD [ "lambda_function.lambda_handler" ]