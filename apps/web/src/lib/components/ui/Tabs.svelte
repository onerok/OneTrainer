<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { TAB_ROUTES, type AppRoute, type TabId } from '../../../app/routes';

  export let activeTab: TabId = 'general';
  export let tabs: AppRoute[] = TAB_ROUTES;
  const dispatch = createEventDispatcher<{ change: { tabId: TabId } }>();

  function onTabClick(tabId: TabId, disabled: boolean) {
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
