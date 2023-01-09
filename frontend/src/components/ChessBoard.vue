<script setup lang="ts">
import type { Ref } from 'vue';
import { ref, computed, watch, onMounted } from 'vue';
import ChessPiece from './ChessPiece.vue';
import { PieceColor, Board, PlayerRole, Match } from '../scripts/ChessClasses';
import { ChessSocket, InteractionEvent } from '../scripts/ChessSocket';

interface Props {
    room_id: number,
    role: PlayerRole | PieceColor,
}

const props = defineProps<Props>()
const match = new Match(new Board(), props.role, PieceColor.WHITE);
let chessSocket: ChessSocket;

const handleInteractionEvent = (event: InteractionEvent): void => {
    if (match.board.getPiece(event.source)?.interact(event.target)) {
        match.nextTurn();
    }
    else {
        console.error(`Error: Invalid action of ${event.source} to ${event.target}`);
    }
}

onMounted(() => {
    chessSocket = new ChessSocket(props.room_id);

    chessSocket.subscribeMatchState(state => {
        state.pieces.forEach(piece => match.board.spawn(piece.type, piece.color, piece.pos));
        match.turn = state.turn;
    })

    watch(() => props.role, (newRole, oldRole) => {
        if (oldRole === PlayerRole.OBSERVER)
            chessSocket.unsubscribeInteractionAll(handleInteractionEvent);
        else if (oldRole === PieceColor.BLACK)
            chessSocket.unsubscribeInteractionWhite(handleInteractionEvent);
        else if (oldRole === PieceColor.WHITE)
            chessSocket.unsubscribeInteractionBlack(handleInteractionEvent);

        if (newRole === PlayerRole.OBSERVER)
            chessSocket.subscribeInteractionAll(handleInteractionEvent);
        else if (newRole === PieceColor.BLACK)
            chessSocket.subscribeInteractionWhite(handleInteractionEvent);
        else if (newRole === PieceColor.WHITE)
            chessSocket.subscribeInteractionBlack(handleInteractionEvent);
    }, { immediate: true });
})

const focusedField: Ref<number | null> = ref(null);
const movableFields = computed(() =>
    (focusedField.value !== null && match.board.isOccupied(focusedField.value))
        ? match.board.getFields()[focusedField.value]!.movableFields()
        : new Array<number>());
const attackableFields = computed(() =>
    (focusedField.value !== null && match.board.isOccupied(focusedField.value))
        ? match.board.getFields()[focusedField.value]!.attackableFields()
        : new Array<number>());

function backgroundColor(pos: number): string {
    if (focusedField.value === pos) {
        return "bg-green-800";
    }

    if (movableFields.value.includes(pos)) {
        return "bg-green-400";
    }

    if (attackableFields.value.includes(pos)) {
        return "bg-red-400";
    }

    if ((pos / 8) % 2 >= 1) {
        return (pos % 2 == 1) ? "bg-orange-100" : "bg-orange-700";
    }
    else {
        return (pos % 2 == 0) ? "bg-orange-100" : "bg-orange-700";
    }
}

function handleClick(pos: number) {
    if (match.turn !== props.role) {
        return;
    }

    if (focusedField.value === null) {
        if (match.board.isOccupied(pos) && match.board.getColor(pos) === props.role) {
            focusedField.value = pos;
            return;
        }
        return;
    }

    if (pos === focusedField.value) {
        focusedField.value = null;
        return;
    }

    if (match.board.getPiece(focusedField.value)!.interact(pos)) {
        chessSocket.publishInteraction({ source: focusedField.value, target: pos, color: props.role })
        focusedField.value = null;
        match.nextTurn();
    }
}

</script>

<template>
    <div class="grid grid-cols-8 grid-rows-8 gap-0 self-center" data-test="board">
        <ChessPiece v-for="pos in match.board.getFields().keys()" :class="backgroundColor(pos)"
            class="h-full w-full p-2 justify-self-center self-center" :piece="match.board.getPiece(pos)"
            @click="handleClick(pos)" />
    </div>
</template>