<script setup lang="ts">
import ChessBoard from './ChessBoard.vue';
import ChatBar from './ChatBar.vue';
import PlayerBar from './PlayerBar.vue';
import { PieceColor, PlayerRole } from '../scripts/ChessClasses';
import { ref, Ref } from 'vue';

interface Props {
    room_id: number,
}

const props = defineProps<Props>()
const playerRole: Ref<PlayerRole | PieceColor> = ref(PlayerRole.OBSERVER);

</script>

<template>
    <div class="flex flex-row gap-2 justify-center">
        <ChessBoard :room_id="props.room_id" :role="playerRole" class="border border-gray-400 shadow-sm"
            style="height: 40vw; width: 40vw" />
        <div class="flex flex-col">
            <PlayerBar :room_id="room_id" @player-color-changed="newColor => playerRole = newColor"></PlayerBar>
            <ChatBar class="flex-grow" :room_id="room_id" />
        </div>
    </div>
</template>