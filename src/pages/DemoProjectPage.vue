<template>
  <q-page class="q-pa-md">
    <div class="content-container">
      <!-- Levý sloupec -->
      <div class="left-column">
        <h1 class="text-primary">Whisper API</h1>
        <p v-if="isLoading" class="text-grey-7">Proces probíhá. Prosím čekejte...</p>
        <textarea ref="txtData" v-model="jsonData" v-if="!isLoading"></textarea>
        <div class="buttons" v-if="!isLoading">
          <q-btn label="↓ Load" @click="LoadDataFromTextArea" color="primary" />
          <q-btn label="↑ Save" @click="saveData" color="secondary" />
        </div>
      </div>

      <!-- Pravý sloupec s videem -->
      <div class="right-column">
        <h2 class="text-primary">Media Player:</h2>
        <video
          ref="videoPlayer"
          controls
          v-if="!isLoading"
          width="100%"
          height="auto"
          :src="'http://localhost:8000/get_video/1733782294156_video_sample.mp4'"
          @timeupdate="onVideoTimeUpdate"
        >
          Váš prohlížeč nepodporuje přehrávání videa.
        </video>
      </div>
    </div>

    <!-- Další obsah stránky (vizualizace apod.) -->
    <div ref="visualization" style="height: 300px; position: relative; margin-top: 20px;">
      <div v-if="isLoading" class="overlay">
        <q-linear-progress
          v-if="isLoading"
          :value="progress / 100"
          color="primary"
          size="lg"
          class="q-mb-md"
        >
          {{ progress }} %
        </q-linear-progress>
      </div>
      <div v-if="!isLoading">
        <div ref="timeline" style="height: 100%;"></div>
      </div>
    </div>

    <q-card v-if="!isLoading && result" class="q-pa-md">
      <q-card-section>
        <h2 class="text-primary">Výsledek</h2>
        <p>{{ result }}</p>
      </q-card-section>
    </q-card>

    <q-banner v-if="error" class="q-mt-md" color="red" dense>
      {{ error }}
    </q-banner>
  </q-page>
</template>

<script>
import axios from 'axios'
import { DataSet } from 'vis-data'
import { Timeline } from 'vis-timeline/standalone'
import 'vis-timeline/styles/vis-timeline-graph2d.min.css'

