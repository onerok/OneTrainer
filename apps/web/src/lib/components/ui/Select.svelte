<script lang="ts">
  export let value = '';
  export let options: string[] = [];
  export let name = '';
</script>

<select class="select" bind:value {name}>
  {#each options as option}
    <option value={option}>{option}</option>
  {/each}
</select>
