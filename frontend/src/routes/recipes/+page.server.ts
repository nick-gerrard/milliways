export const load = async () => {
  const res = await fetch("http://localhost:8000/recipes");
  const recipes = await res.json();
  return { recipes };
}
