from google.cloud import aiplatform

# Initialize the Vertex AI client
aiplatform.init(project='243527177818', location='us-central1')

# List available models
models = aiplatform.Model.list()
for model in models:
    print(model.display_name)
