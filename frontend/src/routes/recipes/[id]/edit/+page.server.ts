import { env } from '$env/dynamic/private';
import { error } from '@sveltejs/kit';

export const load = async ({ params }) => {
  const apiUrl = env.INTERNAL_API_URL ?? "http://127.0.0.1:8002";
  const res = await fetch(`${apiUrl}/recipes/${params.id}`);
  if (!res.ok) error(404, 'Recipe not found');
  const recipe = await res.json();
  return { recipe };
};
