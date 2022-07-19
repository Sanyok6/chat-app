<script lang="ts">
import { fetchApi } from "$lib/api";

    import { publicRoomsStore,userStore } from "$lib/store";
    import type { ChatRoom,User } from "$lib/utils";
    import { onMount } from "svelte";

    let userData: User | null=null;
    let publicChats: ChatRoom[] = [];

    onMount(async () => {
        userStore.subscribe((data) => userData = data);
        publicRoomsStore.subscribe((data) => publicChats = data);

        if (!userData) {
        const response = await fetchApi('auth/users/me/');
        const data = await response.json();

        if (response.ok) {
            userStore.set(data.user);
            publicRoomsStore.set(data.public_chats);
        } else {
            // Some sort of error idk
            // this probably won't happen
            // very rare
        }}
    })
</script>

{#if userData}
<h1 class="text-center">Hello {userData ? userData.username : null}</h1>

<h3 class="text-center">Public chats</h3>

<div class="flex items-center justify-center">
{#each publicChats as chat}
    <a href="/chat/{chat.id}" class="text-blue-500 hover:text-blue-600 hover:underline">{chat.name}</a>
{/each}
</div>

{:else}
    <h1 class="text-center text-4xl">Loading...</h1>
{/if}