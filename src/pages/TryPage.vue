<template>
  <div class="q-pa-md text-center">
    <h1>Try Whisper</h1>
    <p class="text-subtitle2 q-mt-sm">
      Experience the power of real-time audio transcription.
    </p>
    <q-btn
      label="Get Started"
      color="primary"
      class="q-mt-md"
      size="lg"
      @click="handleGetStarted"
    />
    <q-btn
      label="Learn More"
      flat
      color="secondary"
      class="q-mt-sm"
      @click="handleLearnMore"
    />
  </div>
</template>

<script>
export default {
  name: 'TryWhisper',
  methods: {
    handleGetStarted () {
      // Přesměruje na stránku s detailním průvodcem
      this.$router.push('/try/get_started')
    },
    handleLearnMore () {
      // Přesměruje na stránku s více informacemi
      this.$router.push('/learn-more')
    }
  }
}
</script>

<style scoped>
.q-pa-md {
  margin-top: 10%;
}
h1 {
  font-size: 2.5rem;
  color: #3f51b5; /* Modrá barva pro nadpis */
}
.text-subtitle2 {
  font-size: 1.2rem;
  color: #757575; /* Jemnější šedá barva pro podnadpis */
}
</style>
