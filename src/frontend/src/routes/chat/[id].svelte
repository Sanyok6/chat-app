<script lang="ts">
import { fetchApi } from "$lib/api";

import { userStore } from "$lib/store";
import type { ChatRoom } from "$lib/utils";
import { onMount } from "svelte";

export let chat: ChatRoom;

let message: string;

onMount(async () => {
    const response = await fetchApi("/api/chat/rooms");
    const chatSocket = new WebSocket(`ws://${window.location.host}/api/ws/${chat.id}/`);
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const eventName: string = data.event;
        const eventPayload = data.payload;
        console.log(eventName)

        switch (eventName.toUpperCase()) {
            case "READY":
                userStore.set(eventPayload.user)
                break;
        
            default:
                break;
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
})
</script>

<input type="text" bind:value={message}>
<button class="rounded-lg p-2 bg-indigo-500 text-white">Send</button>