export default {
  name: 'WhisperProcessingPage',
  data () {
    return {
      isLoading: true,
      progress: 0,
      result: null,
      error: null,
      jsonData: '',
      items: null,
      timeline: null,
      videoPlayer: null // Odkaz na video přehrávač
    }
  },
  mounted () {
    // Ujistíme se, že videoPlayer je definováno
    this.videoPlayer = this.$refs.videoPlayer;

    // Zkontrolujte, zda videoPlayer je inicializováno
    if (this.videoPlayer) {
      // Nastavení eventu pro načítání metadat videa
      this.videoPlayer.onloadedmetadata = () => {
        const duration = this.videoPlayer.duration * 1000; // Převedeno na milisekundy
        console.log("Délka videa (v milisekundách):", duration); // Přidání logu pro délku videa
        this.timeline.setOptions({
          min: 0,
          max: duration
        });
        this.timeline.fit();
      };

      // Nastavení posluchače pro aktualizaci času videa
      this.videoPlayer.ontimeupdate = this.onVideoTimeUpdate;
    } else {
      console.error("Video přehrávač nebyl nalezen!");
    }

    // Inicializace timeline
    this.items = new DataSet();
    const container = this.$refs.visualization;
    const options = {
      editable: true,
      timeAxis: { scale: 'second', step: 1 },
      format: {
        minorLabels: { minute: 'HH:mm:ss' },
        majorLabels: { minute: '' }
      },
      stack: true // Zajištění správného zarovnání bloků na ose
    };
    this.timeline = new Timeline(container, this.items, options);

    // Zavolání funkce pro načítání dat
    this.fetchWhisperData();
    },

  methods: {
    async fetchWhisperData () {
      try {
        this.isLoading = true
        this.progress = 0
        const interval = setInterval(() => {
          if (this.progress < 90) this.progress += 10
        }, 1000)
        const response = await axios.get('http://localhost:8000/api/whisper')
        clearInterval(interval)
        this.progress = 100
        this.result = response.data.message

        // Po načtení dat zavolejte metodu pro zpracování a přidání do timeline
        this.loadData()
      } catch (error) {
        console.error('Chyba při zpracování:', error)
        this.error = 'Došlo k chybě při zpracování'
      } finally {
        this.isLoading = false
      }
    },

    async loadData () {
      try {
        const response = await fetch('/data.json')
        if (!response.ok) throw new Error('Chyba při načítání souboru')
        const data = await response.json()

        console.log('Načítaná data:', data) // Zkontrolujte, zda data jsou správná

        // Vyčištění a přidání nových dat do timeline
        this.items.clear()
        this.items.add(data)

        // Dynamické nastavení rozsahu časové osy
        const startTimes = this.items.get().map(item => new Date(item.start).getTime())
        const endTimes = this.items.get().map(item => new Date(item.end || item.start).getTime())
        const minTime = Math.min(...startTimes)
        const maxTime = Math.max(...endTimes)

        // Aktualizace možností timeline
        this.timeline.setOptions({
          min: new Date(minTime),
          max: new Date(maxTime)
        })

        this.timeline.fit() // Přizpůsobení časové osy
        this.jsonData = JSON.stringify(data, null, 2) // Možnost zobrazení dat ve formátu JSON
      } catch (error) {
        console.error('Chyba při načítání dat:', error.message)
      }
    },
    
    async LoadDataFromTextArea () {
      const text = this.jsonData // Získání textu z textarea
      try {
        const response = await axios.post('http://localhost:8000/api/save_text_to_json', { text })
        console.log('Text byl úspěšně uložen:', response.data)
      } catch (error) {
        console.error('Chyba při ukládání textu:', error)
      }
      this.loadData()
    },

    async saveData () {
      // Get data from items and serialize to JSON
      const data = this.items.get({
        type: {
          start: 'ISODate',
          end: 'ISODate'
        }
      })
      // Ošetření položek bez 'end' a přiřazení 'start' k 'end' //tohle funguje jen z casti, je potreba tu pravit
      const modifiedData = data.map(item => {
        // Pokud 'end' neexistuje, nastavíme 'end' na 'start'
        if (!item.end) {
          const startDate = new Date(item.start)
          const endDate = new Date(startDate.getTime() + 4000) // Přidání 3 sekund
          item.end = endDate.toISOString()
        }
        return item
      })
      // Update textarea with serialized data
      this.jsonData = JSON.stringify(data, null, 2)
      this.LoadDataFromTextArea()
    },

    // Funkce pro synchronizaci videa s timeline
    onVideoTimeUpdate() {
      try {
        // Vaše logika pro ontimeupdate
        console.log(this.videoPlayer.currentTime);  // Testovací log
      } catch (error) {
        console.error("Chyba v onVideoTimeUpdate:", error);
      }
    },

    // Funkce pro synchronizaci timeline s videem
    onTimelineRangeChange (event) {
      const startTime = event.start.getTime(); // Získání počátečního času z timeline
      this.videoPlayer.currentTime = startTime / 1000; // Nastavení videa na čas z timeline (převedeno na sekundy)
    }
  }
}

</script>

<style scoped>
.content-container {
  display: flex;
  justify-content: space-between;
  align-items: stretch; /* Zarovnání sloupců na stejnou výšku */
  height: 100%; /* Zajištění, že kontejnery budou mít stejnou výšku */
}

.left-column {
  flex-grow: 1; /* Levý sloupec zabírá dostupný prostor */
  margin-right: 20px;
}

.right-column {
  width: 500px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end; /* Zarovnání videa na spodní část */
  margin-top: 20px;
  height: 100%; /* Pravý sloupec musí mít 100% výšky, aby byl ve stejné úrovni jako levý */
}

video {
  max-width: 100%;
  max-height: 600px; /* Maximální výška videa */
  object-fit: contain;
}

.q-page {
  background-color: #f9f9f9;
}

.q-linear-progress {
  margin: 20px auto;
  max-width: 500px;
}

.q-card {
  margin-top: 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

textarea {
  width: 100%;
  height: 450px;
  margin-bottom: 10px;
}
</style>
