import { PUBLIC_API_URL } from '$env/static/public';

export const load = async () => {
  const res = await fetch(`${PUBLIC_API_URL}/recipes`);
  const recipes = await res.json();
  return { recipes };
};
