<template>
  <q-page>
    <h1>Nahrát soubor</h1>
    <q-file
      v-model="file"
      label="Vyberte soubor"
      filled
      accept="image/*,video/*,.mp3,.mp4"
    />
    <q-btn
      @click="uploadFile"
      label="Nahrát soubor"
      color="primary"
      class="q-mt-md"
    />
  </q-page>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FileUploadPage',
  data () {
    return {
      file: null
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
          this.$q.notify({
            color: 'positive',
            message: 'Soubor byl úspěšně nahrán!',
            icon: 'check_circle'
          })
        })
        .catch(() => {
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
