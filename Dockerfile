FROM public.ecr.aws/lambda/python:3.9.2022.06.01.09

COPY function/app.py /var/task

COPY function/requirements.txt .

RUN pip3 install -r requirements.txt --target /var/task

CMD ["app.lambda_handler"]