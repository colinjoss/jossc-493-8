FROM python:3.9
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENV PORT=8080
EXPOSE ${PORT}
CMD [ "python", "main.py" ]
