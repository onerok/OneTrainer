<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let activeTab = 'general';
  const dispatch = createEventDispatcher<{ change: { tabId: string } }>();

  const tabs = [
    { id: 'general', label: 'General', disabled: false },
    { id: 'model', label: 'Model', disabled: false },
    { id: 'lora', label: 'LoRA', disabled: false },
    { id: 'data', label: 'Data', disabled: false },
    { id: 'concepts', label: 'Concepts', disabled: false },
    { id: 'training', label: 'Training', disabled: false },
    { id: 'sampling', label: 'Sampling', disabled: false },
    { id: 'backup', label: 'Backup', disabled: false },
    { id: 'tools', label: 'Tools', disabled: false }
  ];

  function onTabClick(tabId: string, disabled: boolean) {
    if (disabled) {
      return;
    }
    dispatch('change', { tabId });
  }
</script>

<div class="tabs" role="tablist" aria-label="OneTrainer Tabs">
  {#each tabs as tab}
    <button
      class="tab-btn"
      class:active={tab.id === activeTab}
      type="button"
      disabled={tab.disabled}
      role="tab"
      aria-selected={tab.id === activeTab}
      aria-disabled={tab.disabled}
      on:click={() => onTabClick(tab.id, tab.disabled)}
    >
      {tab.label}
    </button>
  {/each}
</div>
