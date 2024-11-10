<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import Sun from "svelte-radix/Sun.svelte";
  import Moon from "svelte-radix/Moon.svelte";
  import { toggleMode } from "mode-watcher";
  import type { PageData } from "./$types.js";
  import SuperDebug from 'sveltekit-superforms';
  import Form from "./form.svelte";
  export let data: PageData;
  let goal = 350;

  function handleClick(adjustment: number) {
    goal = Math.max(200, Math.min(400, goal + adjustment));
  }
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

<div
  class="container flex-col items-center justify-center min-h-screen max-w-lg place-content-center"
>
  <h1 class="text-center m-5 text-5xl">
    Redefine your UMass Dining Experience.
  </h1>
  <div class="w-full p-6 rounded shadow-md outline-double outline-1">
    
    <Form data={data.form} />
  </div>
</div>
<!-- <div>
  <Drawer.Root>
    <Drawer.Trigger asChild let:builder>
      <Button builders={[builder]} variant="outline">Open Drawer</Button>
    </Drawer.Trigger>
    <Drawer.Content>
      <div class="mx-auto w-full max-w-sm">
        <Drawer.Header>
          <Drawer.Title>About us</Drawer.Title>
          <Drawer.Description>Set your daily activity goal.</Drawer.Description>
        </Drawer.Header>
        <div class="p-4 pb-0">
          <div class="flex items-center justify-center space-x-2">
            <Button
              variant="outline"
              size="icon"
              class="h-8 w-8 shrink-0 rounded-full"
              on:click={() => handleClick(-10)}
              disabled={goal <= 200}
            >
              <Minus class="h-4 w-4" />
              <span class="sr-only">Decrease</span>
            </Button>
            <div class="flex-1 text-center">
              <div class="text-7xl font-bold tracking-tighter">
                {goal}
              </div>
              <div class="text-muted-foreground text-[0.70rem] uppercase">
                Calories/day
              </div>
            </div>
            <Button
              variant="outline"
              size="icon"
              class="h-8 w-8 shrink-0 rounded-full"
              on:click={() => handleClick(10)}
            >
              <Plus class="h-4 w-4" />
              <span class="sr-only">Increase</span>
            </Button>
          <!-- </div>
          <!-- <div class="mt-3 h-[120px]">
            <VisXYContainer {data} height={60}>
              <VisGroupedBar {x} {y} color="hsl(var(--primary) / 0.2)" />
            </VisXYContainer>
          </div>
        </div>
        <Drawer.Footer>
          <Button>Submit</Button>
          <Drawer.Close asChild let:builder>
            <Button builders={[builder]} variant="outline">Cancel</Button>
          </Drawer.Close>
        </Drawer.Footer>
      </div>
    </Drawer.Content>
  </Drawer.Root>
</div> -->
