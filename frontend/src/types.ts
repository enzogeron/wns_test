export type Recipe = {
  id: number;
  name: string;
  instructions?: string | null;
};

export type Ingredient = {
  name_raw: string;
  name_norm: string;
  required_g: number;
  buy_g: number;
  cost_per_kg: number;
  cost_ars: number;
};

export type Quote = {
  recipe_id: number;
  recipe_name: string;
  date: string;
  usd_to_ars: number;
  total_ars: number;
  total_usd: number;
  items: Ingredient[];
  instructions?: string | null;
};
