<template>
  <q-page class="q-pa-md">
    <div class="text-center q-mb-lg">
      <h1 class="text-primary">Nahrát soubor</h1>
      <p class="text-grey-7">Vyberte soubor pro nahrání na server.</p>
    </div>
    <q-card class="q-pa-md" bordered>
      <q-card-section>
        <q-file
          v-model="file"
          label="Vyberte soubor"
          filled
          accept="image/*,video/*,.mp3,.mp4"
          class="q-mb-md"
        />
      </q-card-section>
    </q-card>
    <q-btn
      @click="uploadFile"
      label="Nahrát soubor"
      color="primary"
      class="full-width"
      size="lg"
    />
    <q-banner v-if="uploadStatus" class="q-mt-md" :color="uploadStatusColor" dense>
      {{ uploadStatus }}
    </q-banner>
  </q-page>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FileUploadPage',
  data () {
    return {
      file: null,
      uploadStatus: '',
      uploadStatusColor: ''
    }
  },
  methods: {
    uploadFile () {
      if (!this.file) {
        this.$q.notify({
          color: 'negative',
          message: 'Nejprve vyberte soubor!',
          icon: 'warning'
        })
        return
      }
      const formData = new FormData()
      const timestamp = Date.now()
      const uniqueFileName = `${timestamp}_${this.file.name}`
      formData.append('file', this.file, uniqueFileName)
      axios
        .post('http://localhost:8000/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then(() => {
          this.uploadStatus = 'Soubor byl úspěšně nahrán!'
          this.uploadStatusColor = 'green'
          this.$q.notify({
            color: 'positive',
            message: 'Soubor byl úspěšně nahrán!',
            icon: 'check_circle'
          })
          this.$router.push('/try/demo_project') // Přesměrování
        })
        .catch(() => {
          this.uploadStatus = 'Došlo k chybě při nahrávání souboru.'
          this.uploadStatusColor = 'red'
          this.$q.notify({
            color: 'negative',
            message: 'Došlo k chybě při nahrávání souboru.',
            icon: 'error'
          })
        })
    }
  }
}
</script>

<style scoped>
.q-page {
  background-color: #f9f9f9
}
.q-card {
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)
}
.q-btn {
  min-width: 200px;
  margin-top: 16px
}
</style>
