<script lang="ts">
  export let type: 'text' | 'number' = 'text';
  export let value: string | number = '';
  export let min: number | undefined = undefined;
  export let max: number | undefined = undefined;
  export let step: number | string | undefined = undefined;
  export let placeholder = '';
  export let name = '';
</script>

{#if type === 'number'}
  <input
    class="input"
    bind:value
    type="number"
    {min}
    {max}
    {step}
    {placeholder}
    {name}
  />
{:else}
  <input class="input" bind:value type="text" {placeholder} {name} />
{/if}
