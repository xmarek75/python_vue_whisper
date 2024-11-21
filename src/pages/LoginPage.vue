<template>
  <div class="q-pa-md" style="max-width: 400px; margin: 0 auto;">
    <q-card>
      <q-card-section>
        <div class="text-h6">Login</div>
        <div class="text-subtitle2">Enter your credentials below</div>
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="username"
          label="Username"
          outlined
          dense
          autofocus
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          outlined
          dense
          class="q-mt-md"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn color="primary" label="Login" @click="handleLogin" />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      if (!this.username || !this.password) {
        this.$q.notify({
          message: 'Please enter both username and password',
          color: 'negative',
          position: 'top'
        });
        return;
      }

      // Simulate login process (e.g., API call)
      if (this.username === 'admin' && this.password === 'password') {
        this.$q.notify({
          message: 'Login successful!',
          color: 'positive',
          position: 'top'
        });
        // Redirect to a different page
        this.$router.push('/try/try_without_registration'); // change route
      } else {
        this.$q.notify({
          message: 'Invalid username or password',
          color: 'negative',
          position: 'top'
        });
      }
    }
  }
};
</script>

<style scoped>
.q-pa-md {
  margin-top: 10%;
}
</style>
