import pymongo

url = "mongodb+srv://sparshkap:sparshiven32@unicharge.mlty3.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(
    url,
    tls=True,  # Ensure TLS is enabled
    tlsAllowInvalidCertificates=True  # Try this if you're facing certificate issues
)

db = client["chargers"]
print("Connected successfully!")
