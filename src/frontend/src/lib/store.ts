import { writable } from 'svelte/store';

import type { ChatRoom, Message, User } from './utils';


interface ChatRoomMessages {
  id: string;
  messages: Message[];
}

export const userStore = writable<User | null>(null);
export const publicRoomsStore = writable<ChatRoom[]>([]);
export const chatRoomMessages = writable<ChatRoomMessages[]>([{id: '', messages: []}])
