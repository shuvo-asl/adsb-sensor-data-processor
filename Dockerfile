FROM python:3.10.6
LABEL authors="MD Mehedi Hasan"

# Create a directory named adsb_fdp
RUN mkdir "adsb_fdp"

# Copy everythinng to adsb_fdp folder
Copy . ./adsb_fdp/

# Make adsb_fdp as working directory
WORKDIR /adsb_fdp

# Install the Python libraries
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the entrypoing script

CMD ["bash","entrypoint.sh"]