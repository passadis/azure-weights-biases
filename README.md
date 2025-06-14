<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=azure,vue,cs,python,github" />
  </a>
</p>

<h1 align="center">Boost your AI RAG Apps with Feedback and analysis from W&B</h1>

## Introduction

Track user satisfaction in your AI chatbot using a lightweight thumbs up/down feedback system integrated with Weights & Biases. This repo shows how to capture, log,and analyze user feedback to inform continuous model improvement.



## Technologies Used

- **Frontend**: Vue modern UI with thumbs up, thumbs down components for user Feedback
- **Backend**: Python with FAST Api
- **Jupyter Notebooks**: Sample scrapper for blog, AI Search deployment, content upload and embeddings generation
- **AI Features**: Azure OpenAI for text generation and embeddings (gpt-4o and text-embeddings)
- **Vector Search**: Vector and Semantic search functionality using Azure AI Search
- **Weights and Biases**: Trial Cloud Account on Weights and Biases Platform


## Features

- 👍👎 Inline thumbs feedback for chat responses
- Logs feedback and interaction metadata to Weights & Biases
- Custom W&B dashboard for insights
- Built with FastAPI + Azure AI Studio
- Lightweight frontend in Vite/Vue

## Setup and Deployment

- **Clone the repo**
- **Create Weights and Biases Trial account**
- **Deploy gpt-4o and text-embeddings-ada-002**
- **Install dependencies**

```
npm install
```

- **Configure environment**

```env

AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=
AZURE_SEARCH_INDEX=

AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AZURE_OPENAI_DEPLOYMENT=

AZURE_OPENAI_EMBEDDING_DEPLOYMENT=
```
- **Get the Data or use the sample Notebook**
  
***extractblog.py***

- **Create Azure AI Search with Notebooks and upload content and embeddings**

 ***create_azure_ai_index.ipynb***
 
 ***embed_and_upload_blog_docs.ipynb***

- **Run Local Dev**

 ```
uvicorn app.main:app --reload - Python backend
npm run dev - Vue frontend
 ``` 

## Sample Dashboard

![wnball](https://github.com/user-attachments/assets/cf393ba2-87b4-4726-ba12-be511d92ebb0)



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
