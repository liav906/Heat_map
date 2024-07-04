import requests

url = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"
response = requests.get(url)
with open("mnist.npz", "wb") as f:
    f.write(response.content)

# Now, load the dataset from the local file
