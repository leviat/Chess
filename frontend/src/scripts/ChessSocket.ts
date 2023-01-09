import { PieceColor, PlayerRole, PieceType } from "./ChessClasses";

interface ChessWSMessage {
    type: string,
    data: InteractionEvent | MatchStateEvent
}

export interface InteractionEvent {
    color: PieceColor,
    source: number,
    target: number,
}

export interface MatchStateEvent {
    pieces: Array<PieceBackend>,
    turn: PieceColor,
}

export interface ChatMessageEvent {

}

interface PieceBackend {
    pos: number,
    type: PieceType,
    color: PieceColor,
}

type Interactioncb = (event: InteractionEvent) => void;
type MatchStatecb = (event: MatchStateEvent) => void;

export class ChessSocket {
    protected socket!: WebSocket
    protected _isOpen: boolean = false;
    protected roomID: number
    protected backOffTime: number
    protected interactionSubscribersAll: Array<Interactioncb>
    protected interactionSubscribersWhite: Array<Interactioncb>
    protected interactionSubscribersBlack: Array<Interactioncb>
    protected matchStateSubscribers: Array<MatchStatecb>;

    protected msgSendQueue: Array<ChessWSMessage>;

    constructor(roomID: number) {
        this.isOpen = false;
        this.backOffTime = 200; // exponential backoff reconnection
        this.roomID = roomID;
        this.interactionSubscribersAll = new Array();
        this.interactionSubscribersAll.push((e) => console.log(`All: ${e}`));
        this.interactionSubscribersWhite = new Array();
        this.interactionSubscribersWhite.push((e) => console.log(`White: ${e}`));
        this.interactionSubscribersBlack = new Array();
        this.interactionSubscribersBlack.push((e) => console.log(`Black: ${e}`));
        this.matchStateSubscribers = new Array();
        this.msgSendQueue = new Array();

        this.connect();
    }

    get isOpen() {
        return this._isOpen;
    }

    protected set isOpen(b: boolean) {
        this._isOpen = b;
    }

    protected connect = (): void => {
        let chessSocket: ChessSocket = this;
        this.socket = new WebSocket(`ws://localhost:8000/ws/chess/room/${this.roomID}`);
        this.socket.onclose = function (e: Event): void {
            chessSocket.isOpen = false;
            console.log('Chess socket closed.');
            chessSocket.backOffTime = chessSocket.backOffTime < 20000
                ? chessSocket.backOffTime * 2 + Math.random() * 100
                : chessSocket.backOffTime;
            setTimeout(chessSocket.connect, chessSocket.backOffTime);
        };

        this.socket.onmessage = function (e: MessageEvent): void {
            const msg: ChessWSMessage = JSON.parse(e.data);

            if (msg.type === 'state') {
                let stateEvent: MatchStateEvent = msg.data as MatchStateEvent;
                chessSocket.matchStateSubscribers.forEach(cb => cb(stateEvent));
            }
            else if (msg.type === 'interaction') {
                let interactionEvent = msg.data as InteractionEvent;
                chessSocket.interactionSubscribersAll.forEach(cb => cb(interactionEvent));

                if (interactionEvent.color === PieceColor.BLACK)
                    chessSocket.interactionSubscribersBlack.forEach(cb => cb(interactionEvent));
                else if (interactionEvent.color === PieceColor.WHITE)
                    chessSocket.interactionSubscribersWhite.forEach(cb => cb(interactionEvent));
            }
        };

        this.socket.onopen = function (e: Event): void {
            chessSocket.backOffTime = 200;
            chessSocket.isOpen = true;
            console.log("Chess socket opened.");
            chessSocket.msgSendQueue.forEach(msg => this.send(JSON.stringify(msg)));
            chessSocket.msgSendQueue.splice(0, Infinity);
        };
    };

    subscribeMatchState(cb: (event: MatchStateEvent) => void) {
        this.matchStateSubscribers.push(cb);
    }

    unsubscribeMatchState(cb: (event: MatchStateEvent) => void) {
        let i = this.matchStateSubscribers.indexOf(cb);

        if (i > 0)
            this.matchStateSubscribers.splice(i, 1);
    }

    subscribeInteractionAll(cb: (event: InteractionEvent) => void) {
        this.interactionSubscribersAll.push(cb)
    }

    unsubscribeInteractionAll(cb: (event: InteractionEvent) => void) {
        let i = this.interactionSubscribersAll.indexOf(cb)

        if (i > -1)
            this.interactionSubscribersAll.splice(i, 1)
    }

    subscribeInteractionWhite(cb: (event: InteractionEvent) => void) {
        this.interactionSubscribersWhite.push(cb)
    }

    unsubscribeInteractionWhite(cb: (event: InteractionEvent) => void) {
        let i = this.interactionSubscribersWhite.indexOf(cb)

        if (i > -1)
            this.interactionSubscribersWhite.splice(i, 1)
    }

    subscribeInteractionBlack(cb: (event: InteractionEvent) => void) {
        this.interactionSubscribersBlack.push(cb)
    }

    unsubscribeInteractionBlack(cb: (event: InteractionEvent) => void) {
        let i = this.interactionSubscribersBlack.indexOf(cb)

        if (i > -1)
            this.interactionSubscribersBlack.splice(i, 1)
    }

    publishInteraction(event: InteractionEvent) {
        let msg: ChessWSMessage = { type: 'interaction', data: event }
        if (!this.isOpen) {
            this.msgSendQueue.push(msg);
        }
        else {
            this.socket.send(JSON.stringify(msg));
        }
    }
}