<script lang="ts">
import { fetchApi } from "$lib/api";

import { chatRoomMessagesStore,userStore } from "$lib/store";
import type { ChatMessagesPaginator,ChatRoom } from "$lib/utils";
import { afterUpdate, beforeUpdate, onMount } from "svelte";

export let chat: ChatRoom;
let chatPaginatorData: ChatMessagesPaginator | null = null;
let isLoading = true;
let message: string;
let div: any;
let autoscroll: boolean;

chatRoomMessagesStore.subscribe((d) => {
    const chatData = d.find((c) => c.chatId == chat.id);
    if (chatData) {
        chatPaginatorData = chatData;
    }
})

onMount(async () => {
    const chatId = chat.id;
    const response = await fetchApi(`chats/${chat.id}/messages/`);

    if (response.ok) {
        const data = await response.json();
        chatRoomMessagesStore.update((d) => {
            const newData = [...d]
            data.chatId = chat.id;
            newData.push(data)
            return newData;
        });
    }
    
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
                
                case "MESSAGE_CREATE":
                    chatRoomMessagesStore.update((chatsData) => {
                        const newData = [...chatsData]
                        const chatIndex = newData.findIndex((chat) => chat.chatId === chatId);

                        if (chatIndex >= 0) {
                            newData[chatIndex] = {
                                ...newData[chatIndex],
                                results: [...newData[chatIndex].results, eventPayload]
                            }
                        }
                        // console.log('eee')
                        return newData;
                    })
                    break;
                }
            };
            
            chatSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };
        isLoading = false;
        }
    )

beforeUpdate(() => {
    autoscroll = div && (div.offsetHeight + div.scrollTop) > (div.scrollHeight - 20);
});

afterUpdate(() => {
    if (autoscroll) div.scrollTo(0, div.scrollHeight);
});

const sendMessage = async () => {
    if (message) {
        const response = await fetchApi(`chats/${chat.id}/messages/`, {
            method: "POST",
            body: JSON.stringify({
                content: message,
            })
        });
        if (response.ok) {
            message = "";
        }
    }
}
</script>

{#if isLoading}
    <h1 class="text-2xl font-semibold text-center">Loading...</h1>
{:else}

<div class="scrollable h-60" bind:this={div}>
{#if chatPaginatorData}
{#each chatPaginatorData.results as message}
        <div class="flex">
            <h5 class="p-3 text-3xl">{message.author.username}</h5>
            <h5 class="py-2 text-3xl">{message.content}</h5>
        </div>

    {/each}
{/if}
</div>

<input type="text" bind:value={message} on:submit={sendMessage}>
<button class="rounded-lg p-2 bg-indigo-500 text-white" on:click={sendMessage}>Send</button>

{/if}

<style>
    .scrollable {
        flex: 1 1 auto;
		border-top: 1px solid #eee;
		margin: 0 0 0.5em 0;
		overflow-y: auto;
    }
</style>