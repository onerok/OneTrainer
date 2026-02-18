<script lang="ts">
  import type { ToolInfo } from '../../lib/api/types';
  import Button from '../../lib/components/ui/Button.svelte';

  export let toolsList: ToolInfo[] = [];
  export let saving = false;
  export let onReload: () => void | Promise<void>;
  export let onToolAction: (tool: ToolInfo) => void;
</script>

<div class="general-form">
  <div class="field-grid">
    {#each toolsList as tool}
      <div class="field-row full-width">
        <div class="concept-header">
          <strong>{tool.name}</strong>
          <Button type="button" on:click={() => onToolAction(tool)}>
            {tool.action_type === 'WEB_LINK' ? 'Open' : tool.action_type === 'CLI_COMMAND' ? 'Copy Command' : 'Show Info'}
          </Button>
        </div>
        <p class="muted">{tool.description}</p>
        {#if tool.action_type !== 'WEB_LINK'}
          <p><code>{tool.action_value}</code></p>
        {/if}
      </div>
    {/each}
  </div>
  <div class="action-row">
    <Button type="button" disabled={saving} on:click={onReload}>Reload</Button>
  </div>
</div>
