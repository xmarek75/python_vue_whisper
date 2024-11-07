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
        // timeout: 0 // Délka zobrazení, 0 znamená, že se neukáže automaticky (ručně ho skryjeme)
      })

      try {
        // Zavoláme funkci UseWhisper, která provádí nějakou operaci
        const result = await this.UseWhisper()
        this.message = result // Získáme výsledek operace
        // Zobrazíme snackbar s výsledkem operace
        // this.$q.notify({
        //   message: 'Completed',//this.message, // Zpráva, která se zobrazí, když je operace hotová
        //   color: 'green', // Barva (zelená pro úspěch)
        //   position: 'top', // Umístění zprávy
        //   timeout: 0
        // })
      } catch (error) {
        console.error('Error:', error)
        // Pokud dojde k chybě při volání UseWhisper
        this.$q.notify({
          message: 'Error occurred during Whisper operation!', // Chybová zpráva
          color: 'negative', // Červená barva pro chyby
          position: 'top' // Umístění zprávy
        })
      }
    },
    UseWhisper () {
      axios.get('http://127.0.0.1:8000/api/whisper')
        .then(response => {
          console.log('API response:', response)
          this.message = response.data.message || 'No message in response'
        })
        .catch(error => {
          console.error('Error fetching message:', error)
          this.message = 'Failed to fetch message'
        })
    }
    // handleClick() {
    //   this.UseWhisper();  // Zavolání funkce při kliknutí na tlačítko
    // }
  }
}
</script>

<template>
  <div style="width: 50%; margin: 0 auto;">
    <h5>{{ message }}</h5>
    <button @click="handleClick">click here</button>
  </div>
</template>
