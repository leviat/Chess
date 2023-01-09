<script setup lang="ts">
import { stringifyExpression } from '@vue/compiler-core';
import { ref, reactive, onMounted } from 'vue';

interface Props {
  room_id: number,
}

const props = defineProps<Props>()

interface Message {
  user: string,
  text: string,
}

const chatOpened = ref(false);
let chatSocket: WebSocket;
let backOffTime = 200;

const connectToChatSocket = () => {
  chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${props.room_id}/`);

  chatSocket.onclose = function (e: Event): void {
    chatOpened.value = false;
    console.log('Chat socket closed.');
    backOffTime = backOffTime < 20000 ? backOffTime * 2 + Math.random() * 100 : backOffTime;
    setTimeout(connectToChatSocket, backOffTime);
  };

  chatSocket.onmessage = function (e: MessageEvent): void {
    const data = JSON.parse(e.data);
    messages.push({ 'user': data.user, 'text': data.text })
  };

  chatSocket.onopen = function (e: Event): void {
    chatOpened.value = true;
    backOffTime = 200;
  }
};

onMounted(() => connectToChatSocket());

const messages: Message[] = reactive([]); // list of messages we received
const messageText = ref(""); // current message that is being typed in

function handleMessageEntered(e: KeyboardEvent | MouseEvent): void {
  if (e instanceof KeyboardEvent && e.key == "Enter") {
    e.preventDefault(); // prevent enter from creating a new line
  }

  if (messageText.value.length == 0) {
    return
  }

  let payload = JSON.stringify({
    'text': messageText.value.trim(),
  });
  chatSocket.send(payload);
  messageText.value = "";
}

</script>

<template>
  <div class="max-w-xs flex flex-col h-auto p-2 bg-white rounded-sm">
    <div id="#chatBar" class="border-2 border-gray-400 overflow-y-scroll w-full flex-grow text-left px-4 py-2">
      <p v-for="message in messages">
        {{ message.user }}:
        <span class="font-sans text-slate-500"> {{ message.text }}</span>
      </p>

      <p class="font-mono text-xs my-2" v-if="!chatOpened">
        <svg aria-hidden="true"
          class="h-4 w-4 inline-block text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300"
          viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="currentColor" />
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentFill" />
        </svg>
        Trying to connect to chat
      </p>
    </div>
    <div>
      <textarea class="border-2 border-gray-400 px-4 py-2 w-full resize-none" v-model="messageText"
        placeholder="Enter message..." @keypress.enter.exact="handleMessageEntered"> </textarea>
      <button class="bg-gray-200" @click="handleMessageEntered" :disabled="!chatOpened">Send</button>
    </div>
  </div>

</template>