<template>
  <q-page padding>
    <h1>Serialization and Deserialization</h1>
    <p>
      This example shows how to serialize and deserialize JSON data, and load this
      into the Timeline via a DataSet. Serialization and deserialization is needed
      when loading or saving data from a server.
    </p>
    <textarea ref="txtData" v-model="jsonData"></textarea>
    <div class="buttons">
      <q-btn label="↓ Load" @click="LoadDataFromTextArea" color="primary" />
      <q-btn label="↑ Save" @click="saveData" color="secondary" />
    </div>
    <div ref="visualization" style="height: 300px;"></div>
  </q-page>
</template>

<script>
import { DataSet } from 'vis-data'
import { Timeline } from 'vis-timeline/standalone'
import 'vis-timeline/styles/vis-timeline-graph2d.min.css'
import axios from 'axios'

export default {
  name: 'VisTimeline',
  data () {
    return {
      jsonData: '',
      items: null,
      timeline: null
    }
  },
  mounted () {
    this.items = new DataSet()
    const container = this.$refs.visualization
    const options = {
      editable: true,
      timeAxis: { scale: 'second', step: 1 },
      format: {
        minorLabels: { minute: 'HH:mm:ss' },
        majorLabels: { minute: 'HH:mm' }
      }
    }
    this.timeline = new Timeline(container, this.items, options)
    this.loadData()
  },
  methods: {
    async loadData () {
      try {
        const response = await fetch('/data.json')
        if (!response.ok) throw new Error('Chyba při načítání souboru')
        const data = await response.json()

        // Vyčištění a přidání nových dat
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

        this.timeline.fit() // Přizpůsobení obsahu
        this.jsonData = JSON.stringify(data, null, 2)
      } catch (error) {
        console.error('Chyba při načítání dat:', error.message)
      }
    },
    // load data from textarea to data.json then call loadData to refresh timeline
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
    }
  }

}
</script>

<style scoped>
textarea {
  width: 30%;
  height: 450px;
  margin-bottom: 10px;
}
</style>
