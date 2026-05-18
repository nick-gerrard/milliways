import { INTERNAL_API_URL } from '$env/dynamic/private';

export const load = async () => {
  const res = await fetch(`${INTERNAL_API_URL}/recipes`);
  const recipes = await res.json();
  return { recipes };
};
