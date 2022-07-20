import { writable } from 'svelte/store';

import type { ChatMessagesPaginator, ChatRoom, User } from './utils';


export const userStore = writable<User | null>(null);
export const publicRoomsStore = writable<ChatRoom[]>([]);
export const chatRoomMessagesStore = writable<ChatMessagesPaginator[]>([])
