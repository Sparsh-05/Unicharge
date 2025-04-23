import pymongo #to connect MongoDB to Django Project

url = "mongodb+srv://sparshkap:sparshiven32@unicharge.mlty3.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(
    url,
    tls=True,  # Ensure TLS is enabled
    tlsAllowInvalidCertificates=True  
)

db = client["chargers"]
print("Connected successfully!")
