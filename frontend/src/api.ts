import type { Quote, Recipe } from "./types";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function http<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status} - ${text}`);
  }
  return res.json();
}

export function fetchRecipes(): Promise<Recipe[]> {
  return http<Recipe[]>("/recipes");
}

export function fetchQuote(recipeId: number, date: string): Promise<Quote> {
  const qs = new URLSearchParams({
    recipe_id: String(recipeId),
    date,
  });
  return http<Quote>(`/quote?${qs.toString()}`);
}
