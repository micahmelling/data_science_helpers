FROM python:3.7
MAINTAINER Micah Melling, micahmelling@gmail.com
RUN groupadd docker
RUN useradd --create-home appuser
RUN usermod -aG docker appuser
RUN newgrp docker
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN chown -R appuser:docker /app
ENV PATH="/home/appuser/.local/bin:${PATH}"
USER appuser
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN chmod a+rx run.sh
ENTRYPOINT ["./run.sh"]
