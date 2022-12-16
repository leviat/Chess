<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import HelloWorld from './components/HelloWorld.vue'
import Chatbar from './components/Chatbar.vue'
import ChessBoard from './components/ChessBoard.vue'

</script>

<template>
  <div class="flex flex-row gap-2 justify-center">
    <ChessBoard :room_id="1"/>
    <Chatbar :room_id="1" class="bg-green-200" />
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
