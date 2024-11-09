<script lang="ts">
    import * as Form from "$lib/components/ui/form";
    import { Input } from "$lib/components/ui/input";
    import { formSchema, type FormSchema } from "./schema";
    import {
     type SuperValidated,
     type Infer,
     superForm,
    } from "sveltekit-superforms";
    import { zodClient } from "sveltekit-superforms/adapters";
    import { Checkbox } from "$lib/components/ui/checkbox";
    import { toast } from "svelte-sonner";
    export let data: SuperValidated<Infer<FormSchema>>;
    
    // const form = superForm(data, {
    //  validators: zodClient(formSchema),
    // });
    const form = superForm(data, {
    validators: zodClient(formSchema),
    onUpdated: ({ form: f }) => {
      if (f.valid) {
        toast.success(`You submitted ${JSON.stringify(f.data, null, 2)}`);
      } else {
        toast.error("Please fix the errors in the form.");
      }
    }
  });

    const allergens = [
    { id: "peanuts", label: "Peanuts" },
    { id: "gluten", label: "Gluten" },
    { id: "soy", label: "Soy" },
    { id: "dairy", label: "Dairy" },
    { id: "shellfish", label: "Shellfish" },
    { id: "eggs", label: "Eggs" },
  ] as const; 
    const { form: formData, enhance } = form;

   </script>
    
   <form method="POST" use:enhance id="form">
    <Form.Fieldset {form} name="username">
     <Form.Control let:attrs>
      <Form.Label>E-Mail!</Form.Label>
      <Input {...attrs} bind:value={$formData.username} />
     </Form.Control>
     <Form.Description>We will use this email to send you daily email newsletters.</Form.Description>
     <Form.FieldErrors/>
    </Form.Fieldset>
    <Form.Fieldset {form} name="allergens" class="space-y-0">
		<div class="mb-4">
			<Form.Legend class="text-base">Allergens</Form.Legend>
			<Form.Description>
				Choose your allergens so we don't kill you.
			</Form.Description>
		</div>
		<div class="space-y-2">
			{#each allergens as item}
				{@const checked = $formData.allergens.includes(item.id)}
				<div class="flex flex-row items-center space-x-3">
					<Form.Control let:attrs>
						{@const { name, ...rest } = attrs}
						<Checkbox
							{...rest}
							{checked}
							onCheckedChange={(v) => {
								if (v) {
									$formData.allergens = [...$formData.allergens, item.id];
								} else {
									$formData.allergens = $formData.allergens.filter((i) => i !== item.id);
								}
							}}
						/>
						<Form.Label class="font-normal">
							{item.label}
						</Form.Label>
						<input type="checkbox" {name} hidden value={item.id} {checked} />
					</Form.Control>
				</div>
			{/each}
			<Form.FieldErrors />
		</div>
	</Form.Fieldset>
    <Form.Button>Submit</Form.Button>
   </form>