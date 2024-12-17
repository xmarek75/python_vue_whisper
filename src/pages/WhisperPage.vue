<script>
import axios from 'axios'

export default {
  name: 'IndexPage',
  data () {
    return {
      message: ''
    }
  },
  mounted () {
    // Volání API na FastAPI serveru
    axios.get('http://127.0.0.1:8000/api/data')
      .then(response => {
        this.message = response.data.message
      })
      .catch(error => {
        console.error('Error fetching data:', error)
      })
  },
  methods: {
    async handleClick () {
      // Zobrazíme snackbar s informací o čekání
      this.$q.notify({
        message: 'Please wait, Whisper is processing...', // Zpráva zobrazená v Snackbaru
        color: 'positive', // Barva (např. zelená pro pozitivní)
        position: 'top' // Umístění zprávy na obrazovce
      })

      try {
        // Zavoláme UseWhisper a počkáme na výsledek
        const result = await this.UseWhisper()
        this.message = result // Nastavíme výsledek operace do zprávy
        // Zobrazíme snackbar s výsledkem operace
        // this.$q.notify({
        //   message: 'Completed: ' + result, // Výsledek zobrazený v notifikaci
        //   color: 'green', // Barva (zelená pro úspěch)
        //   position: 'top' // Umístění zprávy
        // })
      } catch (error) {
        console.error('Error:', error)
        // Pokud dojde k chybě při volání UseWhisper
        this.$q.notify({
          message: 'Error occurred during Whisper operation!', // Chybová zpráva
          color: 'negative', // Červená barva pro chyby
          position: 'top'
        })
      }
    },

    async UseWhisper () {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/whisper')
        console.log('API response:', response)
        return response.data.message || 'No message in response' // Vrací výsledek volání
      } catch (error) {
        console.error('Error fetching message:', error)
        throw new Error('Failed to fetch message') // Vyvolá chybu pro správné zachycení v `handleClick`
      }
    }
  }
}
</script>

<template>
  <div style="width: 50%; margin: 0 auto;">
    <!-- <h5>{{ message }}</h5> -->
    <!-- <h7 v-html="message"></h7> -->
    <h7>{{message}}</h7>
    <button @click="handleClick">click here</button>
    <br>
  </div>
</template>
