import { z } from "zod";
 

export const formSchema = z.object({
 username: z.string().min(2).max(50),
 allergens: z.array(z.string()).refine((value) => value.length > 0, {
    message: "You have to select at least one allergen.",
  }),
  kosher: z.boolean().default(false).optional(),
});
 
export type FormSchema = typeof formSchema;