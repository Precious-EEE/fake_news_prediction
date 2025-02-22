

# Fake News Prediction 🚀  

This project focuses on detecting fake news using machine learning techniques. The model was trained on a labeled dataset of real and fake news articles and deployed using **Docker** for scalability and ease of deployment.  

## Features  
✅ Preprocesses news articles using NLP techniques.  
✅ Trains a machine learning model to classify news as real or fake.  
✅ Deploys the model in a **Docker container** for seamless execution.  
✅ Provides an API endpoint for real-time predictions.  

## Deployment with Docker  
To build and run the Docker container:  
```sh
docker build -t fake-news-predictor .
docker run -p 5000:5000 fake-news-predictor
```

The API will be available at `http://localhost:5000/predict`, allowing users to submit news articles for classification.  
