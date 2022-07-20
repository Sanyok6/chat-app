export interface User {
  id: number;
  username: string;
  is_staff: boolean;
  is_online: boolean;
  is_banned: boolean;
}

export interface ChatRoom {
  id: string;
  name: string;
  description: string;
  is_public: boolean;
  creator: User;
  created_at: string;
}

export interface Message {
  id: number;
  author: User;
  chat_room: string;
  content: string;
  created_at: string;
  edited_at: string | null;
}


export interface ChatMessagesPaginator {
  chatId: string;
  count: number;
  next: string | null;
  previous: string | null;
  results: Array<Message>;
}
