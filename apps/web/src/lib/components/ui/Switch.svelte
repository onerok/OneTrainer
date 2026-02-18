<script lang="ts">
  export let checked = false;
  export let name = '';
</script>

<label class="switch">
  <input type="checkbox" bind:checked {name} />
  <span class="switch-track">
    <span class="switch-thumb" />
  </span>
</label>
