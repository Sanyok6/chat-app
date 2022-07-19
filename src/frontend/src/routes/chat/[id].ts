import { fetchApi, parseCookies } from "$lib/api";
import type { RequestEvent } from "@sveltejs/kit";


export async function GET(event: RequestEvent) {
  const cookie = event.request.headers.get('cookie') || ''
  const response = await fetchApi(`chats/${event.params.id}/`, {}, parseCookies(cookie, 'csrftoken'));
  
  if (!response.ok) {
    return {
      status: response.status,
    }
  }

  return {
    status: response.status,
    headers: {},
    body: { chat : await response.json() },
  };
}
