<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import Sun from "svelte-radix/Sun.svelte";
    import Moon from "svelte-radix/Moon.svelte";
    import { toggleMode } from "mode-watcher";
    import * as Card from "$lib/components/ui/card";
    import * as Resizable from "$lib/components/ui/resizable";
    import type { PageData } from "./$types.js";
    import SettingsForm from "./form.svelte";
    export let data: PageData;
  </script>
   
  <!-- <Button>Click me</Button>
    -->
  <Button on:click={toggleMode} variant="outline" size="icon">
    <Sun
      class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
    />
    <Moon
      class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
    />
    <span class="sr-only">Toggle theme</span>
  </Button>

  <div class="flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md p-6 rounded shadow-md">
      <SettingsForm data={data.form} />
    </div>
  </div>
