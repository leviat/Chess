<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue';
import type { Ref } from 'vue';
import ChessPiece from './ChessPiece.vue';
import { PieceColor, BoardOccupancy, Piece, Board } from '../scripts/ChessClasses';

import { api_chess_room } from '../scripts/api'

interface Props {
    room_id: number,
}

const props = defineProps<Props>()
const board = new Board();
const boardFields = board.getFields();
const playerColor: Ref<PieceColor | null> = ref(PieceColor.BLACK);

//const board: BoardOccupancy = reactive(new Array<Piece | null>(64));
const focusedField: Ref<number | null> = ref(null);
const movableFields = computed(() =>
    (focusedField.value !== null && board.isOccupied(focusedField.value))
        ? boardFields[focusedField.value]!.movableFields()
        : new Array<number>());
const attackableFields = computed(() =>
    (focusedField.value !== null && board.isOccupied(focusedField.value))
        ? boardFields[focusedField.value]!.attackableFields()
        : new Array<number>());

const isLoading = ref(true);

onMounted(() => {
    api_chess_room.get(props.room_id).then(
        res => {
            res.forEach(piece => {
                if (piece instanceof Piece) {
                    board.spawn(piece.type, piece.color, piece.pos)
                }
            });
            isLoading.value = false;
        }
    ).catch(err => console.log(err));
})

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
    // piece already in focus?
    // possible actions:
    // 1. move / attack specified field if possible
    // 2. otherwise remove focus

    if (pos === focusedField.value) {
        focusedField.value = null;
        return;
    }

    if (focusedField.value !== null) {
        if (board.getPiece(focusedField.value)?.interact(pos)) {
            focusedField.value = null;
            return;
        }
    }

    if (board.isOccupied(pos) && board.getColor(pos) === playerColor.value) {
        focusedField.value = pos;
        return;
    }
}

</script>

<template>
    <div class="bg-blue-200 grid grid-cols-8 grid-rows-8 gap-0 self-center" style="height: 40vw; width: 40vw"
        data-test="board">
        <ChessPiece v-for="pos in boardFields.keys()" :class="backgroundColor(pos)"
            class="h-full w-full p-2 justify-self-center self-center" :piece="board.getPiece(pos)"
            @click="handleClick(pos)" :room-id="props.room_id" />
    </div>
</template>