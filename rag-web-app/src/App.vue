<!-- <template>
  <div class="container">
    <div class="content">
      <img src="/logo.png" alt="App Logo" class="logo">
      <h1>RAG Web App + W&B Demo</h1>
      
      <div class="search-container">
        <input
          type="text"
          v-model="query"
          placeholder="Ask something..."
          :disabled="loading"
        />
        <button @click="handleSearch" :disabled="loading">
          {{ loading ? 'Loading...' : 'Search' }}
        </button>
      </div>

      <div v-if="result" class="result-card">
        <div class="answer-section">
          <h2>Answer</h2>
          <p>{{ result.answer }}</p>
        </div>

        <div class="sources-section">
          <h2>Sources</h2>
          <ul>
            <li v-for="(src, index) in result.sources" :key="index">
              {{ src }}
            </li>
          </ul>
        </div>

        <div class="feedback-section">
          <button @click="sendFeedback(true)">👍</button>
          <button @click="sendFeedback(false)">👎</button>
          <span v-if="feedback">Thanks for your feedback!</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const query = ref('');
const loading = ref(false);
const result = ref(null);
const feedback = ref(null);

const handleSearch = async () => {
  loading.value = true;
  result.value = null;
  feedback.value = null;
  
  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value }),
    });
    result.value = await response.json();
  } catch (error) {
    console.error('Error fetching result:', error);
  }
  loading.value = false;
};

const sendFeedback = async (isPositive) => {
  feedback.value = isPositive ? 'positive' : 'negative';
  await fetch('/api/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: query.value,
      feedback: isPositive ? '👍' : '👎'
    }),
  });
};
</script> -->


<template>
  <div class="container">
    <div class="content">
      <img src="/logo.png" alt="App Logo" class="logo">
      <h1>RAG Web App + W&B Demo</h1>
      
      <div class="search-container">
        <input
          type="text"
          v-model="query"
          placeholder="Ask something..."
          @keyup.enter="handleSearch"
          :disabled="loading"
        />
        <button @click="handleSearch" :disabled="loading">
          {{ loading ? 'Loading...' : 'Search' }}
        </button>
      </div>

      <div v-if="loading" class="loading-indicator">
        <p>Loading your answer...</p>
        </div>

      <div v-if="result" class="result-card">
        <div class="answer-section">
          <h2>Answer</h2>
          <div v-html="renderedAnswer" class="markdown-content"></div>
        </div>

        <div class="sources-section" v-if="result.sources && result.sources.length">
          <h2>Sources</h2>
          <ul>
            <li v-for="(src, index) in result.sources" :key="index">
              <strong>Source {{ index + 1 }}:</strong> 
              {{ src.title ? src.title + ' - ' : '' }}
              <span class="source-content">{{ truncateText(src.content, 150) }}</span>
              <details>
                <summary>Read More</summary>
                <p>{{ src.content }}</p>
              </details>
            </li>
          </ul>
        </div>

        <div class="feedback-section">
          <button @click="sendFeedback(true)" :disabled="feedbackSent">👍</button>
          <button @click="sendFeedback(false)" :disabled="feedbackSent">👎</button>
          <span v-if="feedbackSent">Thanks for your feedback!</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import MarkdownIt from 'markdown-it'; // Import the Markdown renderer

const md = new MarkdownIt(); // Initialize MarkdownIt

const query = ref('');
const loading = ref(false);
const result = ref(null);
const feedbackSent = ref(false); // Renamed for clarity

// Computed property to render Markdown
const renderedAnswer = computed(() => {
  return result.value ? md.render(result.value.answer) : '';
});

const handleSearch = async () => {
  loading.value = true;
  result.value = null;
  feedbackSent.value = false; // Reset feedback status for new search
  
  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value }),
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    result.value = await response.json();
  } catch (error) {
    console.error('Error fetching result:', error);
    // Optionally, display an error message to the user
    result.value = { answer: "I apologize, but there was an error processing your request. Please try again.", sources: [] };
  } finally {
    loading.value = false;
  }
};

const sendFeedback = async (isPositive) => {
  feedbackSent.value = true; // Indicate feedback has been sent
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query.value,
        feedback: isPositive ? '👍' : '👎'
      }),
    });
  } catch (error) {
    console.error('Error sending feedback:', error);
    feedbackSent.value = false; // Allow retrying if feedback failed
  }
};

// Helper function to truncate text for source previews
const truncateText = (text, maxLength) => {
  // Add a check to ensure text is a string before accessing its length
  if (typeof text !== 'string') {
    return ''; // Or return 'No content available' or handle as appropriate
  }
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + '...';
};
</script>



<style scoped>
.container {
  min-height: 100vh;
  padding: 2rem;
  background-color: #f3f4f6;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  max-width: 800px;
  width: 100%;
  text-align: center;
}

.logo {
  max-width: 150px;
  margin-bottom: 1rem;
}

.search-container {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.result-card {
  background-color: white;
  padding: 1.5rem;
  margin-top: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: left;
}

.feedback-section {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  align-items: center;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

h2 {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

ul {
  padding-left: 1.5rem;
}
.markdown-content {
  font-size: 1.1em;
  line-height: 1.6;
  color: #333;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: bold;
}

.markdown-content p {
  margin-bottom: 1em;
}

.markdown-content ul,
.markdown-content ol {
  margin-left: 1.5em;
  margin-bottom: 1em;
  list-style-position: outside; /* Ensure bullets/numbers are outside */
}

.markdown-content li {
  margin-bottom: 0.5em;
}

.markdown-content strong {
  font-weight: bold;
  color: #0056b3; /* A bit more prominent color for bold text */
}

.sources-section ul {
  list-style: none; /* Remove default bullet points for sources */
  padding-left: 0;
}

.sources-section li {
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 5px;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  font-size: 0.95em;
  color: #555;
}

.sources-section li strong {
    color: #4CAF50; /* Highlight source number/title */
}

.source-content {
    display: block; /* Ensures truncate text is on its own line */
    margin-top: 0.25rem;
    color: #777;
}

details {
    margin-top: 0.5rem;
    cursor: pointer;
}

summary {
    font-weight: 500;
    color: #007bff;
    text-decoration: underline;
}

summary:hover {
    color: #0056b3;
}

/* Added loading indicator */
.loading-indicator {
    margin-top: 1rem;
    color: #666;
    font-style: italic;
}
</style>