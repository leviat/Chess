<script setup lang="ts">
import { onMounted, ref, Ref } from 'vue';
import { api_chess_room, api_role } from '../scripts/api';
import { Piece, PieceColor, PlayerRole } from '../scripts/ChessClasses';

interface Props {
    room_id: number,
}

const props = defineProps<Props>()
const playerRole: Ref<PieceColor | PlayerRole> = ref(PlayerRole.OBSERVER);

const emit = defineEmits<{
    (e: 'playerColorChanged', newColor: PieceColor): void
}>()

// get players
onMounted(() => {
    api_role.get(props.room_id).then(
        res => {
            playerRole.value = res;

            if (res === PieceColor.WHITE)
                emit('playerColorChanged', res);
            else if (res === PieceColor.BLACK)
                emit('playerColorChanged', res);
            else
                api_role.register(props.room_id, PieceColor.WHITE).then(res => {
                    playerRole.value = PieceColor.WHITE;
                    emit('playerColorChanged', PieceColor.WHITE);
                }).catch(err =>
                    api_role.register(props.room_id, PieceColor.BLACK).then(res => {
                        playerRole.value = PieceColor.BLACK;
                        emit('playerColorChanged', PieceColor.BLACK);
                    })
                )
        }
    )
})


</script>

<template>
    <div class="max-w-xs flex flex-col h-auto p-2 bg-white rounded-sm">
        <div>Our role:
            <span v-if="playerRole == PlayerRole.OBSERVER">Observer</span>
            <span v-else-if="playerRole == PieceColor.BLACK">Black</span>
            <span v-else>White</span>
        </div>
    </div>
</template>