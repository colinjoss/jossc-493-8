FROM python:3.9
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS='./jossc-8-c1a075c74e50.json'
EXPOSE ${PORT}
CMD [ "python", "main.py" ]
