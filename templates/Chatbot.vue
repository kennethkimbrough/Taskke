<template>
  <!-- ... -->
  <div>
    <input v-model="input" @keyup.enter="sendMessage" />
    <button @click="sendMessage">Send</button>
  </div>
  <!-- ... -->
</template>

<script>
export default {
  data() {
    return {
      input: '',
    };
  },
  methods: {
    async sendMessage() {
      const response = await fetch('http://localhost:3001/process_input', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: this.input }),
      });

      const responseData = await response.json();
      console.log(responseData.response);
      // Update the chatbot UI with the response
    },
  },
};
</script>
