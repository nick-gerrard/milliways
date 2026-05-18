
export interface Recipe {
  id: number;
  name: string;
  description?: string;
  imageUrl?: string;
  tags?: string[]
  prep_time_minutes: number;
  cook_time_minutes: number;
}
