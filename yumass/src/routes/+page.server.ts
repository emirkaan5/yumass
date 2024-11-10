import type { PageServerLoad, Actions } from "./$types.js";
import { fail } from "@sveltejs/kit";
import { superValidate } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";
import { formSchema } from "./schema";

export const load: PageServerLoad = async () => {
  return {
    form: await superValidate(zod(formSchema)),
  };
};

export const actions: Actions = {
  default: async (event) => {
    const form = await superValidate(event, zod(formSchema));
    if (!form.valid) {
      return fail(400, {
        form,
      });
    }
    console.log("asdasdd");

    try {
      // Replace with your actual API endpoint
      const apiEndpoint = "http://127.0.0.1:8001/api/v1/submit-form";

      // Replace with any required headers (e.g., Authorization)
      const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // 'Authorization': `Bearer YOUR_API_TOKEN`, // Uncomment and set if needed
        },
        body: JSON.stringify(form.data),
      });

      if (!response.ok) {
        // Attempt to parse error message from API response
        let errorMessage = "An error occurred while submitting the form.";
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch {
          // If response is not JSON, keep default error message
        }

        return fail(response.status, {
          form,
          error: errorMessage,
        });
      }

      // Optionally, parse success response
      const responseData = await response.json();

      // Return success message and any data from the API
      return {
        form,
        success: "Form submitted successfully!",
        data: responseData, // Optional: Use if you need to pass back data
      };
    } catch (error) {
      console.error("Form submission error:", error);
      return fail(500, {
        form,
        error: "A network error occurred. Please try again later.",
      });
    }

    return {
      form,
    };
  },
};
