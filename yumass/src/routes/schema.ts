import { z } from "zod";
 

export const formSchema = z.object({
 email: z.string().min(2).max(50),
 username: z.string().min(2).max(50),
 allergens: z.array(z.string()).refine((value) => value.length > 0, {
    message: "You have to select at least one allergen.",
  }),
  kosher: z.boolean().default(false).optional(),
  vegan: z.boolean().default(false).optional(),
  vegetarian: z.boolean().default(false).optional(),
  halal: z.boolean().default(false).optional(),
  preferences: z.string().min(0).max(300)

});
 
export type FormSchema = typeof formSchema;