import { env } from '$env/dynamic/private';

export const load = async () => {
  const apiUrl = env.INTERNAL_API_URL ?? "http://127.0.0.1:8002";
  const res = await fetch(`${apiUrl}/recipes`);
  const recipes = await res.json();
  return { recipes };
};
