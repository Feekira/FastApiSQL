FROM python
WORKDIR /FastApiSQL
COPY ./requeriments.txt .
RUN pip install -r ./requeriments.txt
COPY . .
EXPOSE 8000