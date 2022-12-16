<script setup lang="ts">
import { computed } from 'vue';
import { Piece, PieceType, PieceColor } from '../scripts/ChessClasses';

interface Props {
    piece: Piece | null
}

const props = defineProps<Props>()

const imageURL = new Map();
imageURL.set([PieceType.BISHOP, PieceColor.WHITE].join(','), 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg')
imageURL.set([PieceType.BISHOP, PieceColor.BLACK].join(','), 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg')
imageURL.set([PieceType.KNIGHT, PieceColor.BLACK].join(','), 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg')
imageURL.set([PieceType.KNIGHT, PieceColor.WHITE].join(','), 'https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg')
imageURL.set([PieceType.KING, PieceColor.BLACK].join(','), 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg')
imageURL.set([PieceType.KING, PieceColor.WHITE].join(','), 'https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg')
imageURL.set([PieceType.PAWN, PieceColor.BLACK].join(','), 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg')
imageURL.set([PieceType.PAWN, PieceColor.WHITE].join(','), 'https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg')
imageURL.set([PieceType.QUEEN, PieceColor.BLACK].join(','), 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg')
imageURL.set([PieceType.QUEEN, PieceColor.WHITE].join(','), 'https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg')
imageURL.set([PieceType.ROOK, PieceColor.BLACK].join(','), 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg')
imageURL.set([PieceType.ROOK, PieceColor.WHITE].join(','), 'https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg')

const pieceImage = computed(() => imageURL.get([props.piece?.type, props.piece?.color].join(',')))

</script>

<template>
    <img v-if="(props.piece !== null)" class="" :src="pieceImage" alt="" data-test="chess-piece">
    <div v-else></div>
</template>