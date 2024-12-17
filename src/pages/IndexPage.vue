<template>
  <div class="q-pa-md" style="max-width: 400px; margin: 0 auto; text-align: center;">
    <q-card>
      <q-card-section>
        <div class="text-h5">Welcome</div>
        <div class="text-subtitle2 q-mt-sm">Choose an option to get started</div>
      </q-card-section>

      <q-card-actions class="q-mt-lg justify-center">
        <q-btn
          color="primary"
          label="Sign Up"
          size="lg"
          class="q-mb-md"
          @click="$router.push('/auth/signup')"
        />
        <q-btn
          color="secondary"
          label="Sign In"
          size="lg"
          class="q-mb-md"
          @click="$router.push('/auth/login')"
        />
      </q-card-actions>

      <q-card-actions class="justify-center">
        <q-btn
          flat
          label="Try without registration"
          color="primary"
          size="sm"
          @click="$router.push('/try/try_without_registration')"
        />
      </q-card-actions>
      <q-card-actions class="justify-center">
        <q-btn
          flat
          label="Test whisper"
          color="primary"
          size="sm"
          @click="$router.push('/try/Whisper')"
        />
      </q-card-actions>
      <q-card-actions class="justify-center">
        <q-btn
          flat
          label="TimeLine"
          color="primary"
          size="sm"
          @click="$router.push('/try/TimeLineTest')"
        />
      </q-card-actions>
    </q-card>
  </div>
</template>

<script>
export default {
  name: 'IndexPage'
}
</script>

<style scoped>
.q-pa-md {
  margin-top: 10%;
}
</style>
