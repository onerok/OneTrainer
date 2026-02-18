<script lang="ts">
  export let type: 'button' | 'submit' = 'button';
  export let disabled = false;
</script>

<button {type} {disabled} class="btn" on:click>
  <slot />
</button>
