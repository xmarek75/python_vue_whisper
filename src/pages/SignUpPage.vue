<template>
  <div class="q-pa-md" style="max-width: 400px; margin: 0 auto;">
    <q-card>
      <q-card-section>
        <div class="text-h6">Sign Up</div>
        <div class="text-subtitle2">Create an account to get started</div>
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="name"
          label="Full Name"
          outlined
          dense
          class="q-mb-md"
        />
        <q-input
          v-model="email"
          label="Email"
          outlined
          dense
          class="q-mb-md"
          type="email"
        />
        <q-input
          v-model="password"
          label="Password"
          outlined
          dense
          type="password"
          class="q-mb-md"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn color="primary" label="Sign Up" @click="handleSignUp" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'SignUpPage',
  data () {
    return {
      name: '',
      email: '',
      password: ''
    }
  },
  methods: {
    handleSignUp () {
      if (!this.name || !this.email || !this.password) {
        this.$q.notify({
          message: 'All fields are required',
          color: 'negative',
          position: 'top'
        })
        return
      }

      // Simulace registrace (např. volání API)
      this.$q.notify({
        message: `Welcome, ${this.name}! Your account has been created.`,
        color: 'positive',
        position: 'top'
      })

      // Přesměrování na jinou stránku, např. domovskou stránku
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.q-pa-md {
  margin-top: 10%;
}
</style>
